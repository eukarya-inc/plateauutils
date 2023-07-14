import glob
import numpy as np
import os
from plateauutils.abc.plateau_parser import PlateauParser
from plateauutils.mesh_geocorder.polygon_to_meshcode_list import PolygonToMeshCodeList
from shapely.geometry import Polygon
import shutil
import xml.etree.ElementTree as ET
import zipfile


class CityGMLParser(PlateauParser):
    """CityGMLファイルをパースするクラス

    Parameters
    ----------
    polygon : shapely.geometry.Polygon
        対象となるポリゴン
    """

    def __init__(self, polygon: Polygon = None):
        super().__init__(polygon)

    def parse(self, target_path: str = "") -> list:
        """CityGMLファイルをパースして、情報を返すメソッド

        Parameters
        ----------
        target_path : str
            CityGMLファイル(zip)のパス

        Returns
        -------
        list
            パースした情報のリスト、以下の情報を含む

            * gid: gml:id
            * center: 中心座標
            * min_height: 最小高さ
            * measured_height: 測定高さ
            * building_structure_type: 建物構造種別(コード)
        """
        # ファイルが存在しないならエラー
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"target_path: {target_path} is not found")
        # zipファイルにターゲットのパスが存在するか確認
        hit_targets = []
        with zipfile.ZipFile(target_path) as zip_file:
            for name in zip_file.namelist():
                for target in self.targets:
                    path = os.path.join("udx", "bldg", target + "_bldg")
                    if name.find(path) >= 0:
                        hit_targets.append(target)
        if len(hit_targets) == 0:
            raise ValueError(f"target_path: {target_path} is not target")
        # zipファイルを解凍する
        unarchived_dir = target_path.replace(".zip", "")
        shutil.unpack_archive(target_path, unarchived_dir)
        # 返り値を作成
        return_list = []
        # 解凍したファイルをパースする
        for target in hit_targets:
            # ファイルパスを作成
            target_file_path = os.path.join(
                unarchived_dir, "*", "udx", "bldg", target + "_bldg_*.gml"
            )
            # ファイルが二つ以上ある場合に対応させる
            for file_path in glob.glob(target_file_path):
                # XMLのオブジェクトとして読み込む
                tree = ET.parse(file_path)
                root = tree.getroot()
                # パース処理を実施する
                ret = self._parse(root)
                # 返り値に追加
                return_list.extend(ret)
        # 返り値を返却
        return return_list

    def download_and_parse(self, url: str = "", target_dir: str = "") -> list:
        """CityGMLファイルをダウンロードして、情報を返すメソッド

        Parameters
        ----------
        url : str
            CityGMLファイル(zip)のURL
        target_dir : str
            ファイルを展開する先のパス

        Returns
        -------
        list
            パースした情報のリスト、以下の情報を含む

            * gid: gml:id
            * center: 中心座標
            * min_height: 最小高さ
            * measured_height: 測定高さ
            * building_structure_type: 建物構造種別(コード)
        """
        saved_path = self._download(url, target_dir)
        return self.parse(saved_path)

    def _target_list(self, polygon: Polygon = None) -> list:
        # PolygonがNoneならエラー
        if polygon is None:
            raise ValueError("polygon is None")
        # ターゲットとなるメッシュ
        target_meshes = ["1", "2", "2/1", "3", "4/1"]
        # 返り値を作成
        return_list = []
        # メッシュごとに処理
        for mesh in target_meshes:
            # メッシュごとにPolygonを分割
            polygon_to_mesh_code = PolygonToMeshCodeList(polygon, mesh)
            # 返り値に追加
            for j in polygon_to_mesh_code.output():
                return_list.append(j)
        # 返り値を返す
        return return_list

    def _parse(self, root: ET.Element) -> list:
        # 返り値を作成
        return_list = []
        # core:cityObjectMemberの一覧を取得
        city_object_members = root.findall(
            ".//{http://www.opengis.net/citygml/2.0}cityObjectMember"
        )
        # core:cityObjectMemberごとに処理
        for city_object_member in city_object_members:
            # bldg:Buildingを取得
            building = city_object_member.find(
                ".//{http://www.opengis.net/citygml/building/2.0}Building"
            )
            # gml:idを取得
            gid = building.attrib["{http://www.opengis.net/gml}id"]
            # bldg:mesuredHeightを取得
            measured_height = float(
                city_object_member.find(
                    ".//{http://www.opengis.net/citygml/building/2.0}measuredHeight"
                ).text
            )
            # uro:buildingDetailAttributeを取得
            building_detail_attribute = city_object_member.find(
                ".//{https://www.geospatial.jp/iur/uro/2.0}buildingDetailAttribute"
            )
            # uro:buildingStructureTypeを取得
            building_structure_type = building_detail_attribute.find(
                ".//{https://www.geospatial.jp/iur/uro/2.0}buildingStructureType"
            ).text
            # bldg:lod1Solidを取得
            lod1_solid = city_object_member.find(
                ".//{http://www.opengis.net/citygml/building/2.0}lod1Solid"
            )
            # 返り値に入る値を作成
            return_value = {
                "gid": gid,
                "center": None,
                "min_height": 10000,
                "measured_height": measured_height,
                "building_structure_type": building_structure_type,
            }
            # gml:posListを取得
            pos_lists = lod1_solid.findall(".//{http://www.opengis.net/gml}posList")
            for poi_list in pos_lists:
                # posListをパース
                polygon, max_height = self._parse_poi_list(poi_list.text)
                if max_height < return_value["min_height"]:
                    # 返り値に追加
                    return_value["center"] = [polygon.centroid.x, polygon.centroid.y]
                    return_value["min_height"] = max_height
            # 返り値を追加
            return_list.append(return_value)
        # 返り値を返す
        return return_list

    def _parse_poi_list(self, poi_list: str) -> tuple[Polygon, float]:
        # numpyの3次元配列に変換する
        numbers = [float(x) for x in poi_list.split()]
        num_numbers = len(numbers)
        # 3で割り切れることを確認
        if num_numbers % 3 != 0:
            raise ValueError("poi_list is invalid")
        array = np.array(numbers).reshape((-1, 3))
        # max_heightを作成
        max_height = np.max(array[:, 2])
        # heightを削除
        new_array = np.delete(array, 2, axis=1)
        # Polygonを作成する際にlon, latの順番にする
        list_of_points = [sublist[::-1] for sublist in new_array.tolist()]
        polygon = Polygon(list_of_points)
        # 返り値を返す
        return polygon, max_height
