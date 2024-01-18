# Plateau Utils

## 1. 概要 <!-- 本リポジトリでOSS化しているソフトウェア・ライブラリについて1文で説明を記載ください -->
本リポジトリでは、Project PLATEAUの令和4年度のユースケース開発業務の一部であるUC23-01「人工衛星観測データを用いた浸水被害把握等」について、その成果物である「plateau utils」のソースコードを公開しています。

「plateau utils」は、「PLATEAUで公開されている3D都市モデル（CityGML・3DTiles/MVT）」をパースして、Pythonに読み込むためのPythonライブラリです。

## 2. 「人工衛星観測データを用いた浸水被害把握等」について <!-- 「」内にユースケース名称を記載ください。本文は以下のサンプルを参考に記載ください。URLはアクセンチュアにて設定しますので、サンプルそのままでOKです。 -->
「人工衛星観測データを用いた浸水被害把握等」では、洪水等の浸水被害発生直後の人工衛星観測データ（SARデータ）から分析した浸水範囲と3D都市モデルの地形モデル及び建築物モデルをマッチングさせることで、家屋単位での浸水深の算出および被災判定を行うシステムを開発する。さらに、導出された被災家屋リストをデータベース化し、WebGISエンジン「Re:Earth」上で可視化するシステムを構築することで、行政における罹災証明書発行業務の効率化を目指す。
本システムは、人工衛星観測データ（SARデータ）によって取得された浸水範囲と、3D都市モデルが持つ家屋情報を組み合わせて分析する際に、3D都市モデルが持つ家屋情報を取得するために開発されたシステムです。
本システムの詳細については[技術検証レポート](https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_tech_doc_0030_ver01.pdf)を参照してください。

