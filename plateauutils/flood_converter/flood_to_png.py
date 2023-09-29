import abc
import math
import numpy as np
import os
from plateauutils.abc.numpy_tile_parser import NumpyTileParser
import sys


class FloodToPng(NumpyTileParser):
    """洪水浸水域をpngに変換するクラス

    Parameters
    ----------
    path : str
        npzファイルのベースパス
    """

    def __init__(self, path: str = ""):
        super().__init__(path)

    def parse(self, output_dir: str = ""):
        """洪水浸水域をpngに変換するメソッド

        Parameters
        ----------
        output_dir : str
            pngの出力先
        """
        # lontitude, latitude, altitudeを取得
        lons, lats, maps = self._parse_tile()
        # storeを作成
        store = Store()
        # storeのaddメソッドをベクトル化
        vfunc = np.vectorize(store.add)
        # storeにlontitude, latitude, altitudeを追加
        vfunc(lons, lats, maps)
        # pngを書き出す
        writer = PngWriter(output_dir, 15)
        writer.setStore(store)
        writer.write()


class Store(object):
    """タイルの座標及び標高を保持するクラス"""

    def __init__(self):
        self.zoom = 15
        self.storage = dict()

    def add(self, x, y, z):
        """タイルの座標及び標高を格納するメソッド"""
        longitude, latitude, altitude = x, y, z
        # 座標からタイルの座標とタイル内の座標を取得
        x, y, pos_x, pos_y = self._coordinate_to_position(longitude, latitude)
        # storageに格納
        self._insert(x, y, pos_x, pos_y, altitude)

    def _insert(self, x, y, pos_x, pos_y, altitude):
        # keyがstorageに存在する場合はその値を取得
        key = (x, y)
        if key in self.storage.keys():
            array = self.storage[key]
        else:
            # 存在しない場合は256*256の配列を作成
            array = np.zeros((256, 256))
            array.fill(-np.inf)
            self.storage[key] = array
        # 標高を格納
        current = array[pos_x][pos_y]
        if current < altitude:
            array[pos_x][pos_y] = altitude
            self.storage[key] = array

    def _coordinate_to_position(self, longitude, latitude):
        """座標からタイルの座標とタイル内の座標を取得するメソッド"""
        # 座標からタイルのベースとなる座標を取得
        real_x = self._longitude_to_tile_with_decimal(longitude)
        real_y = self._latitude_to_tile_with_decimal(latitude)
        # タイル座標を取得
        x = math.floor(real_x)
        y = math.floor(real_y)
        # タイル内の座標を取得
        pos_x = math.floor((real_x - x) * 256)
        pos_y = math.floor((real_y - y) * 256)
        return x, y, pos_x, pos_y

    def _longitude_to_tile_with_decimal(self, longitude):
        # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
        return (longitude + 180) / 360 * math.pow(2, self.zoom)

    def _latitude_to_tile_with_decimal(self, latitude):
        # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
        return (
            (
                1
                - math.log(
                    math.tan(latitude * math.pi / 180)
                    + 1 / math.cos(latitude * math.pi / 180)
                )
                / math.pi
            )
            / 2
            * math.pow(2, self.zoom)
        )


class Writer(metaclass=abc.ABCMeta):
    """storeの内容を書き出す基底クラス

    出力する形式に応じて _write メソッドを実装する

    Parameters
    ----------
    directory : str
        出力先ディレクトリ
    zoom : int
        ズームレベル
    """

    def __init__(self, directory, zoom):
        self.directory = directory
        self.zoom = zoom

    def setStore(self, store):
        """storeをセットするメソッド"""
        self.store = store

    def write(self):
        """storeの内容を書き出すメソッド"""
        # storeの内容をタイルごとに書き出す
        for key in self.store.storage.keys():
            x = key[0]
            y = key[1]
            value = self.store.storage[key]
            # ディレクトリが無ければ作成する
            target_dir = os.path.join(self.directory, f"{self.zoom}/{x}")
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
            # 書き出し
            self._write(x, y, value)

    @abc.abstractmethod
    def _write(self, x, y, value):
        raise NotImplementedError("_parse method is not implemented")


class PngWriter(Writer):
    def __init__(self, directory, zoom):
        super().__init__(directory, zoom)

    def _write(self, x, y, value):
        # Pillowをインポート、失敗したら終了
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            print("can't import PIL / Pillow, shutdown program")
            sys.exit(-1)
        # 標高をpngに変換
        dt = np.dtype(
            {"names": ["r", "g", "b"], "formats": [np.uint8, np.uint8, np.uint8]}
        )
        converted1 = np.array(
            [tuple(self._dem_to_png(v)) for v in value.reshape(value.size)], dtype=dt
        )
        converted2 = converted1.reshape(value.shape)
        filename = f"{self.directory}/{self.zoom}/{x}/{y}.png"
        width = 256
        img = Image.new("RGB", (width, width), (128, 0, 0))
        draw = ImageDraw.Draw(img)
        for i in range(0, width):
            for j in range(0, width):
                p = converted2[i][j]
                draw.point([(i, j)], (int(p[0]), int(p[1]), int(p[2])))
        img.save(filename)

    def _dem_to_png(self, dem):
        # 標高をPNGのRGBに変換するメソッド
        # 内容が入っていなかったら白色
        if dem == -np.inf:
            return (0xFF, 0xFF, 0xFF)
        # 標高に応じて色を変更
        if dem > 20:
            # 185 26 248
            return (0xB9, 0x1A, 0xF8)
        if dem > 10:
            # 169 8 91
            return (0xA9, 0x08, 0x5B)
        if dem > 5:
            # 253 35 21
            return (0xFD, 0x23, 0x15)
        if dem > 4:
            # 236 106 141
            return (0xEC, 0x6A, 0x8D)
        if dem > 3:
            # 254 115 117
            return (0xFE, 0x73, 0x75)
        if dem > 2:
            # 236 182 182
            return (0xEC, 0xB6, 0xB6)
        if dem > 1:
            # 255 141 36
            return (0xFF, 0x8D, 0x24)
        if dem > 0.3:
            # 255 225 53
            return (0xFF, 0xE1, 0x35)
        if dem > 0.01:
            # 48 254 55
            return (0x30, 0xFE, 0x37)
        # 0.01以下は白色
        # 255 255 255
        return (0xFF, 0xFF, 0xFF)
