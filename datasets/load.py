import os
from .models import Dataset, MeasurementFile

from django.contrib.gis.geos import GEOSGeometry


def run(verbose=True):
    pass
    # TODO
    # for f in files:
    #     shp = read_caliop_met_file(f)
    #     mf = MeasurementFile(spatial_extent=shp.wkt)
    # d = Dataset()
    # d.save()


def read_caliop_met_file(filepath):
    import numpy as np
    from shapely.geometry import LineString, Polygon, MultiPoint
    vals = {}
    _in = ''

    with open(filepath) as f:

        for line in f:
            print(line)
            if len(line.split('=')) > 1:
                key, val = line.split('=')
                key = key.strip()
                val = val.strip()
                if key == 'OBJECT' and val == 'GRINGLATITUDE':
                    _in = 'latitude'
                elif key == 'END_OBJECT' and val == 'GRINGLATITUDE':
                    _in = ''
                if key == 'OBJECT' and val == 'GRINGLONGITUDE':
                    _in = 'longitude'
                elif key == 'END_OBJECT' and val == 'GRINGLONGITUDE':
                    _in = ''

                if _in and key == 'VALUE':
                    vals[_in] = val.strip('(').strip(')').split(',')

    ndarr = np.array([vals['longitude'], vals['latitude']], dtype=np.float).T

    # TODO: There is an issue here when reading points which cross the dateline. A quick google suggests that I should
    #  define an offset projection to define the data in (so it's all on one 360 degree domain), then transform it.
    # This is useful for plotting
    # points = MultiPoint(ndarr).buffer(4)
    points = MultiPoint(ndarr)
    line = LineString(ndarr)
    return line


def plot_test():
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs

    # This is what I want out at the end. I could in principle create it directly, but I feel a bit happier creating the
    #  intermediate obkject for now.

    line = read_caliop_met_file("F:\Local Data\CAL_LID_L2_05kmAPro-Standard-V4-10.2007-12-31T23-51-28ZN.hdf.met")
    print(line.wkt)

    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=90))
    ax.coastlines()
    ax.set_global()
    ax.add_geometries([line], ccrs.PlateCarree(), facecolor='orange', edgecolor='black')

    plt.show()
