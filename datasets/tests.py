import unittest
from nose.tools import assert_almost_equal, assert_greater, assert_equal
from datasets.utils import cis_object_to_shp
from cis.test.integration_test_data import cis_test_files
import shapely.geometry as sgeom


# Create your tests here.
class TestCISLoad(unittest.TestCase):

    def test_get_global_poly_for_global_model(self):
        from cis.test.integration_test_data import valid_hadgem_filename, valid_hadgem_variable
        # This is a 0-360 dataset
        shp = cis_object_to_shp(read_data(valid_hadgem_filename, valid_hadgem_variable))
        assert_almost_equal(shp.area, 64800, 0)  # in deg²

    def test_get_global_poly_for_specified_global_model(self):
        from cis.test.integration_test_data import valid_hadgem_filename, valid_hadgem_variable
        # This is a 0-360 dataset
        shp = cis_object_to_shp(read_data(valid_hadgem_filename, valid_hadgem_variable), platform_type='Global Model')
        assert_almost_equal(shp.area, 64800, 0)  # in deg²

    def test_get_point_for_station(self):
        from cis.test.integration_test_data import valid_aeronet_filename, valid_aeronet_variable
        from shapely.wkt import loads
        shp = cis_object_to_shp(read_data(valid_aeronet_filename, valid_aeronet_variable), platform_type='Station')
        assert_almost_equal(shp.area, 0.0)
        assert shp.almost_equals(loads('POINT (-1.479 15.345)'))

    #TODO: Add some tests to check these are actually in the right place
    def test_get_points_for_ship(self):
        fileset = 'GASSP_ship'
        shp = cis_object_to_shp(read_data(cis_test_files[fileset].master_filename,
                                          cis_test_files[fileset].data_variable_name), platform_type='Ship')

        assert isinstance(shp, sgeom.LineString)

    def test_get_points_for_aircraft(self):
        fileset = 'GASSP_aeroplane'
        shp = cis_object_to_shp(read_data(cis_test_files[fileset].master_filename,
                                          cis_test_files[fileset].data_variable_name), platform_type='Aircraft')
        assert isinstance(shp, sgeom.LineString)

    def test_get_points_for_ungridded_satellite(self):
        from .utils import IDL
        from cis.test.integration_test_data import valid_modis_l2_filename
        shp = cis_object_to_shp(read_data(valid_modis_l2_filename,
                                          'Optical_Depth_Land_And_Ocean'), platform_type='Satellite')
        assert isinstance(shp, (sgeom.Polygon, sgeom.MultiPolygon))
        # There should be two components - one on either side of the dateline
        assert len(shp) == 2
        # The shapes won't actually intersect the dateline - but will do if we buffer the dateline a bit
        assert IDL.buffer(1).intersects(shp)

    def test_get_polygon_for_gridded_satellite(self):
        from cis.test.integration_test_data import valid_modis_l3_filename, valid_modis_l3_variable
        shp = cis_object_to_shp(read_data(valid_modis_l3_filename,
                                          valid_modis_l3_variable), platform_type='Satellite')
        assert isinstance(shp, sgeom.Polygon)
        # It's not quite global for some reason - probably a bounds issue
        assert_almost_equal(shp.area, 64440, 0)  # in deg²

    def test_higher_tolerance_gives_fewer_points(self):
        fileset = 'GASSP_ship'

        ship_data = read_data(cis_test_files[fileset].master_filename,
                              cis_test_files[fileset].data_variable_name)

        # Zero tolerance (Note this isn't quite the same as len(ship_data.lat.points) and varies with each run)
        assert_greater(len(cis_object_to_shp(ship_data, platform_type='Ship', tolerance=0.0).xy[0]), 11700)

        # Default
        assert_equal(len(cis_object_to_shp(ship_data, platform_type='Ship').xy[0]), 1322)

        # Half a degree
        assert_equal(len(cis_object_to_shp(ship_data, platform_type='Ship', tolerance=0.5).xy[0]), 1320)

        # One degree
        assert_equal(len(cis_object_to_shp(ship_data, platform_type='Ship', tolerance=1.0).xy[0]), 883)


if __name__ == '__main__':
    from cis.test.integration_test_data import valid_modis_l2_filename
    from cis import read_data
    from .utils import plot_shape

    shp = cis_object_to_shp(read_data(valid_modis_l2_filename,
                                      'Optical_Depth_Land_And_Ocean'),
                            platform_type='Satellite',
                            tolerance=1)
    plot_shape(shp)
