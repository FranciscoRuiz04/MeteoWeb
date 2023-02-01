import cloupy as cp
import numpy as np
import geopandas as gpd
from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
import matplotlib as mpl

def spline(data, shp_path, date, **kargs):
    minVal = data['z_value'].min()
    maxVal = data['z_value'].max()
    
    if 'crs' not in kargs.keys():
        kargs['crs'] = 'epsg:4326'

    imap = cp.m_MapInterpolation(shapefile_path=shp_path, dataframe=data, **kargs)
    imap.draw(levels=np.arange(minVal, maxVal + 1, 0.1),
                zoom_in=[(-102.2, -99.6), (19.87, 21.9)],
                interpolation_method='cubic',
                cbar_title='Temperatura Mínima (°C)',
                title=f'Pronóstico para el día {date}',
                title_ha='center',
                title_x_position=0.5,
                cmap='seismic',
                save='map_Map.png'
                )


class Kriging(OrdinaryKriging):
    def __init__(self, df, grid_space=0.01, variogram_model="linear", variogram_parameters=None, variogram_function=None, nlags=20, weight=False, anisotropy_scaling=1, anisotropy_angle=0, verbose=False, enable_plotting=False, enable_statistics=False, coordinates_type="euclidean", exact_values=True, pseudo_inv=False, pseudo_inv_type="pinv"):
        
        self.data = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat']))
        
        # Data vectors
        lons = np.array(self.data['lon'])
        lats = np.array(self.data['lat'])
        vals = np.array(self.data['z_value'])
        
        # Grid configuration
        # Longitude interval
        xmin_grid = np.amin(lons)
        xmax_grid = np.amax(lons)
        self.grid_lon = np.arange(xmin_grid, xmax_grid, grid_space)
        # Latitude interval
        ymin_grid = np.amin(lats)
        ymax_grid = np.amax(lats)
        self.grid_lat = np.arange(ymin_grid, ymax_grid, grid_space)
        
        super().__init__(lons, lats, vals, variogram_model, variogram_parameters, variogram_function, nlags, weight, anisotropy_scaling, anisotropy_angle, verbose, enable_plotting, enable_statistics, coordinates_type, exact_values, pseudo_inv, pseudo_inv_type)
    
    
    def interpolateValues(self, style='grid', mask=None, backend="vectorized", n_closest_points=None):
        self.z1, self.ssi = super().execute(style, self.grid_lon, self.grid_lat, mask, backend, n_closest_points)
    
    
    def genMap(self, shp_path, cramp='seismic', shp_contour_col='black', labelBar=None, bshp_path=None, save_path=None, ncontours=None, bshp_contour_col=None, title=None, suptitle=None, barlab=None):
        
        shp = gpd.read_file(shp_path)
        # Contours generation in base interpolated values (z1)
        xintrp, yintrp = np.meshgrid(self.grid_lon, self.grid_lat)    # Generate a meshgrid
        fig, ax = plt.subplots()    # ax is the plot base area. Multi-plotting.
        
        self.interpolateValues()
        
        if ncontours == None:
            ncontours = len(self.z1)
        
        contour = plt.contourf(xintrp, yintrp, self.z1, ncontours, cmap=mpl.colormaps[cramp])  # Fourth argument represents contours number
        
        shp.plot(ax = ax, color = shp_contour_col)
        
        # Plotting state bound and display components
        if bshp_path != None:
            bshp = gpd.read_file(bshp_path)
            
            if bshp_contour_col == None:
                bshp_contour_col = 'black'
            
            bshp.plot(ax = ax, color = bshp_contour_col, linewidth = 0.5)
        
        # Styling the map
        minVal = round(np.amin(self.z1))
        maxVal = round(np.amax(self.z1))    
        # midVal = round(np.mean(self.z1))
        plt.colorbar(contour, label= labelBar, ticks=range(minVal, maxVal + 1, 2))
        plt.clim(minVal, maxVal)
        plt.xlabel('Longitud', fontsize=10)
        plt.ylabel('Latitud', fontsize=10)
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9, ticks=[20, 20.5, 21, 21.5], labels=[20.0, 20.5, 21.0, 20.5])
        plt.annotate('Fuente: meteoblue.com. Mapa Base: Marco Geoestadístico 2020. INEGI. EPSG:4326', ha='left', va='center', xy=(0,-.15), xycoords='axes fraction', fontsize=7)
        
        if suptitle != None:
            fig.suptitle(suptitle, fontsize=10)
        if title != None:
            plt.title(title, fontsize=11, ha='center')
        
        # Zoom in to wanted area
        plt.axis([np.amin(xintrp), np.amax(xintrp), np.amin(yintrp), np.amax(yintrp)])
        
        # Save image
        if save_path != None:
            plt.savefig(save_path, dpi=300,bbox_inches='tight')
        else:
            plt.show()

if __name__ == '__main__':
    import os
    import pandas as pd
    from dotenv import load_dotenv as env
    env()
    ini = Kriging(pd.read_csv(r'C:\CODES\MeteoWeb\data20.csv'))
    ini.genMap(os.getenv('state'), bshp_path=os.getenv('bg'), title='Pronóstico Meteorológico para el día 2023-01-20\nTemperatura Mínima', cramp='winter_r')