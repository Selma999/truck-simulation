import numpy as np
import pandas as pd
import json
import random
import os
import requests
import time
from typing import List, Tuple, Dict
import math
import geopandas as gpd
from shapely.geometry import Point

class TruckRouting:
    def __init__(self, metros_file: str = None, osrm_url: str = "https://router.project-osrm.org", 
                 valhalla_url: str = None, router_type: str = "osrm", states_geojson: str = None):
        """Initialize routing system with OSRM/Valhalla and spatial analysis"""
        if metros_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            metros_file = os.path.join(current_dir, '..', 'data', 'metros.json')
        
        with open(metros_file, 'r') as f:
            self.metros_data = json.load(f)
        self.metros = self.metros_data['metros']
        
        self.osrm_url = osrm_url
        self.valhalla_url = valhalla_url
        self.router_type = router_type
        
        # Load US states GeoJSON for spatial analysis
        if states_geojson is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            states_geojson = os.path.join(current_dir, '..', 'data', 'us_states.geojson')
        
        try:
            self.states_gdf = gpd.read_file(states_geojson)
            # Normalize expected state name column to 'STATE_NAME'
            if 'NAME' in self.states_gdf.columns:
                self.states_gdf = self.states_gdf.rename(columns={'NAME': 'STATE_NAME'})
            elif 'name' in self.states_gdf.columns:
                self.states_gdf = self.states_gdf.rename(columns={'name': 'STATE_NAME'})
            print(f"Loaded {len(self.states_gdf)} US states for spatial analysis")
        except FileNotFoundError:
            print("US states GeoJSON not found. Please download us_states.geojson to data/ folder")
            self.states_gdf = None
        
    def get_valhalla_route(self, start_lat: float, start_lon: float, 
                          end_lat: float, end_lon: float) -> Dict:
        """Get real route from Valhalla"""
        try:
            if self.valhalla_url is None:
                raise ValueError("Valhalla URL not configured")
                
            # Valhalla route API call
            url = f"{self.valhalla_url}/route"
            payload = {
                "locations": [
                    {"lat": start_lat, "lon": start_lon},
                    {"lat": end_lat, "lon": end_lon}
                ],
                "costing": "auto",
                "directions_options": {
                    "units": "kilometers"
                }
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'trip' not in data or not data['trip']['legs']:
                raise ValueError(f"Valhalla didn't find the route: {data}")
            
            leg = data['trip']['legs'][0]
            geometry = leg['shape']
            
            # Decode polyline geometry (Valhalla encodes with precision=6)
            import polyline
            route_points = [(lat, lon) for lat, lon in polyline.decode(geometry, 6)]
            
            return {
                'route_points': route_points,
                'distance_meters': leg['summary']['length'] * 1000,  # Convert km to meters
                'duration_seconds': leg['summary']['time'],
                'distance_km': leg['summary']['length'],
                'duration_hours': leg['summary']['time'] / 3600
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Valhalla API error: {e}")
            raise RuntimeError(f"Valhalla API failed: {e}")
        except Exception as e:
            print(f"Error in Valhalla call: {e}")
            raise RuntimeError(f"Valhalla routing failed: {e}")

    def get_osrm_route(self, start_lat: float, start_lon: float, 
                      end_lat: float, end_lon: float) -> Dict:
        """Get real route from OSRM"""
        try:
            # OSRM route API call
            url = f"{self.osrm_url}/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
            params = {
                'overview': 'full',  # Get all points 
                'geometries': 'geojson',
                'steps': 'true'
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data['code'] != 'Ok' or not data['routes']:
                raise ValueError(f"OSRM didn't find the route: {data}")
            
            route = data['routes'][0]
            geometry = route['geometry']['coordinates']
            
            # Converting [lon, lat] into [lat, lon]
            route_points = [(coord[1], coord[0]) for coord in geometry]
            
            return {
                'route_points': route_points,
                'distance_meters': route['distance'],
                'duration_seconds': route['duration'],
                'distance_km': route['distance'] / 1000,
                'duration_hours': route['duration'] / 3600
            }
            
        except requests.exceptions.RequestException as e:
            print(f"OSRM API error: {e}")
            raise RuntimeError(f"OSRM API failed: {e}")
        except Exception as e:
            print(f"Error in OSRM call: {e}")
            raise RuntimeError(f"OSRM routing failed: {e}")
    
    
    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Distance between 2 points in km"""
        R = 6371
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return 2 * R * math.asin(math.sqrt(a))
    
    def interpolate_route(self, start_lat: float, start_lon: float, 
                         end_lat: float, end_lon: float, 
                         total_minutes: int) -> List[Tuple[float, float]]:
        """Creating interpolated route with per-minute resolution"""
        route_points = []
        for minute in range(total_minutes + 1):
            ratio = minute / total_minutes if total_minutes > 0 else 0
            lat = start_lat + (end_lat - start_lat) * ratio
            lon = start_lon + (end_lon - start_lon) * ratio
            route_points.append((lat, lon))
        return route_points
    
    def sample_route_to_minutes(self, route_points: List[Tuple[float, float]], 
                               total_duration_minutes: int) -> List[Tuple[float, float]]:
        """Sample route to per-minute resolution"""
        if len(route_points) <= 1:
            return route_points
        
        # Linear distribution of minutes per route
        sampled_points = []
        for minute in range(total_duration_minutes + 1):
            ratio = minute / total_duration_minutes if total_duration_minutes > 0 else 0
            point_idx = int(ratio * (len(route_points) - 1))
            point_idx = min(point_idx, len(route_points) - 1)
            sampled_points.append(route_points[point_idx])
        
        return sampled_points
    
    def reverse_geocode_state(self, lat: float, lon: float) -> str:
        """Reverse geocoding of states using Nominatim API"""
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1,
                'zoom': 3 
            }
            headers = {
                'User-Agent': 'TruckSimulation/1.0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            address = data.get('address', {})
            
            # Try to find a state
            state = (address.get('state') or 
                    address.get('country_code', '').upper())
            
            # Map to US state codes
            state_mapping = {
                'california': 'CA', 'texas': 'TX', 'florida': 'FL',
                'new york': 'NY', 'pennsylvania': 'PA', 'illinois': 'IL',
                'georgia': 'GA', 'massachusetts': 'MA', 'washington': 'DC'
            }
            
            if state.lower() in state_mapping:
                return state_mapping[state.lower()]
            
            return state if state else 'UNKNOWN'
            
        except Exception as e:
            print(f"Nominatim error for {lat}, {lon}: {e}")
            return 'UNKNOWN'
    
    def generate_trajectory(self, start_metro: str, end_metro: str, 
                          avg_speed_kmh: float = None) -> Dict:
        """Generate one trajectory between two metro centers using configured router (Valhalla/OSRM)"""
        if avg_speed_kmh is None:
            avg_speed_kmh = random.uniform(70, 95)
        
        # Find metro region coordinates
        start_coords = None
        end_coords = None
        
        for metro in self.metros:
            if metro['name'] == start_metro:
                start_coords = (metro['lat'], metro['lon'])
            elif metro['name'] == end_metro:
                end_coords = (metro['lat'], metro['lon'])
        
        if not start_coords or not end_coords:
            raise ValueError(f"Metro region not found: {start_metro} or {end_metro}")
        
        # Get real route from configured router
        if self.router_type == "valhalla":
            route_data = self.get_valhalla_route(*start_coords, *end_coords)
        else:  # default to OSRM
            route_data = self.get_osrm_route(*start_coords, *end_coords)
        
        # Sample route to minutes
        total_minutes = int(route_data['duration_hours'] * 60)
        sampled_route = self.sample_route_to_minutes(
            route_data['route_points'], total_minutes
        )
        
        return {
            'start_metro': start_metro,
            'end_metro': end_metro,
            'distance_km': route_data['distance_km'],
            'duration_minutes': total_minutes,
            'avg_speed_kmh': avg_speed_kmh,
            'route_points': sampled_route
        }
    
    def get_random_metro_pair(self) -> Tuple[str, str]:
        """Get random pair of metro regions"""
        metros = [metro['name'] for metro in self.metros]
        start, end = random.sample(metros, 2)
        return start, end
    
    def get_all_metro_names(self) -> List[str]:
        """Get list of all metro regions"""
        return [metro['name'] for metro in self.metros]
    
    def batch_reverse_geocode(self, coordinates: List[Tuple[float, float]], 
                            delay: float = 1.0) -> List[str]:
        """Batch reverse geocoding with rate limiting"""
        states = []
        for i, (lat, lon) in enumerate(coordinates):
            if i > 0 and i % 10 == 0:
                print(f"Reverse geocoding progress: {i}/{len(coordinates)}")
                time.sleep(delay)  # Rate limiting
            
            state = self.reverse_geocode_state(lat, lon)
            states.append(state)
        
        return states
    
    def get_state_for_coordinates(self, lat: float, lon: float) -> str:
        """Get state for a single coordinate using spatial join"""
        if self.states_gdf is None:
            return 'UNKNOWN'
        
        point = Point(lon, lat)
        
        # Find which state contains this point
        for idx, row in self.states_gdf.iterrows():
            if row.geometry.contains(point):
                return row.get('STATE_NAME', 'UNKNOWN')
        
        return 'UNKNOWN'
    
    def batch_spatial_analysis(self, coordinates: List[Tuple[float, float]]) -> List[str]:
        """Batch spatial analysis for all coordinates using shapefile"""
        if self.states_gdf is None:
            return ['UNKNOWN'] * len(coordinates)
        
        states = []
        for lat, lon in coordinates:
            state = self.get_state_for_coordinates(lat, lon)
            states.append(state)
        
        return states
    
    def calculate_per_minute_speeds(self, trajectory: Dict) -> List[float]:
        """Calculate per-minute speeds for a trajectory"""
        route_points = trajectory['route_points']
        speeds = []
        
        for i in range(len(route_points) - 1):
            lat1, lon1 = route_points[i]
            lat2, lon2 = route_points[i + 1]
            
            # Haversine distance calculation
            R = 6371  # Earth radius in km
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            dlat, dlon = lat2 - lat1, lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            distance_km = 2 * R * math.asin(math.sqrt(a))
            
            # Speed in km/h (1 minute = 1/60 hour)
            speed_kmh = distance_km * 60
            speeds.append(speed_kmh)
        
        return speeds
    
    def calculate_rolling_mean_speeds(self, speeds: List[float], window: int = 5) -> List[float]:
        """Calculate rolling mean speeds with specified window"""
        if len(speeds) < window:
            return speeds
        
        rolling_means = []
        for i in range(len(speeds)):
            start_idx = max(0, i - window // 2)
            end_idx = min(len(speeds), i + window // 2 + 1)
            window_speeds = speeds[start_idx:end_idx]
            rolling_means.append(sum(window_speeds) / len(window_speeds))
        
        return rolling_means
