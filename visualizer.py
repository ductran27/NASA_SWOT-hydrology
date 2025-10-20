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
        """Create global spatial distribution map with continents"""
        fig = plt.figure(figsize=(18, 10))
        ax = fig.add_subplot(111)
        
        # Set global extent
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.set_aspect('equal')
        
        # Set ocean background
        ax.set_facecolor('#E8F4F8')
        fig.patch.set_facecolor('white')
        
        # Draw simple continent outlines (simplified approach)
        # Draw land masses with basic shapes
        continents = [
            # North America
            [(-170, 25), (-170, 70), (-50, 70), (-50, 25), (-170, 25)],
            # South America
            [(-80, -55), (-80, 12), (-35, 12), (-35, -55), (-80, -55)],
            # Europe
            [(-10, 35), (-10, 70), (40, 70), (40, 35), (-10, 35)],
            # Africa
            [(-20, -35), (-20, 35), (50, 35), (50, -35), (-20, -35)],
            # Asia
            [(40, 0), (40, 75), (180, 75), (180, 0), (40, 0)],
            # Australia
            [(110, -45), (110, -10), (155, -10), (155, -45), (110, -45)],
        ]
        
        for continent in continents:
            lons, lats = zip(*continent)
            ax.fill(lons, lats, color='#D3D3D3', alpha=0.3, edgecolor='#999999', linewidth=1)
        
        # Plot water body observations
        scatter = ax.scatter(df['longitude'], df['latitude'], 
                           c=df['water_elevation_m'], 
                           s=df['water_area_km2']*3,  # Size by area
                           cmap='YlGnBu', alpha=0.8, edgecolors='darkblue', 
                           linewidth=0.8, zorder=5)
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax, label='Water Elevation (m)', 
                           fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=10)
        
        # Add gridlines
        ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5, color='gray')
        
        # Set major gridlines
        ax.set_xticks(np.arange(-180, 181, 30))
        ax.set_yticks(np.arange(-90, 91, 30))
        
        # Labels and title
        ax.set_xlabel('Longitude (°E)', fontsize=13, fontweight='bold')
        ax.set_ylabel('Latitude (°N)', fontsize=13, fontweight='bold')
        ax.set_title('Global SWOT Water Body Observations', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Add info box
        info_text = f"Total Observations: {len(df)}\n"
        info_text += f"Total Water Area: {results['total_water_area_km2']:.1f} km²\n"
        info_text += f"Mean Elevation: {results['mean_elevation']:.1f} m"
        ax.text(0.02, 0.02, info_text, transform=ax.transAxes, 
                fontsize=11, verticalalignment='bottom',
                bbox=dict(boxstyle='round', facecolor='white', 
                         edgecolor='darkblue', alpha=0.9, linewidth=2))
        
        # Add legend for point sizes
        sizes = [10, 50, 100]
        labels = ['Small', 'Medium', 'Large']
        legend_points = [plt.scatter([], [], s=s*3, c='steelblue', alpha=0.6, 
                                    edgecolors='darkblue', linewidth=0.8) 
                        for s in sizes]
        legend = ax.legend(legend_points, labels, scatterpoints=1, 
                          title='Water Body Size', loc='upper right',
                          frameon=True, fancybox=True, shadow=True,
                          fontsize=10, title_fontsize=11)
        legend.get_frame().set_alpha(0.9)
        
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
