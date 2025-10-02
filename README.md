# Truck Simulation with Valhalla

A comprehensive simulation of 100 trucks traveling between 10 major US metro regions using real road routes via Valhalla API and state-level analysis through spatial join with US states GeoJSON.

## Project Overview

This project simulates truck movements across the United States, analyzing:
- **Real road routes** using Valhalla routing engine (preferred) or OSRM API (fallback)
- **Per-minute coordinates** for detailed trajectory analysis
- **State-level time analysis** using spatial join with US states GeoJSON
- **Speed and distance distributions** with comprehensive interactive visualizations

## Key Features

- **100 simulated truck trajectories** between 10 major US metro regions
- **Real road routing** via Valhalla API (preferred) or OSRM API (fallback)
- **Minute-resolution tracking** for precise analysis
- **State-level analysis** using spatial join with US states GeoJSON (all segments processed)
- **Interactive visualizations**: Plotly-based charts with hover tooltips and zoom functionality
- **Data export** with CSV files for trajectories, speeds, and state analysis
- **Quality validation** with correlation analysis and statistical checks
- **Advanced spatial analysis** with nearest-neighbor fallback for boundary cases

## Metro Regions

The simulation covers the 10 largest US metropolitan areas:

1. **New York** (NY) - 20.1M population
2. **Los Angeles** (CA) - 13.2M population  
3. **Chicago** (IL) - 9.5M population
4. **Dallas-Fort Worth** (TX) - 7.2M population
5. **Houston** (TX) - 7.0M population
6. **Washington DC** (DC) - 6.2M population
7. **Miami** (FL) - 6.1M population
8. **Philadelphia** (PA) - 6.0M population
9. **Atlanta** (GA) - 5.0M population
10. **Boston** (MA) - 4.9M population

## Technology Stack

### Core Technologies
- **Python 3.10+** - Main programming language
- **Valhalla API** - Modern routing engine (preferred)
- **OSRM API** - Open source routing (fallback)
- **GeoPandas** - Spatial data analysis and state assignment
- **Plotly** - Interactive data visualization
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations

### APIs Used
- **Valhalla** - Modern routing engine (primary)
- **OSRM** (`https://router.project-osrm.org`) - Open source routing (fallback)
- **US States GeoJSON** - Spatial boundaries for state assignment

## Project Structure

```
simulation_task/
├── README.md                    # This file
├── requirements.txt            # Python dependencies
├── data/
│   ├── metros.json             # Metro region definitions
│   ├── us_states.geojson       # US states boundaries
│   ├── trajectories/           # Generated simulation data
│   │   ├── trajectory_summary.csv
│   │   ├── state_minutes_full.csv
│   │   ├── per_minute_segments_with_state.csv
│   │   └── per_minute_speeds.csv
│   └── plots/                  # Interactive visualization outputs
│       ├── distance_histogram.html
│       ├── duration_histogram.html
│       ├── speed_histogram.html
│       ├── speed_histogram_rolling5.html
│       ├── state_minutes_histogram.html
│       ├── distance_vs_duration.html
│       ├── state_minutes_choropleth.html
│       └── state_avg_speed_choropleth.html
├── notebooks/
│   └── simulation_valhalla.ipynb        # Main simulation and analysis notebook
└── src/
    ├── __init__.py
    └── routing.py              # Valhalla/OSRM routing implementation
```

## Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment (recommended)
- Internet connection (for Valhalla/OSRM APIs)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Selma999/truck-simulation.git
   cd simulation_task
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Manual Package Installation

If you prefer to install packages individually or need specific versions:

```bash
# Core data science packages
pip install numpy>=1.21.0
pip install pandas>=1.3.0
pip install matplotlib>=3.4.0

# API and networking
pip install requests>=2.25.0

# Spatial analysis
pip install geopandas>=0.12.0
pip install shapely>=2.0.0

# Interactive visualizations
pip install plotly>=5.0.0

# Polyline decoding for Valhalla
pip install polyline>=2.0.0

# Jupyter environment
pip install jupyter>=1.0.0
pip install jupyterlab>=3.0.0
```

### Package Versions Used
- **Python**: 3.10+
- **NumPy**: 1.21.0+ (numerical computations)
- **Pandas**: 1.3.0+ (data manipulation)
- **GeoPandas**: 0.12.0+ (spatial analysis)
- **Shapely**: 2.0.0+ (geometric operations)
- **Plotly**: 5.0.0+ (interactive visualizations)
- **Polyline**: 2.0.0+ (Valhalla geometry decoding)
- **Requests**: 2.25.0+ (API calls for Valhalla/OSRM)
- **Jupyter**: 1.0.0+ (notebook environment)

### Detailed Installation Instructions

