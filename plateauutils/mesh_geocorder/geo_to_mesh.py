# coding: utf-8

import math
from shapely.geometry import Point


class MeshException(Exception):
    pass


def _validate_mesh(mesh: str):
    """メッシュコードのバリデーション"""
    if mesh not in ["1", "2", "2/1", "3", "4/1"]:
        raise MeshException("Mesh must be one of 1, 2, 2/1, 3, 4/1")


def point_to_meshcode(point: Point, mesh: str = "2"):
    """緯度経度をメッシュコードに変換して返す"""
    # メッシュコードのバリデーション
    _validate_mesh(mesh)

    # メッシュコードの初期化
    mesh_code = ""

    # 緯度経度の取得
    longitude = point.x
    latitude = point.y

    # https://qiita.com/yoshiyama_hana/items/8a9fc012cb02db7cbeb0
    # 1次メッシュ
    longitude_1st = int(longitude - 100)
    latitude_1st = int(math.floor(latitude * 60 / 40))
    mesh_code = f"{latitude_1st:02d}{longitude_1st:02d}"
    if mesh == "1":
        return mesh_code
    # 2次メッシュ
    longitude_2nd = int((longitude - math.floor(longitude)) * 60 / 7.5)
    latitude_2nd = int((latitude * 60) % 40 / 5)
    mesh_code = mesh_code + f"{latitude_2nd}{longitude_2nd}"
    if mesh == "2":
        return mesh_code

    # 3次メッシュ
    longitude_3rd = math.floor(
        ((longitude - math.floor(longitude)) * 60) % 7.5 * 60 / 45
    )
    latitude_3rd = int(math.floor(((latitude * 60) % 40) % 5 * 60 / 30))
    mesh_code = mesh_code + f"{latitude_3rd}{longitude_3rd}"
    if mesh == "3":
        return mesh_code

    # 2分の1メッシュ
    mesh_2nd1 = int(
        math.floor(((latitude * 60) % 40) % 5 * 60 % 30 / 15) * 2
        + math.floor(((longitude - math.floor(longitude)) * 60) % 7.5 * 60 % 45 / 22.5)
        + 1
    )
    print(mesh_2nd1)
    mesh_code = mesh_code + f"{mesh_2nd1:01d}"
    if mesh == "2/1":
        return mesh_code

    # 4分の1メッシュ
    mesh_4th1 = int(
        math.floor(((latitude * 60) % 40) % 5 * 60 % 30 % 15 / 7.5) * 2
        + math.floor(
            ((longitude - math.floor(longitude)) * 60) % 7.5 * 60 % 45 % 22.5 / 11.25
        )
        + 1
    )

    mesh_code = mesh_code + f"{mesh_4th1}"
    if mesh == "4/1":
        return mesh_code
