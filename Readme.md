# Spider XINHUANET

## Overview
Spider XINHUANET is a Python-based application designed for collecting, analyzing, and visualizing the latest news from Xinhua News Agency. It supports data storage in MongoDB, synchronization with Elasticsearch, and allows users to query data using specific conditions.

## Features
- Automatically crawls the latest news from Xinhua News Agency.
- Visualizes and analyzes the collected news.
- Downloads collected data as an Excel file.
- Stores data in MongoDB.
- Synchronizes data with Elasticsearch.
- Allows querying data from Elasticsearch or MongoDB based on specific conditions.

## Modules
- **Spider**: Responsible for real-time crawling of the latest news from Xinhua News Agency and visualizing the data.
- **sync_es**: Handles the synchronization of data from MongoDB to Elasticsearch.
- **Collect**: Provides functionality for querying data from both MongoDB and Elasticsearch based on user-defined conditions.

## Technologies and Libraries Used
- **Python Libraries**:
  - `streamlit`: For creating the web interface.
  - `pyecharts`: For data visualization.
  - `pymongo`: For interacting with MongoDB.
  - `elasticsearch`: For integrating with Elasticsearch.

- **Technologies**:
  - MongoDB: NoSQL database for storing collected data.
  - Elasticsearch: Search and analytics engine for indexing and querying data.
  - Docker-compose: For containerizing the application and managing dependencies.

## Requirements
- Python 3.9
- Docker (for containerization)
- MongoDB (for data storage)
- Elasticsearch (for data synchronization and querying)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```


2. Use project:
   ```bash
	docker-compose up -d
	```