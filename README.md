# STILL UNDER DEVELOPMENT!
# Spectral Analysis for Earthquake Source (SAES) Parameters

## Description
This code is intended to perform a spectral analysis to calculate earthquake
source parameters, i.e. corner frequencies and source radius, assuming
a circular patch.


## INSTALLATION
```
python setup.py install
```
## USAGE
```
from saes.saes_core import saes_core
from saes.handlers.saes_main import saes_main
saes_obj=saes_core('path/to/your/control.file')

```
## EXAMPLE