#### Option 1: Using pip (Recommended)
```bash
# Install all packages at once
pip install numpy pandas matplotlib requests jupyter jupyterlab

# Or install with specific versions
pip install numpy>=1.21.0 pandas>=1.3.0 matplotlib>=3.4.0 requests>=2.25.0 jupyter>=1.0.0 jupyterlab>=3.0.0
```

#### Option 2: Using conda (Alternative)
```bash
# Create conda environment
conda create -n truck-sim python=3.10

# Activate environment
conda activate truck-sim

# Install packages
conda install numpy pandas matplotlib requests jupyter jupyterlab
```

#### Option 3: Individual Package Installation
```bash
# Core numerical computing
pip install numpy

# Data manipulation and analysis
pip install pandas

# Data visualization
pip install matplotlib

# HTTP requests for APIs
pip install requests

# Jupyter notebook environment
pip install jupyter jupyterlab
```

#### Verification
After installation, verify all packages are working:
```python
# Test imports in Python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
print("All packages installed successfully!")
```

4. **Start Jupyter Lab**
   ```bash
   jupyter lab
   ```

5. **Run simulation**
   - Open `notebooks/simulation_valhalla.ipynb`
   - Execute all cells to generate 100 truck trajectories
   - View generated visualizations and data

## Generated Analysis

The simulation produces:

### Interactive Visualizations (HTML files in `data/plots/`)
1. **`distance_histogram.html`** - Distribution of trip distances (interactive)
2. **`duration_histogram.html`** - Distribution of trip durations (interactive)
3. **`distance_vs_duration.html`** - Correlation analysis scatter plot with hover tooltips
4. **`state_minutes_histogram.html`** - Time spent per US state (interactive)
5. **`speed_histogram.html`** - Per-minute speed distribution (interactive)
6. **`speed_histogram_rolling5.html`** - 5-minute rolling mean speed distribution
7. **`state_minutes_choropleth.html`** - Choropleth map of minutes per state
8. **`state_avg_speed_choropleth.html`** - Choropleth map of average speed per state

### Quality Analysis
- **Correlation analysis** - Distance vs Duration correlation (typically r > 0.8)
- **Statistical validation** - Realistic speed ranges (70-95 km/h)
- **Data quality checks** - Outlier detection and validation
- **Fallback monitoring** - OSRM vs Linear interpolation usage tracking

### Data Exports (CSV files in `data/trajectories/`)
- **`trajectory_summary.csv`** - High-level trajectory data (100 routes)
- **`state_minutes_full.csv`** - Per-truck state-level time analysis
- **`per_minute_segments_with_state.csv`** - All minute segments with state assignments
- **`per_minute_speeds.csv`** - Detailed speed measurements (all minute segments)

## Configuration

### Valhalla API Settings (Recommended)
```python
# Custom Valhalla server
routing = TruckRouting(
    valhalla_url="http://your-valhalla-server:8002",
    router_type="valhalla"
)
```

### OSRM API Settings (Fallback)
```python
# Default OSRM endpoint
routing = TruckRouting(
    osrm_url="https://router.project-osrm.org",
    router_type="osrm"
)
```

### Rate Limiting
- **Valhalla API**: No rate limits
- **OSRM API**: No rate limits (public service)

## Local Valhalla Deployment (Optional)

For production use or offline analysis:

```bash
# Start local Valhalla server
docker run -p 8002:8002 -v $(pwd)/valhalla:/data ghcr.io/valhalla/valhalla:latest

# Use local Valhalla in code
routing = TruckRouting(valhalla_url="http://localhost:8002", router_type="valhalla")
```

## Sample Results

### Typical Output
- **100 trajectories** with real road routes
- **~150,000 per-minute coordinates** 
- **Distance range**: 200-4,000 km
- **Duration range**: 3-50 hours
- **Speed analysis**: Per-minute calculations
- **State coverage**: All 50 US states

### Performance
- **Generation time**: ~3-5 minutes for 100 trajectories (Valhalla)
- **API calls**: ~100 Valhalla requests (no rate limiting)
- **Data size**: ~3MB CSV files + interactive HTML visualizations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

**Valhalla API errors**
- Check network connection to Valhalla server
- Verify Valhalla endpoint availability
- Use OSRM fallback if needed

**OSRM API errors (fallback)**
- Check internet connection
- Verify API endpoint availability
- Consider rate limiting

**Import errors**
- Verify virtual environment is activated
- Check Python path configuration
- Install missing dependencies

### Support
For issues and questions, please open a GitHub issue with:
- Error messages
- System information
- Steps to reproduce

## References

- [Valhalla Documentation](https://github.com/valhalla/valhalla)
- [OSRM Documentation](http://project-osrm.org/)
- [GeoPandas Documentation](https://geopandas.org/)
- [Plotly Documentation](https://plotly.com/python/)
- [US States GeoJSON](https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json)

---

