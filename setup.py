from distutils.core import setup

setup(
    name='sasd',
    version='0.0.1',
    author='Jon Onwuemeka and Ge Li',
    author_email='john.onwuemeka@mail.mcgill.ca;ge.li2@mail.mcgill.ca',
    description='Earthquake stress drop calculation based on spectral methods ',
    keywords=['earthquake stress drop','spectral analysis'],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Seismologist',
        'Intended Discipline :: Science/Research'
    ],
    packages=['sasd',
              'sasd.analyzer',
              'sasd.create_plots',
              'sasd.handlers',
              'sasd.optimizer',
              'sasd.sasdutils'],
    package_dir={'sasd': 'src'}
    #scripts=['scripts/some usefule binary executables'],
)
