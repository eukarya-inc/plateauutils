from click.testing import CliRunner
from plateauutils.cli import point_to_meshcode, meshcode_to_polygon


def test_point_to_meshcode():
    runner = CliRunner()
    result = runner.invoke(point_to_meshcode, ["139.71475", "35.70078", "2"])
    assert result.exit_code == 0
    assert result.output == "533945\n"


def test_invalid_point_to_meshcode():
    runner = CliRunner()
    result = runner.invoke(point_to_meshcode, ["139.71475", "35.70078", "5/1"])
    assert result.exit_code == 0
    assert result.output == "Error: Mesh must be one of 1, 2, 2/1, 3, 4/1\n"


def test_meshcode_to_polygon():
    runner = CliRunner()
    result = runner.invoke(meshcode_to_polygon, ["533945"])
    assert result.exit_code == 0
    assert (
        result.output
        == "POLYGON ((139.625 35.66666666666667, 139.75 35.66666666666667, 139.75 35.75000000000001, 139.625 35.75000000000001, 139.625 35.66666666666667))\n"
    )


def test_invalid_meshcode_to_polygon():
    runner = CliRunner()
    result = runner.invoke(meshcode_to_polygon, ["53394547141"])
    assert result.exit_code == 0
    assert result.output == "Error: Mesh code must be 10 or less digits\n"
