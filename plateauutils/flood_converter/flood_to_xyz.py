import pandas as pd
from plateauutils.abc.numpy_tile_parser import NumpyTileParser


class FloodToXyz(NumpyTileParser):
    """洪水浸水域をxyzに変換するクラス

    Parameters
    ----------
    path : str
        npzファイルのベースパス
    """

    def __init__(self, path: str = ""):
        super().__init__(path)

    def parse(self):
        """洪水浸水域をxyzに変換するメソッド"""
        lons, lats, maps = self._parse_tile()
        # xyzファイルを作成, 並びはlatitude, longitude, altitude
        df = pd.DataFrame({"lat": lats, "lon": lons, "map": maps})
        return df.to_csv(index=False, header=False, sep=" ")
