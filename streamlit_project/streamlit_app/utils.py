import requests
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from elasticsearch import Elasticsearch, helpers

mongo = MongoClient(host="127.0.0.1", port=27017)
mydb = mongo['en_news']
mycol = mydb['news_databases']
mycol.create_index([("publishUrl", 1)], unique=True)

es = Elasticsearch(['http://170.11.0.1:9200']) #If implemented on another device, please change the ip address first
index_name = 'news_databases'

headers = {
    "sec-ch-ua-platform": "\"Windows\"",
    "Referer": "https://english.news.cn/culture/index.htm",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

def spider_main(limit, types):
    url = "https://english.news.cn/culture/ds_183b33c7ed1a44f4897bd0d6928556d5.json"
    response = requests.get(url, headers=headers)
    data_json = response.json()
    data_list = data_json['datasource']
    result_list = []
    for datas in data_list[0: limit]:
        keywords = datas['keywords']
        title = datas['title']
        publishUrl = datas['publishUrl'].replace('../', 'https://english.news.cn/').strip()
        publishTime = datas['publishTime']
        author = datas['author']
        source = datas['sourceText']
        save_dict = {"title": title, "publishUrl": publishUrl, "publishTime": publishTime, "author": author, "keywords": keywords, "source": source}
        if types == 'MongoDB':
            try:
                mycol.insert_one(save_dict)
            except DuplicateKeyError:
                pass
        else:
            pass
        result_list.append(save_dict)
        pd.DataFrame(result_list).to_excel('./spider_data.xlsx', index=False)
    return result_list

def collect_mongo(limit):
    cursor = mycol.find().limit(limit)
    result_list = []
    for doc in cursor:
        del doc['_id']
        result_list.append(doc)
    return result_list

def mongo_to_es(limit):
    cursor = mycol.find().limit(limit)
    actions = []
    for doc in cursor:
        action = {
            "_index": index_name,
            "_id": str(doc['_id']),
            "_source": doc
        }
        actions.append(action)
        del doc['_id']
    if actions:
        helpers.bulk(es, actions)
    else:
        pass

def collect(types, limit, query):
    if types == 'Mongodb':
        result = mycol.find(query).limit(limit)
        data = list(result)
        for datas in data:
            print(datas)
        return data
    elif types == 'ES':
        response = es.search(index="news_databases", body=query, size=limit)
        hits = response['hits']['hits']
        return hits
    else:
        raise ValueError("Unsupported data source type: {}".format(types))
