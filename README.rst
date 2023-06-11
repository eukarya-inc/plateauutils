Plateau Utils
=============

This is a collection of utilities for the [Plateau](https://www.mlit.go.jp/plateau/).

How to develop
--------------

.. code:: bash

    python3.9 -m venv venv
    ./venv/bin/activate
    pip install -U pip
    pip install -r dev-requirements.txt
    pytest --cov=plateauutils --cov-report=html --cov-fail-under=90