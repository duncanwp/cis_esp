import shapely.geometry as sgeom

GLOBAL_EXTENT = sgeom.box(-179.999, -89.999, 179.999, 89.999)

IDL = sgeom.LineString(((180, -90), (180, 90)))
GMT = sgeom.LineString(((0, -90), (0, 90)))

platform_shapes = {'Ground station': sgeom.Point, 'Ship': sgeom.LineString, 'Aircraft': sgeom.LineString,
                   'Global Model': sgeom.Polygon, 'Regional Model': sgeom.Polygon, 'Satellite': sgeom.MultiPoint}


def shift(geom):
    """
    Reads every point in every component of input geometry, and performs the following change:
        if the longitude coordinate is <0, adds 360 to it.
        if the longitude coordinate is >180, subtracts 360 from it.
    Useful for shifting between 0 and 180 centric map
    """

    if geom.is_empty:
        return geom

    if geom.has_z:
        num_dim = 3
    else:
        num_dim = 2

    def shift_pts(pts):
        """Internal function to perform shift of individual points"""
        if num_dim == 2:
            for x, y in pts:
                if x < 0:
                    x += 360
                elif x > 180:
                    x -= 360
                yield (x, y)
        elif num_dim == 3:
            for x, y, z in pts:
                if x < 0:
                    x += 360
                elif x > 180:
                    x -= 360
                yield (x, y, z)

    # Determine the geometry type to call appropriate handler
    if geom.type in ('Point', 'LineString'):
        return type(geom)(list(shift_pts(geom.coords)))
    elif geom.type == 'Polygon':
        ring = geom.exterior
        shell = type(ring)(list(shift_pts(ring.coords)))
        holes = list(geom.interiors)
        for pos, ring in enumerate(holes):
            holes[pos] = type(ring)(list(shift_pts(ring.coords)))
        return type(geom)(shell, holes)
    elif geom.type.startswith('Multi') or geom.type == 'GeometryCollection':
        # Recursive call to shift all components
        return type(geom)([shift(part)
                           for part in geom.geoms])
    else:
        raise ValueError('Type %r not supported' % geom.type)


def idl_resolve(geom, buffer_width=0.0000001):
    """
    Identifies when an intersection is present with -180/180 international date line and corrects it
    Geometry is shifted to 180 centric map and intersection is checked against a line defined as [(180, -90), (180,90)]
    If intersection is identified then the line is buffered by given amount (decimal degrees) and the difference
    between input geometry and buffer result is returned
    If no intersection is identified the passed in geometry is returned
    """

    shifted_geom = shift(geom)

    if shifted_geom.intersects(IDL):
        buffered_line = IDL.buffer(buffer_width)
        difference_geom = shifted_geom.difference(buffered_line)
        geom = shift(difference_geom)

    return geom


def lat_lon_points_to_polygon(lons, lats):
    """
    Routine for converting a list of lat lons to an outline polygon taking into account the dateline

    .note this might not work with large polygons which cross GMT *and* the IDL

    :param numpy.ndarray lats: Array of latitude points (not necasarily 1-D)
    :param numpy.ndarray lons: Array of longitude points (not necasarily 1-D)
    :return shapely.geometry.Polygon: The convex hull of the points
    """
    import numpy as np

    if all(np.abs(lons[0::3] - lons[1:2]) > 180):
        lons[0::3] = np.maximum(lons[0::3], lons[0::3]+360.0)

    poly = sgeom.MultiPoint(list(zip(lons, lats)))

    return poly.convex_hull


def lat_lon_points_to_linestring(lons, lats):
    """
    Routine for converting a list of lat lons to a linestring taking into account the dateline
    :param numpy.ndarray lats: Array of latitude points (not necasarily 1-D)
    :param numpy.ndarray lons: Array of longitude points (not necasarily 1-D)
    :return shapely.geometry.LineString: The path of the points
    """
    import cartopy.crs as ccrs
    poly = sgeom.LineString(list(zip(lons.flat, lats.flat)))

    pc = ccrs.PlateCarree()
    # Project our PC geometry onto a Geodetic -180 to 180 projection
    return pc.project_geometry(poly, ccrs.Geodetic())


def cis_object_to_shp(data, tolerance=0.1, platform_type=None):
    from iris.coords import DimCoord

    # Ensure that all the data we load is on a -180 to 180
    data.set_longitude_range(-180)

    lon = data.coord('longitude')
    lat = data.coord('latitude')

    shape = platform_shapes[platform_type] if platform_type is not None else sgeom.Polygon

    if platform_type == 'Global Model':
        poly = GLOBAL_EXTENT
    elif isinstance(lon, DimCoord) and isinstance(lat, DimCoord):
        if not lon.has_bounds():
            lon.guess_bounds()

        poly = sgeom.box(lon.bounds.min(), lat.points.min(), lon.bounds.max(), lat.points.max())
    else:
        if len(lon.points) != len(lat.points):
            raise ValueError("Longitude and Latitude must have the same number of points if they aren't DimCoords.")

        # Deal with dateline wrappings...
        if platform_type == 'Satellite':
            poly = lat_lon_points_to_polygon(lon.points, lat.points)
        elif shape == sgeom.LineString:
            poly = lat_lon_points_to_linestring(lon.points, lat.points)
        elif platform_type == 'Ground station':
            poly = shape(lon.points.flat[0], lat.points.flat[0])
        else:
            poly = shape(list(zip(lon.points.flat, lat.points.flat)))

    # Simplify to a specified tolerance
    rough_poly = poly.simplify(tolerance)

    return rough_poly


def plot_shape(shps):
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs

    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.coastlines()
    # ax.set_global()
    ax.add_geometries(shps, ccrs.PlateCarree(), edgecolor='black', alpha=0.5)

    plt.show()
