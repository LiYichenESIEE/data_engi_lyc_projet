import streamlit as st
from datetime import datetime
import pandas as pd
from utils import collect
import re

st.title('Data query tool')

data_source = st.selectbox('Select data source', ['ES', 'Mongodb'])

item = st.selectbox("Select Field", ["date", 'keyword'])

limit = st.text_input("Please enter the quantity to be queried", "10")

collect_dict = {}

if item == 'date':
    query_item = st.date_input('Query specified date', min_value=datetime(2020, 1, 1).date(), value=datetime(2024, 1, 1).date())
    collect_dict = {"keyword": "publishTime", "query_item": query_item.strftime('%Y-%m-%d')}
elif item == 'keyword':
    query_item = st.text_input('Please enter keywords')
    collect_dict = {"keyword": "keywords", "query_item": query_item}

if st.button('query'):
    if not limit.isdigit():
        st.error("Please enter a valid query quantity (integer)")
    else:
        limit = int(limit)

        try:
            if data_source == 'Mongodb':
                pattern = re.compile(collect_dict['query_item'], re.IGNORECASE)
                query = {collect_dict['keyword']: {'$regex': pattern}}

            elif data_source == 'ES':
                query = {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "match": {
                                        "title": {
                                            "query": collect_dict['query_item'],
                                            "fuzziness": "AUTO"
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "keywords": {
                                            "query": collect_dict['query_item'],
                                            "fuzziness": "AUTO"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            data = collect(types=data_source, limit=limit, query=query)

            if data:
                df = pd.json_normalize(data)
                st.subheader('Query results:')
                st.write(df)
            else:
                st.write('No matching results found!')

        except Exception as e:
            st.error(f"Query failed:{e}")
