from django.test import TestCase
from nose.tools import assert_almost_equal
from django.contrib.gis.geos import LineString
import numpy as np
from datasets.models import MeasurementFile, Dataset
from .utils import lat_lon_points_to_linestring, GLOBAL_EXTENT

IDL = LineString(((180, -90), (180, 90)))
GMT = LineString(((0, -90), (0, 90)))


# Some example CALIOP tracks
GMT_CALIOP_lats = np.array([-61.2257804870605, -79.5027313232422, -73.3666152954102, -53.5407295227051, -32.7400054931641,
                            -11.6668529510498, 9.50000190734863, 30.6280879974365, 51.5395812988281, 71.6460189819336,
                            71.6834182739258, 51.5807838439941, 30.6695766448975, 9.54182147979736,
                            -11.6248531341553, -32.6984558105469, -53.4998626708984, -73.3305435180664,
                            -79.5287094116211, -61.265796661377, -61.2257804870605])

GMT_CALIOP_lons = np.array([22.8961048126221, -14.4517259597778, -115.92992401123, -135.000335693359, -142.396087646484,
                            -147.470413208008, -152.020462036133, -156.99609375, -164.019744873047, 179.211883544922,
                            179.148132324219, -164.038177490234, -157.007110595703, -152.029357910156,
                            -147.479736328125, -142.407501220703, -135.020553588867, -116.005149841309,
                            -14.6338376998901, 22.8673706054688, 22.8961048126221])

GMT2_CALIOP_lats = np.array([72.0812911987305, 81.419303894043, 67.3020477294922, 49.3935546875, 30.9990997314453,
                             12.4387702941895, -6.16989135742188, -24.7372646331787, -43.1630363464355,
                             -61.2502784729004, -61.2903709411621, -43.2042808532715, -24.7791023254395,
                             -6.21180105209351, 12.3969297409058, 30.9572525024414, 49.3524017333984,
                             67.26318359375, 81.4064712524414, 72.1185913085938, 72.0812911987305])

GMT2_CALIOP_lons = np.array([156.938018798828, 74.1632766723633, 20.8236236572266, 9.10158443450928, 3.12463307380676,
                             -1.29365634918213, -5.28192234039307, -9.46958351135254, -14.699912071228,
                             -23.4183616638184, -23.4468173980713, -14.7141056060791, -9.47976684570312,
                             -5.29088544845581, -1.30288529396057, 3.11358022689819, 9.08454322814941,
                             20.7806148529053, 73.8929672241211, 156.872039794922, 156.938018798828])

BOTH_CALIOP_lats = np.array([-61.7712249755859, -79.8181915283203, -73.0511169433594, -53.2617797851562,
                             -32.5424118041992, -11.5558624267578, 9.52341079711914, 30.5632972717285,
                             51.3922729492188, 71.4396667480469, 71.4773330688477, 51.4333457946777,
                             30.6049404144287, 9.56545066833496, -11.514142036438, -32.5010299682617,
                             -53.2211380004883, -73.0146713256836, -79.8428802490234, -61.8112258911133,
                             -61.7712249755859])

BOTH_CALIOP_lons = np.array([0.926125824451447, -38.1023101806641, -138.352874755859, -156.826950073242,
                             -164.115707397461, -169.144790649414, -173.661911010742, -178.600189208984,
                             174.449676513672, 158.034301757812, 157.972320556641, 174.431655883789,
                             -178.611175537109, -173.6708984375, -169.153839111328, -164.126892089844,
                             -156.8466796875, -138.425415039062, -38.2956123352051, 0.896559417247772,
                             0.926125824451447])


class TestMeasurementFile(TestCase):

    def setUp(self):
        from datetime import datetime
        self.time_start = datetime(1960, 1, 1)
        self.time_end = datetime(1960, 1, 2)

    def test_can_create_global_extent(self):
        mf = MeasurementFile.objects.create(time_start=self.time_start, time_end=self.time_end,
                                            name='test.nc', spatial_extent=GLOBAL_EXTENT.wkt)
        assert_almost_equal(mf.spatial_extent.area, 64800, delta=10)  # in deg² - should be in km^2...

    def test_CALIOP_crossing_meridian(self):
        ls = lat_lon_points_to_linestring(GMT2_CALIOP_lons, GMT2_CALIOP_lats)
        mf = MeasurementFile.objects.create(time_start=self.time_start, time_end=self.time_end,
                                            name='test.nc', spatial_extent=ls.wkt)

        assert mf.spatial_extent.intersects(GMT)

    def test_another_CALIOP_crossing_meridian(self):
        ls = lat_lon_points_to_linestring(GMT_CALIOP_lons, GMT_CALIOP_lats)
        mf = MeasurementFile.objects.create(time_start=self.time_start, time_end=self.time_end,
                                            name='test.nc', spatial_extent=ls.wkt)

        assert mf.spatial_extent.intersects(GMT)

    def test_CALIOP_crossing_dateline_and_meridian(self):
        ls = lat_lon_points_to_linestring(BOTH_CALIOP_lons, BOTH_CALIOP_lats)
        mf = MeasurementFile.objects.create(time_start=self.time_start, time_end=self.time_end,
                                            name='test.nc', spatial_extent=ls.wkt)

        assert mf.spatial_extent.intersects(GMT)
        # The lines won't actually intersect the dateline - but will do if we buffer the dateline a bit
        assert mf.spatial_extent.intersects(IDL.buffer(1.0))


class TestFixtures(TestCase):

    fixtures = ['test_fixtures.json']

    def setUp(self):
        self.caliop_ds = Dataset.objects.filter(name='CALIOP L2 Aerosol Profile V4').first()
        self.ace1_ship_ds = Dataset.objects.filter(name='ACE1 Ship').first()
        self.ace1_ship_mf = MeasurementFile.objects.filter(measurements__dataset=self.ace1_ship_ds).first()
        self.ace1_c130_ds = Dataset.objects.filter(name='ACE1 C-130').first()

    def test_can_query_intersection_between_datasets(self):
        assert self.ace1_ship_ds.spatial_extent.intersects(self.caliop_ds.spatial_extent)
        assert self.ace1_ship_ds.spatial_extent.intersects(self.ace1_c130_ds.spatial_extent)

    def test_can_query_intersection_between_datasets_and_measurement_files(self):
        assert self.ace1_ship_mf.spatial_extent.intersects(self.caliop_ds.spatial_extent)
