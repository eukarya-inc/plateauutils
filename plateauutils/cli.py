# coding: utf-8

import click
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from shapely.geometry import Point
from plateauutils.mesh_geocorder.geo_to_mesh import (
    point_to_meshcode as _point_to_meshcode,
    MeshException,
)


@click.group()
def cli():
    pass


@cli.group()
def mesh_geocorder():
    """Mesh geocorder commands"""
    pass


@mesh_geocorder.command()
@click.argument("longitude", required=True, type=float)
@click.argument("latitude", required=True, type=float)
@click.argument("mesh", required=False, type=str, default="2")
def point_to_meshcode(longitude, latitude, mesh):
    """Convert a point to a meshcode"""
    point = Point(longitude, latitude)
    try:
        meshcode = _point_to_meshcode(point, mesh)
        click.echo(meshcode)
    except MeshException as e:
        click.echo("Error: {}".format(e))


def main():
    cli()


if __name__ == "__main__":
    main()
