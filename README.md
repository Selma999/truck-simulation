# Truck Simulation with OSRM

A comprehensive simulation of 100 trucks traveling between 10 major US metro regions using real road routes via OSRM API and state-level analysis through Nominatim geocoding.

## Project Overview

This project simulates truck movements across the United States, analyzing:
- **Real road routes** using OSRM (Open Source Routing Machine) API
- **Per-minute coordinates** for detailed trajectory analysis
- **State-level time analysis** using Nominatim reverse geocoding
- **Speed and distance distributions** with comprehensive visualizations

## Key Features

- **100 simulated truck trajectories** between 10 major US metro regions
- **Real road routing** via OSRM API (not linear interpolation)
- **Minute-resolution tracking** for precise analysis
- **State-level geocoding** using Nominatim API
- **Comprehensive visualizations**: histograms, scatter plots, speed analysis
- **Export capabilities** for further analysis

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
- **OSRM API** - Real road routing and navigation
- **Nominatim API** - Reverse geocoding for state identification
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Data visualization
- **NumPy** - Numerical computations

### APIs Used
- **OSRM** (`https://router.project-osrm.org`) - Open source routing
- **Nominatim** (`https://nominatim.openstreetmap.org`) - OpenStreetMap geocoding

## Project Structure

```
simulation_task/
├── README.md                    # This file
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # OSRM deployment (optional)
├── data/
│   ├── metros.json             # Metro region definitions
│   └── trajectories/           # Generated simulation data
│       ├── trajectory_summary.csv
│       ├── state_minutes.csv
│       └── per_minute_speeds.csv
├── notebooks/
│   ├── simulation.ipynb       # Main simulation notebook
│   └── analysis.ipynb          # Data analysis notebook
└── src/
    ├── routing.py              # Linear interpolation (fallback)
    ├── routing_osrm_api.py     # OSRM API implementation
    └── routing_linear_fallback.py
```

## Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment (recommended)
- Internet connection (for OSRM and Nominatim APIs)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
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

# Jupyter environment
pip install jupyter>=1.0.0
pip install jupyterlab>=3.0.0
```

### Package Versions Used
- **Python**: 3.10+
- **NumPy**: 1.21.0+ (numerical computations)
- **Pandas**: 1.3.0+ (data manipulation)
- **Matplotlib**: 3.4.0+ (visualization)
- **Requests**: 2.25.0+ (API calls for OSRM and Nominatim)
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
   - Open `notebooks/simulation.ipynb`
   - Execute all cells to generate 100 truck trajectories
   - View generated visualizations and data

## Generated Analysis

The simulation produces:

### Visualizations
1. **Distance Histogram** - Distribution of trip distances
2. **Duration Histogram** - Distribution of trip durations  
3. **Distance vs Duration Scatter Plot** - Correlation analysis
4. **State Minutes Histogram** - Time spent per US state
5. **Speed Histogram** - Per-minute speed distribution

### Data Exports
- **trajectory_summary.csv** - High-level trajectory data
- **state_minutes.csv** - State-level time analysis
- **per_minute_speeds.csv** - Detailed speed measurements

## Configuration

### OSRM API Settings
```python
# Default OSRM endpoint
osrm_url = "https://router.project-osrm.org"

# For local OSRM deployment
osrm_url = "http://localhost:5000"
```

### Rate Limiting
- **OSRM API**: No rate limits (public service)
- **Nominatim API**: 1 request/second (with User-Agent header)

## Local OSRM Deployment (Optional)

For production use or offline analysis:

```bash
# Start local OSRM server
docker-compose up osrm-backend-small -d

# Use local OSRM in code
routing = TruckRouting(osrm_url="http://localhost:5001")
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
- **Generation time**: ~5-10 minutes for 100 trajectories
- **API calls**: ~100 OSRM + ~1,000 Nominatim requests
- **Data size**: ~2.5MB CSV files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Troubleshooting

### Common Issues

**OSRM API errors**
- Check internet connection
- Verify API endpoint availability
- Consider rate limiting

**Nominatim 403 errors**
- Ensure User-Agent header is set
- Implement proper rate limiting (1 req/sec)
- Use fallback geocoding if needed

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

- [OSRM Documentation](http://project-osrm.org/)
- [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)
- [OpenStreetMap](https://www.openstreetmap.org/)

---

