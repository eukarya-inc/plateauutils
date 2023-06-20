.. plateauutils documentation master file, created by
   sphinx-quickstart on Fri Jun  2 14:34:17 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to plateauutils's documentation!
========================================

This is a collection of utilities for the `Plateau <https://www.mlit.go.jp/plateau/>`_ project.

How to develop
--------------

.. code:: bash

    python3.9 -m venv venv
    ./venv/bin/activate
    pip install -U pip
    pip install -r dev-requirements.txt
    pytest --cov=plateauutils --cov-report=html --cov-fail-under=90

How to install
--------------

.. code:: bash

    pip install plateauutils

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

