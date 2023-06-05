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
