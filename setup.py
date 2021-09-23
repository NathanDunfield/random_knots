long_description = """\
A sample of knot diagrams, with one diagram per crossing number in
[3,...,1000]
"""

from setuptools import setup

setup(
    name = 'knot_sample',
    version = '0.1',
    description = 'Random knots for fun and profit',
    long_description = long_description,
    url = 'http://t3m.computop.org',
    author = 'Nathan M. Dunfield and Malik Obeidin',
    author_email = 'nathan@dunfield.info',
    license='GPLv2+',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
        ],
    packages = ['knot_sample'],
    install_requires = ['snappy'],
    package_dir = {'knot_sample':'knot_sample'},
    package_data = {'knot_sample':['knots.sqlite']}
)

