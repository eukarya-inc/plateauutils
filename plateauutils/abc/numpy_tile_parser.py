import abc
import glob
import numpy as np
import os


class NumpyTileParser(metaclass=abc.ABCMeta):
    def __init__(self, path: str = ""):
        self.path = path

    @abc.abstractmethod
    def parse(self):
        raise NotImplementedError("parse method is not implemented")

    def _parse_tile(self):
        """タイルをパースするメソッド"""
        tile_list = self.__make_tile_list()
        lons = []  # 経度
        lats = []  # 緯度
        maps = []  # 標高
        # それぞれのタイルをパース
        for tile in tile_list:
            t = np.load(tile)
            lons.append(t["lons"])
            lats.append(t["lats"])
            map = t["map"]
            # 標高がnanの場合は0にする
            map[np.isnan(map)] = 0
            maps.append(map)
        return np.concatenate(lons), np.concatenate(lats), np.concatenate(maps)

    def __make_tile_list(self):
        """タイルのリストを作成するメソッド"""
        return glob.glob(os.path.join(self.path, "**", "*.npz"), recursive=True)
