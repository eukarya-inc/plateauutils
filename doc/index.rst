.. plateauutils documentation master file, created by
   sphinx-quickstart on Fri Jun  2 14:34:17 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to plateauutils's documentation!
========================================

This is a collection of utilities for the `Plateau <https://www.mlit.go.jp/plateau/>`_ project.

Source code available at `GitHub <https://github.com/eukarya-inc/plateauutils>`_.

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

Usage
-----

.. code:: python

    >>> from shapely import from_wkt
    >>> from plateauutils.parser.city_gml_parser import CityGMLParser
    >>> target_polygon = from_wkt("POLYGON ((130.41249721501615 33.224722548534864, 130.41249721501615 33.22506264293093, 130.41621606802997 33.22506264293093, 130.41621606802997 33.224722548534864, 130.41249721501615 33.224722548534864))")
    >>> parser = CityGMLParser(target_polygon)
    >>> result = parser.download_and_parse("https://assets.cms.plateau.reearth.io/assets/d6/70821e-7f58-4f69-bc34-341875704e78/40203_kurume-shi_2020_citygml_3_op.zip", "/tmp")
    >>> result
    [{'gid': 'bldg_383f1804-aa34-4634-949f-f769e09fa92d', 'center': [130.41263587199947, 33.22489181671553], 'min_height': 3.805999994277954, 'measured_height': 9.3, 'building_structure_type': '610'}, {'gid': 'bldg_877dea60-35d0-4fd9-8b02-852e39c75d81', 'center': [130.41619367090038, 33.22492719812357], 'min_height': 4.454999923706055, 'measured_height': 3.0, 'building_structure_type': '610'},...]


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

