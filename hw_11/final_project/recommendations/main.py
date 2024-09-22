import random
from typing import List
import requests

import numpy as np
import redis
from fastapi import FastAPI
import polars as pl
from models import InteractEvent, RecommendationsResponse, NewItemsEvent
from watched_filter import WatchedFilter

app = FastAPI()

redis_connection = redis.Redis('localhost')
watched_filter = WatchedFilter()

unique_item_ids = set()
EPSILON = 0.05

# movie_id_imdb = eval(requests.get('http://frontend:8000/get_all_items').content.decode())

movie_id_imdb = set(
    pl.read_csv('webapp/static/links.csv')
    .with_columns(pl.col('movieId').cast(pl.Utf8))
    .to_series()
)


@app.get('/healthcheck')
def healthcheck():
    return 200


@app.get('/cleanup')
def cleanup():
    global unique_item_ids
    unique_item_ids = set()
    try:
        redis_connection.delete('*')
        redis_connection.json().delete('*')
        redis_connection.flushall()
    except redis.exceptions.ConnectionError:
        pass
    return 200


@app.post('/add_items')
def add_movie(request: NewItemsEvent):
    global unique_item_ids
    for item_id in request.item_ids:
        unique_item_ids.add(item_id)
    return 200


@app.get('/recs/{user_id}')
def get_recs(user_id: str):
    global unique_item_ids

    try:
        item_ids = redis_connection.json().get(user_id)
        popular_item_ids = redis_connection.json().get('top_items')
        random_item_ids = np.random.choice(list(movie_id_imdb), size=20, replace=False).tolist()

        item_ids = (item_ids if item_ids else []) + (popular_item_ids if popular_item_ids else []) + random_item_ids


        # item_ids = redis_connection.json().get('top_items')
    except redis.exceptions.ConnectionError:
        item_ids = np.random.choice(list(unique_item_ids), size=20, replace=False).tolist()

    if random.random() < EPSILON:
        if len(unique_item_ids) != 0:
            item_ids = np.random.choice(list(unique_item_ids), size=20, replace=False).tolist()
        else:
            item_ids = np.random.choice(list(movie_id_imdb), size=20, replace=False).tolist()
    #  Фильтруем уже просмотренные
    item_ids = [i for i in item_ids if redis_connection.get(f"{user_id}_{i}") is None]
    return RecommendationsResponse(item_ids=item_ids)


#@app.post('/interact')
#async def interact(request: InteractEvent):
#    watched_filter.add(request.user_id, request.item_id)
#    return 200
