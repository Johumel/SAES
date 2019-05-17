from distutils.core import setup

setup(
    name='saes',
    version='0.0.1',
    author='Jon Onwuemeka and Ge Li',
    author_email='john.onwuemeka@mail.mcgill.ca;ge.li2@mail.mcgill.ca',
    description='Earthquake source parameter calculation based on spectral analysis methods ',
    keywords=['earthquake source parameters','spectral analysis'],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Seismologist','Induced Seismicity'
        'Intended Discipline :: Science/Research'
    ],
    packages=['saes',
              'saes.analyzer',
              'saes.create_plots',
              'saes.handlers',
              'saes.optimizer',
              'saes.saesutils'],
    package_dir={'saes': 'src'},
    install_requires=[
          'obspy',
          'numpy',
          'mtspec',
          'matplotlib',
          'pyproj',
          'joblib'
      ],
    scripts=['scripts/Source_time_function.py']
)
