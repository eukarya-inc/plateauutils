# 開発者向け情報

## 開発環境の整備

```bash
python3.9 -m venv venv
./venv/bin/activate
pip install -U pip
pip install -r dev-requirements.txt
pytest --cov=plateauutils --cov-report=html --cov-fail-under=90
```

## CityGMLのパーサーを拡充する

CityGMLのパーサーを拡充する(パースする属性を増やす)には、ライブラリ内の[parser/city_gml_parser.py](https://github.com/eukarya-inc/plateauutils/blob/main/plateauutils/parser/city_gml_parser.py)の`_parse`メソッドを修正します。

具体的には `for city_object_member in city_object_members:` のループ内で、以下のように属性を追加します。[PR#62](https://github.com/eukarya-inc/plateauutils/pull/62)

```python
            try:
                # bldg:usageを取得
                usage = city_object_member.find(".//bldg:usage", ns)
                # bldg:usageのdescriptionを取得
                usage_xml_path = os.path.normpath(
                    os.path.join(target, "..", "../../codelists/Building_usage.xml")
                )
                usage_xml_root = ET.fromstring(zip_file.read(usage_xml_path))
                usage_text = None
                for usage_xml_root_child in usage_xml_root.findall(
                    ".//gml:dictionaryEntry", ns
                ):
                    gml_name = usage_xml_root_child.find(".//gml:name", ns)
                    if str(gml_name.text) == str(usage.text):
                        usage_text = str(
                            usage_xml_root_child.find(".//gml:description", ns).text
                        )
                        break
            except AttributeError:
                print("bldg:usage is NoneType in", gid, "in", target)
                usage_text = None
```

上記の例では`try`ブロック内で`bldg:usage`を取得し、その`description`を`codelists/Building_usage.xml`から取得しています。

`try`ブロックを使うことで、`bldg:usage`が存在しない場合にエラーが発生することを防ぎます。

Plateauではファイルによって存在しない属性があるため、`try`ブロックを使うことでエラーを回避しています。

最後に、`usage_text`を`return_value`に追加します。

```python
            return_value = {
                "gid": gid,
                "center": None,
                "min_height": 10000,
                "measured_height": measured_height,
                "building_structure_type": building_structure_type_text,
                "usage": usage_text,
            }
```

Plataeuでは様々な属性が定義されているため、属性に応じて`_parse`メソッドを拡充していき、`return_value`に属性を増やしていきます。

そのときに気をつけるべきことは、属性値の属性の型及び多重度です。

例えば、`uro:realEstateIDOfBuilding`は`xs:string`型であり、`1`の多重度を持ちます。

このケースでは、`return_value`にはString型の値を追加しますが、Plateauのバージョンによっては属性が無いため、`try`ブロックを使ってエラーを回避します。

また、`uro:realEstateIDOfBuildingUnitOwnership`は`xs:string`型であり、`0..*`の多重度を持ちます。

このケースでは、`return_value`にはString型の*配列*を追加しますが、属性が存在しない場合でも必ず空の配列を返すようにします。

このように、属性値の属性の型及び多重度に応じて`_parse`メソッドを拡充していきます。

## コード整形について

コード整形には、[black](https://pypi.org/project/black/)を利用しています。

Visual Studio Codeの場合はすでに設定されているため、特に設定は不要です。

なお、現状の設定では保存時に自動的にコード整形が行われます。

## テストについて

テストには、[pytest](https://docs.pytest.org/en/6.2.x/)を利用しています。

テストに使うデータは、ネットワーク通信を含めたテストの場合はインターネット上にデータを置きます。

その際、テストデータが肥大化しないように注意をしてください。

ローカルのテストデータの場合は`tests`ディレクトリ内に配置してください。

## APIドキュメントについて

APIドキュメントは、[Sphinx](https://www.sphinx-doc.org/ja/master/)を利用しています。

以下のコマンドでビルドできます。

```bash
cd doc
make html
```

ビルド後、`doc/_build/html/index.html`をブラウザで開くと、APIドキュメントが閲覧できます。