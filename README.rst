Plateau Utils
=============

This is a collection of utilities for the `Plateau <https://www.mlit.go.jp/plateau/>`_ project.

.. code:: python

    >>> from plateauutils.mesh_geocorder.geo_to_mesh import point_to_meshcode
    >>> point = Point(139.71475, 35.70078)
    >>> mesh_code = point_to_meshcode(point, "2/1")
    >>> mesh_code
    '533945471'

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
