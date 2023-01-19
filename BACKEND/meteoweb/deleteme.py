# import pandas as pd
# import cloupy as cp
# import numpy as np
from dotenv import load_dotenv as env
import os

env()
# # Spline interpolation method (cubic method)
# df = pd.read_csv('C:\CODES\MeteoWeb\data.csv')
# imap = cp.m_MapInterpolation(shapefile_path=os.getenv('bounds'), dataframe=df, crs='epsg:4326')
# imap.draw(
# levels=np.arange(-2, 16, 0.5), # (start, end, step),
# zoom_in=[(-102.2, -99.6), (19.87, 21.9)],
# # cbar_ticks=[-10, -5, 0, 5, 10, 16],
# # show_points=True,
# interpolation_method='cubic',
# cbar_title='Temperatura Mínima (°C)',
# title='Pronóstico meteorológico para el estado de Guanajuato\n18 de enero, 2023.',
# title_ha='center',
# title_x_position=0.5,
# save='map_cubic.png'
# )
# help(cp.m_MapInterpolation.draw)


# # Kriging interpolation method
import numpy as np
import pandas as pd
import geopandas as gpd
from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
import matplotlib as mpl

slp = gpd.read_file(os.getenv('bg'))
gto = gpd.read_file(os.getenv('state'))
df = pd.read_csv(r'C:\CODES\MeteoWeb\data.csv')
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat']))

# Data vectors
lons = np.array(df['lon'])
lats = np.array(df['lat'])
vals = np.array(df['z_value'])

# Grid configuration
grid_space = 0.01
# Longitude interval
xmin_grid = np.amin(lons)
xmax_grid = np.amax(lons)
grid_lon = np.arange(xmin_grid, xmax_grid,grid_space)
# Latitude interval
ymin_grid = np.amin(lats)
ymax_grid = np.amax(lats)
grid_lat = np.arange(ymin_grid, ymax_grid, grid_space)

# Interpolating Data
ok = OrdinaryKriging(lons, lats, vals, variogram_model='gaussian', enable_plotting=False, nlags=20, verbose=False)
z1, ssi = ok.execute('grid', grid_lon, grid_lat)    # z1 has the interpolated values within the grid

# Contours generation in base interpolated values (z1)
xintrp, yintrp = np.meshgrid(grid_lon, grid_lat)    # Generate a meshgrid
fig, ax = plt.subplots(figsize=(10, 15))    # ax is the plot base area. Multi-plotting.
contour = plt.contourf(xintrp, yintrp, z1, len(z1), cmap=mpl.colormaps['seismic'])  # Third argument represents contours number

# Plotting state bound and display components 
slp.plot(ax = ax, color = 'black', linewidth = 0.5)
gto.plot(ax = ax, color = 'black')

# Styling the map
minVal = round(np.amin(z1))
maxVal = round(np.amax(z1))
midVal = round(np.mean(z1))
plt.colorbar(contour, ticks = [minVal, 0, maxVal, midVal])
plt.title('Temperatura Mínima (°C)\nPronostico para el día 18/01/2023')
plt.axis([np.amin(xintrp), np.amax(xintrp), np.amin(yintrp), np.amax(yintrp)])

# Save image
# plt.savefig('figurename.png',dpi=300,bbox_inches='tight')

plt.show()