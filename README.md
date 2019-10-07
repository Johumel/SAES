

# Spectral Analysis for Earthquake Source (SAES) Parameters

## 1.Description
SAES code is intended to perform a spectral analysis to calculate earthquake source parameters, i.e. corner frequencies, $f_c$, and long-period spectral amplitude, $\Omega_0$ , which can be used to calcualte seismic moment, $M_w$,  stress drop, $\Delta \sigma$, and source dimension, $r$ in subsequent analysis. Through the input control file, the code allows the user to specify the following:
1. desired source model (e.g., Brune's model, Boatwright model) 
2. choice of single spectrum fitting and/or spectral ratio fitting 
3. stations and events blacklisting or whitelisting 
4. signal-to-noise (SNR) threshold
5. instrument response removal
6. free-surface effect correction^[1]

Computation can be performed in parallel by setting ```numworkers``` larger than 1 in the control file. 

## 2.Installtion
```
cd $SAES_DIR
python setup.py install
```
## 3.Usage
```
from saes.saes_core import saes_core
saes_obj=saes_core('path/to/your/control.file')
```

## 4. Input 
**catalog.dat**
It includes the list of events to be analyzed in ***Pyrocko*** format. Alternatatively, the users can provide event list in a 11-column table, for example:
| yyyy	|	mm	|	dd 	|hr	| min	|sec|	lat	|lon	|depth	|$M_w$|ID|
|--|--|--|--|--|--|--|--|--|--|--|
|2002  |  |

![Example input table](https://github.com/Johumel/SAES/blob/master/images/image1.png)


See example in ```/input```

**cclist.dat**
*Description:*

*Parameter:*

*Example:*

**control.file**
*Description:*

*Parameter:*

*Example:*

## events.dat
*Description:*

*Parameter:*

*Example:*

## pre_filt.dat
*Description:*

*Parameter:*

*Example:*

## read.me
*Description:*

*Parameter:*

*Example:*
## stations.xml
*Description:*

*Parameter:*

*Example:*

## tt_pyrocky.dat
*Description:*

*Parameter:*

*Example:*

## tt.dat
*Description:*

*Parameter:*

*Example:*



## 5. Output
## 6. Example

> Written with [StackEdit](https://stackedit.io/).
