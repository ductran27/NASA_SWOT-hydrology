# Setup Guide for NASA SWOT Monitoring

Simple instructions to get your NASA SWOT satellite monitoring running automatically.

## What This Does

Monitors NASA SWOT satellite data for surface water observations. Analyzes water elevations, lake levels, and generates spatial maps showing water resources from space.

## Quick Setup

### 1. Test Locally First

```bash
cd nasa-swot-monitor
pip install -r requirements.txt
python main.py
```

The system works without NASA credentials - it generates sample data for demonstration. To use real NASA data, you'll need Earthdata credentials (optional).

### 2. Push to GitHub

```bash
cd nasa-swot-monitor
git init
git add .
git commit -m "Initial commit: NASA SWOT monitoring"

# Create new public repo on GitHub named 'swot-water-monitor'
git remote add origin https://github.com/YOUR_USERNAME/swot-water-monitor.git
git branch -M main
git push -u origin main
```

### 3. Automatic Daily Updates

Once pushed, GitHub Actions runs automatically every day at 10 AM UTC to:
- Generate new SWOT-like observations
- Analyze water elevation patterns
- Create spatial maps
- Commit results automatically

## Optional: Real NASA Data

To use actual NASA SWOT data:

1. Register at https://urs.earthdata.nasa.gov/
2. In your GitHub repository, go to Settings > Secrets > Actions
3. Add two secrets:
   - `EARTHDATA_USERNAME`: your NASA username
   - `EARTHDATA_PASSWORD`: your NASA password
4. Update swot_fetcher.py to use real NASA API calls

The system works fine without credentials using simulated data.

## What Gets Committed Daily

- Water elevation analysis (JSON)
- Spatial distribution maps (PNG)
- Elevation distribution plots (PNG)
- Water area analysis (PNG)

## Files Included

- `main.py` - Main script
- `swot_fetcher.py` - Data retrieval
- `analyzer.py` - Statistical analysis  
- `visualizer.py` - Map and plot generation
- `config.yaml` - Configuration
- `.github/workflows/` - Daily automation

## Notes

- Uses simulated SWOT-like data by default (no credentials needed)
- Runs completely automatically once pushed to GitHub
- PUBLIC repository recommended (unlimited free Actions)
- Generates professional remote sensing visualizations
- Shows consistent GitHub activity

This is a research/educational tool for water resource monitoring.
