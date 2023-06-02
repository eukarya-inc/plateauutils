# coding: utf-8

import click


@click.group()
def cli():
    pass


@cli.group()
def mesh_geocorder():
    """Mesh geocorder commands"""
    pass


@mesh_geocorder.command()
@click.argument("point", required=True, type=str)
@click.argument("mesh", required=False, type=str, default="2")
def point_to_mesh(point, mesh):
    """Convert a point to a mesh"""
    pass


def main():
    cli()


if __name__ == "__main__":
    main()
