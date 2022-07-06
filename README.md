# crypto-news-etl

## Description
An attempt, of course simple, to simulate workflow of an ETL data pipline. Extracting news from [cryptonews.com](https://cryptonews.com/), transforming fetched content and loading to sqlite3 database and S3 Bucket.

## Installing

#### Use docker-compose:
```
git clone https://github.com/alimghmi/crypto-news-etl.git
cd crypto-news-etl
docker-compose up --build
```
Current working directory is mounted to container thus logs and sqlite3 database is accessible locally.

#### Or run locally:
```
git clone https://github.com/alimghmi/crypto-news-etl.git
cd crypto-news-etl
pip3 install -r requirements.txt
python3 app.py
```