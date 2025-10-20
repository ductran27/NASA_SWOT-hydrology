"""
SWOT Visualizer Module
Creates visualizations for SWOT satellite observations
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from pathlib import Path


class SWOTVisualizer:
    """Create visualizations for SWOT data"""
    
    def __init__(self, config):
        """Initialize visualizer with configuration"""
        self.config = config
        self.plots_dir = Path('plots')
        self.plots_dir.mkdir(exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def create_plots(self, df, results):
        """
        Create all visualizations
        
        Args:
            df: pandas.DataFrame with SWOT data
            results: dict with analysis results
        
        Returns:
            list: Paths to created plot files
        """
        plots = []
        
        # Filter good quality data
        good_data = df[df['quality_flag'] == 'good'].copy()
        
        # Elevation distribution
        plots.append(self._plot_elevation_distribution(good_data, results))
        
        # Spatial map
        plots.append(self._plot_spatial_map(good_data, results))
        
        # Water area analysis
        plots.append(self._plot_water_area(good_data, results))
        
        return plots
    
    def _plot_elevation_distribution(self, df, results):
        """Create elevation distribution plot"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        ax1.hist(df['water_elevation_m'], bins=20, edgecolor='black', alpha=0.7, color='steelblue')
        ax1.axvline(results['mean_elevation'], color='red', linestyle='--', linewidth=2, 
                   label=f"Mean: {results['mean_elevation']:.1f} m")
        ax1.set_xlabel('Water Elevation (m)', fontsize=11)
        ax1.set_ylabel('Frequency', fontsize=11)
        ax1.set_title('Water Elevation Distribution', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Box plot with uncertainty
        ax2.boxplot(df['water_elevation_m'], vert=True)
        ax2.set_ylabel('Water Elevation (m)', fontsize=11)
        ax2.set_title('Elevation Variability', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Add stats text
        stats_text = f"Range: {results['min_elevation']:.1f} - {results['max_elevation']:.1f} m\n"
        stats_text += f"Std Dev: {results['std_elevation']:.1f} m\n"
        stats_text += f"Features: {results['good_quality_features']}"
        ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        # Save
        timestamp = pd.Timestamp.now().strftime('%Y%m%d')
        filepath = self.plots_dir / f'elevation_dist_{timestamp}.png'
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def _plot_spatial_map(self, df, results):
        """Create spatial distribution map"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Color by elevation
        scatter = ax.scatter(df['longitude'], df['latitude'], 
                           c=df['water_elevation_m'], 
                           s=df['water_area_km2']*2,  # Size by area
                           cmap='viridis', alpha=0.6, edgecolors='black', linewidth=0.5)
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax, label='Water Elevation (m)')
        
        # Labels and title
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.set_title('SWOT Water Body Observations', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add centroid marker
        centroid = results['spatial_stats']
        ax.plot(centroid['centroid_lon'], centroid['centroid_lat'], 
               'r*', markersize=15, label='Centroid')
        ax.legend()
        
        # Add info text
        info_text = f"Observations: {len(df)}\n"
        info_text += f"Total Area: {results['total_water_area_km2']:.1f} km²"
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        plt.tight_layout()
        
        # Save
        timestamp = pd.Timestamp.now().strftime('%Y%m%d')
        filepath = self.plots_dir / f'spatial_map_{timestamp}.png'
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def _plot_water_area(self, df, results):
        """Create water area analysis plot"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Area distribution
        ax1.hist(df['water_area_km2'], bins=20, edgecolor='black', alpha=0.7, color='teal')
        ax1.set_xlabel('Water Area (km²)', fontsize=11)
        ax1.set_ylabel('Frequency', fontsize=11)
        ax1.set_title('Water Body Size Distribution', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Area vs Elevation scatter
        ax2.scatter(df['water_area_km2'], df['water_elevation_m'], 
                   alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
        ax2.set_xlabel('Water Area (km²)', fontsize=11)
        ax2.set_ylabel('Water Elevation (m)', fontsize=11)
        ax2.set_title('Area vs Elevation Relationship', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save
        timestamp = pd.Timestamp.now().strftime('%Y%m%d')
        filepath = self.plots_dir / f'water_area_{timestamp}.png'
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
