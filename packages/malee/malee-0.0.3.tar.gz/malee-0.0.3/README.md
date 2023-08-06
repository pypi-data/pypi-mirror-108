[![Build Status](https://travis-ci.com/RezaBehzadpour/financial-modeling.svg?branch=master)](https://travis-ci.com/RezaBehzadpour/financial-modeling)
[![codecov](https://codecov.io/gh/RezaBehzadpour/financial-modeling/branch/master/graph/badge.svg?token=CNWKBIN7US)](https://codecov.io/gh/RezaBehzadpour/financial-modeling)
[![Documentation Status](https://readthedocs.org/projects/financial-modeling/badge/?version=latest)](https://financial-modeling.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/financial-modeling)
![PyPI - Downloads](https://img.shields.io/pypi/dm/financial-modeling)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![financia_modeling-logo](https://user-images.githubusercontent.com/29193529/119222492-dfdf8680-bb09-11eb-9fd1-031c2aa6ec77.png)

# Financial Modeling
The `malee` package contains a collection of financial modeling functions.

The major goal of this package is to provide you an easy to use library that implements most of the financial modeling formulas like risk and return ready to be used. This package is using `numpy` as its backend so everything is fast enough as you might expect. There are similar projects like [`numpy-financial`][1], but most of the have these two problems of 1) not having everything you might need 2) not being maintained actively. Hence this packages aims to fill this gap and be your goto library when you want financial modeling stuff.

`malee` in Farsi means *Financial*. Tried so many other cool names, but I was late in the game
and they were already taken.

The source code of this package is available at https://github.com/RezaBehzadpour/malee

## Install
To install the current release of `malee`, type the following command in terminal:
```bash
$ pip install -U malee
```

## How to use?
Here's how you can calculate simple **Arithmetic Return**:  
```python
>>> import malee
>>> malee.ar(100, 140)
0.4
```

For more information, see the [documentation](https://malee.readthedocs.io).

## License
[BSD 3-Clause](LICENSE)

[1]: https://github.com/numpy/numpy-financial