# STILL UNDER DEVELOPMENT!
# Spectral Analysis for Earthquake Source (SAES) Parameters

## 1.Description
This code is intended to perform a spectral analysis to calculate earthquake
source parameters, i.e. corner frequencies and source radius, assuming
a circular patch.

## 2.Input files
### 2.1 catalog.dat
*Description:*

*Parameter:*

*Example:*

### 2.2 cclist.dat
<u>Description:</u>

<u>Parameter:</u>

<u>Example:</u>

### 2.3 control.file
<u>Description:</u>

<u>Parameter:</u>

<u>Example:</u>

### 2.4 events.dat
<u>Description:</u>

<u>Parameter:</u>

<u>Example:</u>

### 2.5 pre_filt.dat
<u>Description:</u>

<u>Parameter:</u>

<u>Example:</u>

### 2.6 read.me
<u>Description:</u>

<u>Parameter:</u>

<u>Example:</u>

### 2.7 stations.xml
<u>Description:</u>

<u>Parameter:</u>

<u>Example:</u>

### 2.8 tt_pyrocky.dat
<u>Description:</u>

<u>Parameter:</u>

<u>Example:</u>

### 2.9 tt.dat
<u>Description:</u>

<u>Parameter:</u>

<u>Example:</u>


## 3.Installtion
```
python setup.py install
```
## 4.Usage
```
from saes.saes_core import saes_core
saes_obj=saes_core('path/to/your/control.file')

```
## 5.Example
