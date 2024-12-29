import streamlit as st
from utils import spider_main
import pandas as pd
from pyecharts.charts import Pie, WordCloud
from pyecharts import options as opts
from collections import Counter

limit = st.sidebar.text_input("Please enter your spider Number:")
choose = st.sidebar.selectbox("Please select your spider", ["MongoDB", "Show"])

if limit:
    if st.sidebar.button("Spider Now!"):
        result_list = spider_main(limit=int(limit), types=choose)
        df = pd.DataFrame(result_list)
        st.title("Spider DataFrame Data")
        st.dataframe(df)
        file_path = "spider_data.xlsx"
        with open(file_path, "rb") as excel_file:
            st.download_button(
                label="Download File",
                data=excel_file,
                file_name="example.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        if choose == 'MongoDB':
            st.success("Insert to MongoDB Success")

            data = pd.DataFrame(result_list)
            data.columns = ['title', 'publishUrl', 'publishTime', 'author', 'keywords', 'source', '_id']
        else:
            data = pd.DataFrame(result_list)
            data.columns = ['title', 'publishUrl', 'publishTime', 'author', 'keywords', 'source']
        data_cleaned = data.drop(0).reset_index(drop=True)

        st.title("News data visualization")
        st.header("Keyword Cloud")
        all_keywords = ','.join(data_cleaned['keywords'].dropna())
        keywords_series = data_cleaned['keywords'].dropna().str.split(',').explode()
        keyword_counts = Counter(keywords_series)
        keyword_items = keyword_counts.most_common(100)

        wordcloud = (
            WordCloud()
            .add("", keyword_items, word_size_range=[10, 100], shape="circle")
            .set_global_opts()
        )
        st.components.v1.html(wordcloud.render_embed(), height=500)

        st.header("Proportion of daily news quantity")
        data_cleaned['publishDate'] = pd.to_datetime(data_cleaned['publishTime']).dt.date
        daily_news_count = data_cleaned['publishDate'].value_counts(normalize=True) * 100
        daily_news_data = [(str(date), round(percent, 2)) for date, percent in daily_news_count.items()]

        pie_chart = (
            Pie()
            .add("", daily_news_data, radius=["30%", "70%"], center=["50%", "50%"])
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=True)
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        )
        st.components.v1.html(pie_chart.render_embed(), height=500)


