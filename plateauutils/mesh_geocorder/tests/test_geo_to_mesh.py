from shapely.geometry import Point


def test_invalid_mesh():
    """メッシュコードが不正な場合のテスト"""
    from plateauutils.mesh_geocorder.geo_to_mesh import MeshException, _validate_mesh

    try:
        _validate_mesh("0")
    except MeshException:
        pass
    else:
        assert False


def test_point_to_mesh():
    """緯度経度をメッシュコードに変換するテスト"""
    from plateauutils.mesh_geocorder.geo_to_mesh import point_to_meshcode

    point = Point(139.71475, 35.70078)
    mesh_code = point_to_meshcode(point, "1")
    assert mesh_code == "5339"

    mesh_code = point_to_meshcode(point, "2")
    assert mesh_code == "533945"

    mesh_code = point_to_meshcode(point, "3")
    assert mesh_code == "53394547"

    mesh_code = point_to_meshcode(point, "2/1")
    assert mesh_code == "533945471"

    mesh_code = point_to_meshcode(point, "4/1")
    assert mesh_code == "5339454711"


def test_meshcode_to_polygon():
    """メッシュコードからポリゴンを生成するテスト"""
    from plateauutils.mesh_geocorder.geo_to_mesh import meshcode_to_polygon

    mesh_code = "5339"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139 35.333333333333336, 140 35.333333333333336, 140 36, 139 36, 139 35.333333333333336))"
    )

    mesh_code = "533900"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139 35.333333333333336, 139.125 35.333333333333336, 139.125 35.41666666666667, 139 35.41666666666667, 139 35.333333333333336))"
    )

    mesh_code = "533945"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.625 35.66666666666667, 139.75 35.66666666666667, 139.75 35.75000000000001, 139.625 35.75000000000001, 139.625 35.66666666666667))"
    )

    # TODO: implement
    mesh_code = "53394500"
    polygon = meshcode_to_polygon(mesh_code)
    assert polygon == None
