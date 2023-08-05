import setuptools
__version__ = '0.4.3'

with open('requirements', 'r') as fh:
    pip_req = fh.read().split('\n')
    pip_req = [x.strip() for x in pip_req if len(x.strip()) > 0]


setuptools.setup(
    name='pyorb',
    version=__version__,
    long_description='''
PyOrb
======

PyOrb is a lightweight package designed to convert between cartesian and kepler 
coordinates seamlessly and consequently following strict defined rules. It 
provides a convenience class for handling orbits and is tested for special cases 
such as planar and circular orbits.
''',
    url='https://github.com/danielk333/pyorb',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Development Status :: 4 - Beta',
    ],
    python_requires='>=3.0',
    install_requires=pip_req,
    packages=setuptools.find_packages(),
    extras_require={
        "dev":  [
            "pytest",
            "sphinx",
            'sphinx-gallery',
            'coverage',
            'matplotlib',
        ],
    },
    # metadata to display on PyPI
    author='Daniel Kastinen',
    author_email='daniel.kastinen@irf.se',
    description='Kepler orbit functions in Python',
    license='GNU-GPLv3',
)
