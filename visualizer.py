"""
SWOT Visualizer Module
Creates visualizations for SWOT satellite observations
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from pathlib import Path
import cartopy.crs as ccrs
import cartopy.feature as cfeature


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
        """Create global spatial distribution map with proper coastlines and boundaries"""
        # Create figure with Plate Carree projection
        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
        
        # Set global extent
        ax.set_global()
        
        # Add geographic features
        ax.add_feature(cfeature.LAND, facecolor='#F5F5DC', alpha=0.3)
        ax.add_feature(cfeature.OCEAN, facecolor='#E8F4F8')
        ax.add_feature(cfeature.COASTLINE, linewidth=0.8, edgecolor='#333333')
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='#666666', linestyle='--', alpha=0.7)
        ax.add_feature(cfeature.LAKES, facecolor='#B3D9FF', alpha=0.5, edgecolor='#4D94FF', linewidth=0.3)
        ax.add_feature(cfeature.RIVERS, edgecolor='#4D94FF', linewidth=0.3, alpha=0.5)
        
        # Add gridlines with labels
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', 
                         alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 11}
        gl.ylabel_style = {'size': 11}
        
        # Plot water body observations
        scatter = ax.scatter(df['longitude'], df['latitude'], 
                           c=df['water_elevation_m'], 
                           s=df['water_area_km2']*4,  # Size by area
                           cmap='YlGnBu', alpha=0.8, edgecolors='navy', 
                           linewidth=1, zorder=5, transform=ccrs.PlateCarree())
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax, label='Water Elevation (m)', 
                           fraction=0.03, pad=0.04, shrink=0.8)
        cbar.ax.tick_params(labelsize=11)
        
        # Title
        ax.set_title('Global SWOT Water Body Observations\nNASA Surface Water and Ocean Topography Mission', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Add info box
        info_text = f"Total Observations: {len(df)}\n"
        info_text += f"Total Water Area: {results['total_water_area_km2']:.1f} km²\n"
        info_text += f"Mean Elevation: {results['mean_elevation']:.1f} m\n"
        info_text += f"Elevation Range: {results['min_elevation']:.1f} - {results['max_elevation']:.1f} m"
        ax.text(0.02, 0.02, info_text, transform=ax.transAxes, 
                fontsize=11, verticalalignment='bottom',
                bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                         edgecolor='navy', alpha=0.95, linewidth=2.5))
        
        # Add legend for point sizes
        sizes = [10, 50, 100]
        labels = ['Small (<10 km²)', 'Medium (10-50 km²)', 'Large (>50 km²)']
        legend_points = [plt.scatter([], [], s=s*4, c='steelblue', alpha=0.7, 
                                    edgecolors='navy', linewidth=1) 
                        for s in sizes]
        legend = ax.legend(legend_points, labels, scatterpoints=1, 
                          title='Water Body Size', loc='upper right',
                          frameon=True, fancybox=True, shadow=True,
                          fontsize=10, title_fontsize=11)
        legend.get_frame().set_alpha(0.95)
        legend.get_frame().set_edgecolor('navy')
        legend.get_frame().set_linewidth(2)
        
        plt.tight_layout()
        
        # Save
        timestamp = pd.Timestamp.now().strftime('%Y%m%d')
        filepath = self.plots_dir / f'spatial_map_{timestamp}.png'
        plt.savefig(filepath, dpi=200, bbox_inches='tight', facecolor='white')
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
