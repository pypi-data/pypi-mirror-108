Example Project
===============
This is an example project that is used to demonstrate how to publish
Python packages on PyPI. 

Installing
============

.. code-block:: bash

    pip install example-publish-pypi-medium

Usage
=====

.. code-block:: bash

    >>> from src.example import custom_sklearn
    >>> custom_sklearn.get_sklearn_version()
    '0.24.2'
    >>> from src.example import custom_sklearn
    >>> custom_sklearn.get_sklearn_version()
    '0.24.2'
    >>> from example_publish_pypi_medium.example import custom_sklearn
    >>> custom_sklearn.get_sklearn_version()
    '0.24.2'

