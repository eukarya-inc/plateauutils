# Plateau Utils

## 1. 概要 <!-- 本リポジトリでOSS化しているソフトウェア・ライブラリについて1文で説明を記載ください -->
本リポジトリでは、Project PLATEAUの令和4年度のユースケース開発業務の一部であるUC23-01「人工衛星観測データを用いた浸水被害把握等」について、その成果物である「Plateau Utils」のソースコードを公開しています。

「Plateau Utils」は、「PLATEAUで公開されている3D都市モデル（CityGML・3DTiles/MVT）」をパースして、Pythonに読み込むためのPythonライブラリです。

## 2. 「人工衛星観測データを用いた浸水被害把握等」について <!-- 「」内にユースケース名称を記載ください。本文は以下のサンプルを参考に記載ください。URLはアクセンチュアにて設定しますので、サンプルそのままでOKです。 -->
「人工衛星観測データを用いた浸水被害把握等」では、洪水等の浸水被害発生直後の人工衛星観測データ（SARデータ）から分析した浸水範囲と3D都市モデルの地形モデル及び建築物モデルをマッチングさせることで、家屋単位での浸水深の算出および被災判定を行うシステムを開発する。さらに、導出された被災家屋リストをデータベース化し、WebGISエンジン「Re:Earth」上で可視化するシステムを構築することで、行政における罹災証明書発行業務の効率化を目指す。
本システムは、人工衛星観測データ（SARデータ）によって取得された浸水範囲と、3D都市モデルが持つ家屋情報を組み合わせて分析する際に、3D都市モデルが持つ家屋情報を取得するために開発されたシステムです。
本システムの詳細については[技術検証レポート](https:XXXX)を参照してください。

## 3. 利用手順 <!-- 下記の通り、GitHub Pagesへリンクを記載ください。URLはアクセンチュアにて設定しますので、サンプルそのままでOKです。 -->
以下のpipコマンドにより、ライブラリをインストールしてください。
```bash
pip install plateauutils
```

## CityGML parser
CityGMLのパーサーするには、以下を参照してください。
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
[{'gid': 'bldg_383f1804-aa34-4634-949f-f769e09fa92d', 'center': [130.41263587199947, 33.22489181671553], 'min_height': 3.805999994277954, 'measured_height': 9.3, 'building_structure_type': '非木造', 'usage': '運輸倉庫施設'}, {'gid': 'bldg_877dea60-35d0-4fd9-8b02-852e39c75d81', 'center': [130.41619367090038, 33.22492719812357], 'min_height': 4.454999923706055, 'measured_height': 3.0, 'building_structure_type': '非木造', 'usage': '共同住宅'},...]
```

3D都市モデルのCityGMLのZIPファイルのURLは[G空間情報センター](https://www.geospatial.jp/ckan/dataset/plateau)から取得できる。

## MVT parser
MVTのパーサーするには、以下を参照してください。

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
浸水を3DTiles化するには、以下を参照してください。

```python
>>> from plateauutils.flood_converter.flood_to_3dtiles import FloodTo3dtiles
>>> f = FloodTo3dtiles()
>>> f.convert('/tmp/floodmap_depth', '/tmp/depth_3dtiles')
>>> from plateauutils.flood_converter.flood_to_png import FloodToPng
>>> p = FloodToPng('/tmp/floodmap_depth')
>>> p.parse('/tmp/depth_png')
```

## How to develop
開発方法は以下の通りです。

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r dev-requirements.txt
pytest --cov=plateauutils --cov-report=html --cov-fail-under=90
```


## 4. システム概要 <!-- OSS化対象のシステムが有する機能を記載ください。 -->
### 【3D都市モデルのパーサ】
#### ①3D都市モデル（CityGML）のパース
- 3D都市モデルのCityGMLのZIPファイルのURLを指定することで、3D都市モデルのパースを行うことができる。
- 3D都市モデルのCityGMLのZIPファイルのURLは[G空間情報センター](https://www.geospatial.jp/ckan/dataset/plateau)から取得できる。

#### ①3D都市モデル（3DTiles、MVT）のパース
- 3D都市モデルの3DTiles、MVTのZIPファイルのURLを指定することで、3D都市モデルのパースを行うことができる。
- 3D都市モデルの3DTiles、MVTのZIPファイルのURLは[G空間情報センター](https://www.geospatial.jp/ckan/dataset/plateau)から取得できる。

## 5. 利用技術

| 種別              | 名称   | バージョン | 内容 |
| ----------------- | --------|-------------|-----------------------------|
| ライブラリ      | click | 8.1.3 | コマンドラインインターフェース (CLI) を作成するためのライブラリ |
|       | [reearthcmsapi](https://github.com/reearth/reearth-cms-api) | 0.0.3 | Re:Earth-CMSと乗連携を行うためのライブラリ |
|       | numpy | 1.26.2 | 数値情報処理の根幹ライブラリ |
|       | pandas | 2.1.4 | データ解析や操作を容易にするためのデータ構造とツールを提供するライブラリ |
|       | Pillow | 10.0.1 | 幾何学的な操作を行うためのツールを提供するライブラリ |
|       | py3dtiles | 7.0.0 | 3D地理情報のためのタイルセットを生成・利用するためのイブラリ |
|       | pyproj | 3.6.1 | 座標変換用のライブラリ |
|       | requests | 2.31.0 | HTTPリクエストを行うためのライブラリ |
|       | shapely | 2.0.1 | Python Imaging Library (PIL) のフォークとして開発された画像処理ライブラリ |
|       | tqdm | 4.65.0 | データのダウンロードの進捗を表示 |

## 6. 動作環境 <!-- 動作環境についての仕様を記載ください。 -->
- 本ユースケースにおいては、動作環境としてGoogle Colaboratory（2024/02/01時点）を使用しています。

| 項目               | GoogleColaboratoryでの動作環境（2024/02/01時点）                                                                                                                                                                                                                                                                                                                                    | 推奨環境 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------- |
| CPU                | コア数2，スレッド数4                                                                                                                                                                                                                                                                                                                              |  同左 |
| GPU                | Tesla K80 GPU等                                                                                                                                                                                                                                                                                                                              |  同左 |
| メモリ             | 12.7GB以上                                                                                                                                                                                                                                                                                                                                          |  同左 |
| ネットワーク       | ネットワークからのダウンロード機能とRe:Earth CMSへのアップロード機能を使用しない場合はネットワーク環境は不要<br>ネットワークからのダウンロード機能とRe:Earth CMSへのアップロード機能を使用する場合、ネットワークを閲覧できる環境が必要<br> | 同左 |

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
- 技術検証レポート: https:XXXX
- PLATEAU WebサイトのUse caseページ「人工衛星観測データを用いた浸水被害把握等」: https/XXXX/
