import streamlit as st
from utils import mongo_to_es, collect_mongo
import pandas as pd

st.title("sync mongo data for elastic search")
collect_num = st.text_input("Please enter num")

if collect_num:
    result_list = collect_mongo(int(collect_num))
    df = pd.DataFrame(result_list)
    st.title("This is the data that will be synchronized from MongoDB to ES soon")
    st.dataframe(df)

    if st.button("Start sync"):
        judge = mongo_to_es(int(collect_num))
        
        st.success("sync success!")
