from shapely.geometry import box
from datasets.load_CALIOP import load_caliop_data

GLOBAL_EXTENT = box(-180, -90, 180, 90)


if __name__ == '__main__':
    load_caliop_data('/Users/watson-parris/Local data/2008_metfiles', test_set=True)
