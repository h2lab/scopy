
# scopy

This repository holds the source of the python package used to drive your scopes
With it, you will be able to drive lecroy and owon xds osciloscope.

The documentation dedicated to the scopy package can be found [here](https://github.com/h2lab/scopy),
please check it to have details about the basic usage and the API for advanced
development features.

## Dependencies

You can install the requirements of the package using:

```sh
pip install requirements.txt
```

## Installation of smartleia-target

### From git

You may need to use the last version of python builtin's setuptools to install
smartleia from git

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
