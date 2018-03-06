from .load_CALIOP import load_caliop_data
from .load_MODIS import load_modis_geoData
from os.path import join


def run(data_dir, **kwargs):
    # load_caliop_data(join(data_dir, 'CALIOP'), **kwargs)
    load_modis_geoData(join(data_dir, 'CALIOP'), **kwargs)
