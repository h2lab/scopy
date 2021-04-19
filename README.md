
# scopy

The [scopy](https://github.com.cnpmjs.org/h2lab/scopy) python module provides oscilloscope controls and allow you to quickly build automated tests, capture traces. This module is under developpment but already allows you to automate traces capture with Lecroy and Owon XDS (xds3202e,...) scopes but also using the [Chipwisperer](https://github.com/newaetech/chipwhisperer). 

* Warning: For now you must setup your scope parameters manualy only the trigger arming and traces capture features are fully operational. As this project is opensources we do consider every contribution and pull request. 

## Dependencies

You can install the requirements of the package using:

```sh
pip install requirements.txt
```

## Installation of smartleia-target

### From git

You may need to use the last version of python builtin's setuptools to install
scopy from git

```sh
python3 -m pip install --upgrade pip setuptools wheel
```

```sh
git clone https://github.com/h2lab/scopy
cd scopy
python3 -m pip install .
`````

### From pipy

```sh
python3 -m pip install scopy
```
