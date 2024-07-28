from typing import List, Any

import numpy as np

def check(K: int):
    if not (K > 0):
        raise ValueError("K must be greater than 0.")

def user_hitrate(y_rel: List[Any], y_rec: List[Any], k: int = 10) -> float:
    """
    :param y_rel: relevant items
    :param y_rec: recommended items
    :param k: number of top recommended items
    :return: 1 if top-k recommendations contains at lease one relevant item
    """
    check(k)
    return int(len(set(y_rec[:k]).intersection(set(y_rel))) > 0)


def user_precision(y_rel: List[Any], y_rec: List[Any], k: int = 10) -> float:
    """
    :param y_rel: relevant items
    :param y_rec: recommended items
    :param k: number of top recommended items
    :return: percentage of relevant items through recommendations
    """
    check(k)
    return len(set(y_rec[:k]).intersection(set(y_rel)))/k


def user_recall(y_rel: List[Any], y_rec: List[Any], k: int = 10) -> float:
    """
    :param y_rel: relevant items
    :param y_rec: recommended items
    :param k: number of top recommended items
    :return: percentage of found relevant items through recommendations
    """
    check(k)
    return len(set(y_rec[:k]).intersection(set(y_rel)))/len(set(y_rec))


def user_ap(y_rel: List[Any], y_rec: List[Any], k: int = 10) -> float:
    """
    :param y_rel: relevant items
    :param y_rec: recommended items
    :param k: number of top recommended items
    :return: average precision metric for user recommendations
    """
    check(k)
    user_ap_l = [
        user_precision(y_rel, y_rec, i+1)
        for i, item in enumerate(y_rec[:k])
        if item in y_rel
    ]
    return sum(user_ap_l)/k

def user_ap_v2(y_rel: List[Any], y_rec: List[Any], k: int = 10) -> float:
    """
    2-й вариант, когда делят не на k, а на кол-во релевантных объектов
    :param y_rel: relevant items
    :param y_rec: recommended items
    :param k: number of top recommended items
    :return: average precision metric for user recommendations
    """
    check(k)
    user_ap_l = [
        user_precision(y_rel, y_rec, i+1)
        for i, item in enumerate(y_rec[:k])
        if item in y_rel
    ]
    return np.mean(user_ap_l)


def user_ndcg(y_rel: List[Any], y_rec: List[Any], k: int = 10) -> float:
    """
    :param y_rel: relevant items
    :param y_rec: recommended items
    :param k: number of top recommended items
    :return: ndcg metric for user recommendations
    """
    check(k)
    num = min(len(y_rel), k)
    dcg = sum([1/np.log2(i+2) for i, j in enumerate(y_rec[:k]) if j in y_rel])
    idcg = sum([1/np.log2(i+1) for i in range(1, num+1)])
    if dcg == 0 and idcg == 0:
        return 0
    return dcg/idcg


def user_rr(y_rel: List[Any], y_rec: List[Any], k: int = 10) -> float:
    """
    :param y_rel: relevant items
    :param y_rec: recommended items
    :param k: number of top recommended items
    :return: reciprocal rank for user recommendations
    """
    check(k)
    for i, j in enumerate(y_rec[:k]):
        if j in y_rel:
            return 1/(i+1)
    return 0
    return 1/first_rel_rank
