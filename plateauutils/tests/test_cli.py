from click.testing import CliRunner
from plateauutils.cli import point_to_meshcode


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
