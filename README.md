# NASA SWOT Water Level Monitoring

Automated system for retrieving and analyzing NASA SWOT satellite data for surface water monitoring. Tracks water elevation changes, lake levels, and river discharge measurements from space.

## Overview

This project monitors surface water using NASA's SWOT satellite mission data. It retrieves daily observations, analyzes water level changes, and generates visualizations showing temporal trends in water resources.

## Data Source

NASA SWOT Mission via Earthdata API:
- Surface water elevation measurements
- Lake and reservoir level data
- River discharge estimates
- Global coverage with ~21-day repeat cycle

## Setup

Install required Python packages:
```bash
pip install -r requirements.txt
```

NASA Earthdata credentials required:
1. Register at https://urs.earthdata.nasa.gov/
2. Create `.env` file with credentials:
```
EARTHDATA_USERNAME=your_username
EARTHDATA_PASSWORD=your_password
```

Run analysis:
```bash
python main.py
```

## Features

The system performs:
- Automated SWOT data retrieval from NASA
- Water elevation change detection
- Statistical trend analysis
- Time series visualization
- Spatial mapping of water bodies

## Automated Updates

GitHub Actions workflow runs daily to:
- Check for new SWOT data
- Download latest observations
- Update analysis and plots
- Commit results automatically

## Project Structure

```
.
├── main.py              - Main script
├── swot_fetcher.py      - NASA data retrieval
├── analyzer.py          - Analysis and statistics
├── visualizer.py        - Plot generation
├── config.yaml          - Configuration
├── requirements.txt     - Dependencies
└── .github/workflows/   - Automation schedule
```

## Output

Generated files:
- `data/` - Raw SWOT observations
- `results/` - Analysis JSON files
- `plots/` - Visualization images
- `maps/` - Spatial distribution maps

## Notes

Uses NASA Earthdata API for legitimate research purposes. All data is publicly available. Analysis code is original work focused on water resource monitoring.
