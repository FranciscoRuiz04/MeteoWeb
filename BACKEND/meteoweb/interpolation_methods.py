from pykrige.ok import OrdinaryKriging
from pykrige.uk import UniversalKriging
from pyidw import idw



class OK(OrdinaryKriging):
    def __init__(self, x, y, z, variogram_model="linear", variogram_parameters=None, variogram_function=None, nlags=20, weight=False, anisotropy_scaling=1, anisotropy_angle=0, verbose=False, enable_plotting=False, enable_statistics=False, coordinates_type="euclidean", exact_values=True, pseudo_inv=False, pseudo_inv_type="pinv"):
        super().__init__(x, y, z, variogram_model, variogram_parameters, variogram_function, nlags, weight, anisotropy_scaling, anisotropy_angle, verbose, enable_plotting, enable_statistics, coordinates_type, exact_values, pseudo_inv, pseudo_inv_type)
    
    def interpolateValues(self, grid_lon, grid_lat, style='grid', mask=None, backend="vectorized", n_closest_points=None):
        z1, ssi = super().execute(style, grid_lon, grid_lat, mask, backend, n_closest_points)
        return z1, ssi



class UK(UniversalKriging):
    def __init__(self, lons, lats, vals, variogram_model="linear", variogram_parameters=None, variogram_function=None, nlags=6, weight=False, anisotropy_scaling=1, anisotropy_angle=0, drift_terms=None, point_drift=None, external_drift=None, external_drift_x=None, external_drift_y=None, specified_drift=None, functional_drift=None, verbose=False, enable_plotting=False, exact_values=True, pseudo_inv=False, pseudo_inv_type="pinv"):
        super().__init__(lons, lats, vals, variogram_model, variogram_parameters, variogram_function, nlags, weight, anisotropy_scaling, anisotropy_angle, drift_terms, point_drift, external_drift, external_drift_x, external_drift_y, specified_drift, functional_drift, verbose, enable_plotting, exact_values, pseudo_inv, pseudo_inv_type)

    def interpolateValues(self, grid_lon, grid_lat, style='grid', mask=None, backend="vectorized", n_closest_points=None):
        z1, ssi = super().execute(style, grid_lon, grid_lat, mask, backend, n_closest_points)
        return z1, ssi



class IDW:
    def __init__(self, input_shp, delimitation_shp, colname="z_value", resolution=450):
         idw.idw_interpolation(
             input_point_shapefile=input_shp,
            extent_shapefile=delimitation_shp,
            column_name=colname,
            output_resolution=resolution,
            )