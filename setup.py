from setuptools import setup

setup(
    name='cis_esp',
    version=0.1,
    description='CIS Evaluation and data Synthesis Platform',
    author='Duncan Watson-Parris',
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Visualization',
        'Environment :: Web Environment',
        ],
    scripts=[],
    install_requires=['jinja2', 'gdal', 'psycopg2', 'django', 'django-widget-tweaks', 'django-extensions']
)
