Regressionmodels 
=======

#### A package which can be used to fit linear- as well as polynomial Regression Models to n-dimensional data.

# Installation 

The installation requires a Python Version of 3.6+.

You can install the package via:

`pip install regressionmodels`

If you already installed the package you can update it via:

`pip install --upgrade sdllib`

#Installation for Developers

Locally, the package and its development-dependencies can be installed via:

`pip install .[dev] `

and in the main directory of the package via 

`python setup.py sdist bdistwheel`

the package can be built as Source- and Binary-Distribution. 

# Unittests

You can run Unittests with `pytest`. You can conduct them locally via

```pytest test.py```

# Overview of the Modules

## model.py 

Includes a class Regression, which can be initialized via 

`Regression(deg=1)`

with the parameter deg (default =1) to determine which degree of Regression function should be fit on the data.

The beta vector can be estimated using the method:

`.fit(X,y)` 

After that, the fitted beta can be used to predict unseen data via:

`.predict(X)`



