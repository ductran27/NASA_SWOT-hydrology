"""
Water Level Analyzer Module
Performs analysis on SWOT satellite observations
"""

import pandas as pd
import numpy as np
from scipy import stats
import json
from pathlib import Path


class WaterLevelAnalyzer:
    """Analyze SWOT water level observations"""
    
    def __init__(self, config):
        """Initialize analyzer with configuration"""
        self.config = config
        self.results_dir = Path('results')
        self.results_dir.mkdir(exist_ok=True)
    
    def analyze(self, df):
        """
        Perform comprehensive analysis on SWOT data
        
        Args:
            df: pandas.DataFrame with SWOT observations
        
        Returns:
            dict: Analysis results
        """
        results = {}
        
        # Filter good quality data
        good_data = df[df['quality_flag'] == 'good'].copy()
        
        # Basic statistics
        results['total_features'] = len(df)
        results['good_quality_features'] = len(good_data)
        results['mean_elevation'] = float(good_data['water_elevation_m'].mean())
        results['median_elevation'] = float(good_data['water_elevation_m'].median())
        results['std_elevation'] = float(good_data['water_elevation_m'].std())
        results['min_elevation'] = float(good_data['water_elevation_m'].min())
        results['max_elevation'] = float(good_data['water_elevation_m'].max())
        
        # Total water area
        results['total_water_area_km2'] = float(good_data['water_area_km2'].sum())
        
        # Elevation change analysis
        results['elevation_change'] = self._calculate_elevation_change(good_data)
        
        # Spatial distribution
        results['spatial_stats'] = self._analyze_spatial_distribution(good_data)
        
        # Quality assessment
        results['quality_distribution'] = df['quality_flag'].value_counts().to_dict()
        
        # Uncertainty statistics
        results['mean_uncertainty'] = float(good_data['elevation_uncertainty_m'].mean())
        
        # Summary message
        results['summary'] = self._generate_summary(results)
        
        # Metadata
        results['analysis_date'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        results['observation_count'] = len(df)
        
        return results
    
    def _calculate_elevation_change(self, df):
        """Calculate elevation change metrics"""
        # For first run, we don't have historical data
        # In production, this would compare with previous observations
        
        # Simulate change by comparing high vs low elevation areas
        high_elev = df[df['water_elevation_m'] > df['water_elevation_m'].median()]
        low_elev = df[df['water_elevation_m'] <= df['water_elevation_m'].median()]
        
        change = float(high_elev['water_elevation_m'].mean() - low_elev['water_elevation_m'].mean())
        
        return change
    
    def _analyze_spatial_distribution(self, df):
        """Analyze spatial distribution of observations"""
        return {
            'longitude_range': [float(df['longitude'].min()), float(df['longitude'].max())],
            'latitude_range': [float(df['latitude'].min()), float(df['latitude'].max())],
            'centroid_lon': float(df['longitude'].mean()),
            'centroid_lat': float(df['latitude'].mean())
        }
    
    def _generate_summary(self, results):
        """Generate human-readable summary"""
        mean_elev = results['mean_elevation']
        n_features = results['good_quality_features']
        total_area = results['total_water_area_km2']
        
        summary = f"Tracked {n_features} water bodies (avg elevation: {mean_elev:.1f} m, total area: {total_area:.1f} km²)"
        
        return summary
    
    def save_results(self, results, filepath):
        """Save analysis results to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
