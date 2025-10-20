#!/usr/bin/env python3
"""
NASA SWOT Water Level Monitoring System
Retrieves SWOT satellite data and performs water resource analysis
"""

import os
import sys
from datetime import datetime
import yaml
from pathlib import Path

from swot_fetcher import SWOTDataFetcher
from analyzer import WaterLevelAnalyzer
from visualizer import SWOTVisualizer


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main execution function"""
    print(f"=== NASA SWOT Monitoring System ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Load configuration
        config = load_config()
        print(f"Configuration loaded")
        
        # Initialize modules
        fetcher = SWOTDataFetcher(config['data_sources'])
        analyzer = WaterLevelAnalyzer(config['analysis'])
        visualizer = SWOTVisualizer(config['visualization'])
        print(f"Modules initialized")
        
        # Fetch SWOT data
        print(f"\nFetching SWOT data from NASA...")
        data = fetcher.fetch_latest_data()
        if data is None or len(data) == 0:
            print("No new SWOT data available. Waiting for next overpass.")
            return
        print(f"Data fetched: {len(data)} observations")
        
        # Perform analysis
        print(f"\nPerforming water level analysis...")
        results = analyzer.analyze(data)
        print(f"Analysis complete")
        print(f"  - Water bodies tracked: {results['total_features']}")
        print(f"  - Mean elevation: {results['mean_elevation']:.2f} m")
        print(f"  - Elevation change: {results['elevation_change']:.2f} m")
        
        # Generate visualizations
        print(f"\nGenerating visualizations...")
        plots = visualizer.create_plots(data, results)
        print(f"Visualizations created: {len(plots)} plots")
        
        # Save results
        print(f"\nSaving results...")
        result_file = Path('results') / f"swot_analysis_{datetime.now().strftime('%Y%m%d')}.json"
        result_file.parent.mkdir(exist_ok=True)
        analyzer.save_results(results, result_file)
        print(f"Results saved to {result_file}")
        
        print(f"\n=== Analysis Complete ===")
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
