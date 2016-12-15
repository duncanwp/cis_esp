from .load_CALIOP import load_caliop_data
from os.path import join


def run(data_dir, **kwargs):
    load_caliop_data(join(data_dir, 'CALIOP'), **kwargs)
