# coding: utf-8
import reearthcmsapi
from reearthcmsapi.apis.tags import items_project_api
from reearthcmsapi.model.model import Model
from reearthcmsapi.model.versioned_item import VersionedItem
from reearthcmsapi.model.asset_embedding import AssetEmbedding
import pprint
import requests

class NoArgsException(Exception):
    pass

class NotFoundException(Exception):
    pass

# query reearth cms via public api
def public_query(endpoint:str=None, prefecture:str=None, city_name:str=None) -> str:
    if endpoint == None or prefecture == None or city_name == None:
        raise NoArgsException
    res = None
    page = 1
    hasMore = True
    while hasMore:
        response = requests.get(endpoint, params={'page': page})
        if response.status_code == 200:
            obj = response.json()
            for item in obj['results']:
                if item['city_name'] == city_name and item['prefecture'] == prefecture:
                    res = item['citygml']['url']
                    return res
            hasMore = obj['hasMore'] == 'true'
            if hasMore:
                page += 1
        else:
            hasMore = False
    if res == None:
        raise NotFoundException

# check prefecture and city from given private api result
def _check_prefecture_city(items,prefecture,city):
    # search each items from given prefecture and city
    for item in items:
        pref_check=False
        city_check=False
        for keys in item['fields']:
            # Since the items are an array, whether each item have certain column varies.
            # This makes typing difficult.
            # So the fields are stored in the form of an array of key-value.
            if keys['key'] == 'prefecture':
                if keys['value'] == prefecture:
                    pref_check=True
            elif keys['key'] == 'city_name':
                if keys['value'] == city:
                    city_check=True
            elif keys['key'] == 'citygml':
                try:
                    # Asset is one. So it is not stored in the way of key-value and access directry.
                    # But if the key does not exist, it raises an error
                    url = keys['value']['url']
                except Exception as e:
                    url = ''
            if pref_check and city_check:
                return url
    return False

# query reearth cms via private api
def private_query(
        endpoint:str=None,
        access_token:str=None,
        project:str=None,
        model:str=None,
        prefecture:str=None,
        city_name:str=None):
    configuration = reearthcmsapi.Configuration(
        host = endpoint,
        access_token = access_token
    )
    # Enter a context with an instance of the API client
    with reearthcmsapi.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = items_project_api.ItemsProjectApi(api_client)

        # example passing only optional values
        path_params = {
            'projectIdOrAlias': project,
            'modelIdOrKey': model,
        }
        page = 1
        perPage = 50
        totalCount = 0
        query_params = {
            'sort': "createdAt",
            'dir': "desc",
            'page': page,
            'perPage': perPage,
            'ref': "latest",
            'asset': AssetEmbedding("all"),
        }
        try:
            # Returns a list of items.
            api_response = api_instance.item_filter_with_project(
                path_params=path_params,
                query_params=query_params,
            )
            items = api_response.body['items']
            url = _check_prefecture_city(items, prefecture, city_name)
            if url != None:
                return url
            totalCount = api_response.totalCount
            page += 1
        except reearthcmsapi.ApiException as e:
            print("Exception when calling ItemsApi->item_filter: %s\n" % e)
        while (page * perPage) < totalCount:
            query_params = {
                'sort': "createdAt",
                'dir': "desc",
                'page': page,
                'perPage': perPage,
                'ref': "latest",
                'asset': AssetEmbedding("all"),
            }
            try:
                # Returns a list of items.
                api_response = api_instance.item_filter_with_project(
                    path_params=path_params,
                    query_params=query_params,
                )
                items = api_response.body['items']
                url = _check_prefecture_city(items, prefecture, city_name)
                if url != None:
                    return url
                page += 1
            except reearthcmsapi.ApiException as e:
                print("Exception when calling ItemsApi->item_filter: %s\n" % e)