## 3. 利用手順 <!-- 下記の通り、GitHub Pagesへリンクを記載ください。URLはアクセンチュアにて設定しますので、サンプルそのままでOKです。 -->
本システムの構築手順及び利用手順については[利用チュートリアル](https://r5-plateau-acn.github.io/SolarPotential/)を参照してください。

```bash
pip install plateauutils
```

Tested with Python 3.9 and 3.10

## CityGML parser

```python
>>> from shapely.geometry import Point
>>> from plateauutils.mesh_geocorder.geo_to_mesh import point_to_meshcode
>>> point = Point(139.71475, 35.70078)
>>> mesh_code = point_to_meshcode(point, "2/1")
>>> mesh_code
'533945471'
>>> from shapely import from_wkt
>>> from plateauutils.parser.city_gml_parser import CityGMLParser
>>> target_polygon = from_wkt("POLYGON ((130.41249721501615 33.224722548534864, 130.41249721501615 33.22506264293093, 130.41621606802997 33.22506264293093, 130.41621606802997 33.224722548534864, 130.41249721501615 33.224722548534864))")
>>> parser = CityGMLParser(target_polygon)
>>> result = parser.download_and_parse("https://assets.cms.plateau.reearth.io/assets/d6/70821e-7f58-4f69-bc34-341875704e78/40203_kurume-shi_2020_citygml_3_op.zip", "/tmp")
>>> result
[{'gid': 'bldg_383f1804-aa34-4634-949f-f769e09fa92d', 'center': [130.41263587199947, 33.22489181671553], 'min_height': 3.805999994277954, 'measured_height': 9.3, 'building_structure_type': '非木造'}, {'gid': 'bldg_877dea60-35d0-4fd9-8b02-852e39c75d81', 'center': [130.41619367090038, 33.22492719812357], 'min_height': 4.454999923706055, 'measured_height': 3.0, 'building_structure_type': '非木造'},...]
```

3D都市モデルのCityGMLのZIPファイルのURLは[G空間情報センター](https://www.geospatial.jp/ckan/dataset/plateau)から取得できる。

## MVT parser

```python
>>> from plateauutils.parser.mvt_tile_parser import MvtTileParser
>>> target_polygon = from_wkt("POLYGON ((130.525689 33.323966, 130.522728 33.314069, 130.511441 33.308653, 130.501013 33.30937, 130.492516 33.318516, 130.493717 33.325831, 130.504618 33.332249, 130.512857 33.332213, 130.525689 33.323966))")
>>> parser = MvtTileParser(target_polygon)
>>> result = parser.download_and_parse("https://assets.cms.plateau.reearth.io/assets/43/53a0e1-cc14-4228-a5ef-19333a23596d/40203_kurume-shi_2020_3dtiles-mvt_3_op.zip", "/tmp")
>>> result
['/tmp/40203_kurume-shi_2020_3dtiles-mvt_3_op/luse/15/28254/13174.mvt']
```
3D都市モデルの3D Tiles/MVTのZIPファイルのURLは[G空間情報センター](https://www.geospatial.jp/ckan/dataset/plateau)から取得できる。


## Flood converter

```python
>>> from plateauutils.flood_converter.flood_to_3dtiles import FloodTo3dtiles
>>> f = FloodTo3dtiles()
>>> f.convert('/tmp/floodmap_depth', '/tmp/depth_3dtiles')
>>> from plateauutils.flood_converter.flood_to_png import FloodToPng
>>> p = FloodToPng('/tmp/floodmap_depth')
>>> p.parse('/tmp/depth_png')
```

## How to develop

```bash
python3.9 -m venv venv
./venv/bin/activate
pip install -U pip
pip install -r dev-requirements.txt
pytest --cov=plateauutils --cov-report=html --cov-fail-under=90
```


## 4. システム概要 <!-- OSS化対象のシステムが有する機能を記載ください。 -->
### 【3D都市モデルのパーサ】
#### ①3D都市モデル（CityGML）のパース
- 3D都市モデルのCityGMLのZIPファイルのURLを指定することで、3D都市モデルのパースを行うことができる。
- 3D都市モデルのCityGMLのZIPファイルのURLはG空間情報センターから取得できる。

#### ①3D都市モデル（3DTiles、MVT）のパース
- 3D都市モデルの3DTiles、MVTのZIPファイルのURLを指定することで、3D都市モデルのパースを行うことができる。
- 3D都市モデルの3DTiles、MVTのZIPファイルのURLはG空間情報センターから取得できる。

## 5. 利用技術（未対応（サンプルのまま））

| 種別              | 名称   | バージョン | 内容 |
| ----------------- | --------|-------------|-----------------------------|
| ミドルウェア       | [poetry](https://python-poetry.org/) | 1.3.2 | Pythonライブラリの管理 |
| ライブラリ      | [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/) | 0.10.2 | SQL データベースを Python で利用するためのライブラリ <br> SQLAlchemyの空間データベース機能拡張（PostGIS にアクセスするために使用） |
|       | [Jageocoder](https://www.info-proto.com/jageocoder/) | 2.0.0 | 住所ジオコーダライブラリ（不動産登記情報における建物所在地を登記所備付地図と突合するために使用） |
|       | [GEOS](https://libgeos.org/) | 3.1.0 | 地理空間情報を処理するためのオープンソースライブラリ（Geometry Engine Open Source） |
|       | [Proj4](https://proj.org/) | 4.5.0 | 空間参照系変換ライブラリ |
|       | [React.js](https://react.dev/) | 18.2.0 | ユーザインターフェース構築のための JavaScript ライブラリ |

## 6. 動作環境（未対応（サンプルのまま）） <!-- 動作環境についての仕様を記載ください。 -->
| 項目               | 最小動作環境                                                                                                                                                                                                                                                                                                                                    | 推奨動作環境                   | 
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | 
| OS                 | Microsoft Windows 10 または 11                                                                                                                                                                                                                                                                                                                  |  同左 | 
| CPU                | Intel Core i3以上                                                                                                                                                                                                                                                                                                                               | Intel Core i5以上              | 
| メモリ             | 4GB以上                                                                                                                                                                                                                                                                                                                                         | 8GB以上                        | 
| ディスプレイ解像度 | 1024×768以上                                                                                                                                                                                                                                                                                                                                    |  同左                   | 
| ネットワーク       | 【解析・シミュレーション】<br>不要<br>【集計・適地判定】<br>範囲選択機能を使用しない場合はネットワーク環境は不要<br>範囲選択機能を使用する場合、以下のURLを閲覧できる環境が必要<br>・地理院地図（国土地理院）　<br>http://cyberjapandata.gsi.go.jp<br>・地図表示のため標準地図<br>https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png |  同左                            | 

## 7. 本リポジトリのフォルダ構成 <!-- 本GitHub上のソースファイルの構成を記載ください。 -->
| フォルダ名 |　詳細 |
|-|-|
| citygmlfinder | Re:Earth CMSよりCityGMLを探索してくる |
| flood_converter | 浸水を3DTiles、PNG、XYZタイルへ変換する |
| mesh_geocorder | ポリゴンや地物をメッシュコードのリスト化する |
| parser | 読み込んだCityGMLやMVTをパースする |
| tile_list | ポリゴンや地物をタイル化する |

## 8. ライセンス <!-- 変更せず、そのまま使うこと。 -->

- ソースコード及び関連ドキュメントの著作権は国土交通省に帰属します。
- 本ドキュメントは[Project PLATEAUのサイトポリシー](https://www.mlit.go.jp/plateau/site-policy/)（CCBY4.0及び政府標準利用規約2.0）に従い提供されています。

## 9. 注意事項 <!-- 変更せず、そのまま使うこと。 -->

- 本リポジトリは参考資料として提供しているものです。動作保証は行っていません。
- 本リポジトリについては予告なく変更又は削除をする可能性があります。
- 本リポジトリの利用により生じた損失及び損害等について、国土交通省はいかなる責任も負わないものとします。

## 10. 参考資料 <!-- 技術検証レポートのURLはアクセンチュアにて記載します。 -->
- 技術検証レポート: https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_tech_doc_0030_ver01.pdf
- PLATEAU WebサイトのUse caseページ「カーボンニュートラル推進支援システム」: https://www.mlit.go.jp/plateau/use-case/uc22-013/
