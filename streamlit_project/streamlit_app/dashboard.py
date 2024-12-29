import streamlit as st

st.title("Spider XINHUANET")

st.markdown('''## Spider XINHUANET

### 1. Feature Introduction
- Automatically collects the latest news from Xinhua News Agency
- Visualizes and analyzes the collected news
- Downloads data as an Excel spreadsheet
- Stores data in MongoDB
- Synchronizes data to Elasticsearch
- Queries data from Elasticsearch or MongoDB based on specific conditions

### 2. Module Division
- Spider: Responsible for real-time crawling of the latest news from Xinhua News Agency and visualizing the data
- sync_es: Responsible for transferring data from MongoDB to Elasticsearch
- Collect: Responsible for querying data from MongoDB and Elasticsearch based on conditions

### 3. Python Libraries and Technologies Used
- streamlit
- pyecharts
- pymongo
- elasticsearch

Technologies:
- MongoDB
- Elasticsearch
- Docker-compose
- streamlit
''')