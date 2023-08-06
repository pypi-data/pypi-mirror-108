#!/usr/bin/env python
# coding: utf-8

from typing import Any, Dict
import contextlib
from deta import Deta

from essencia_app.settings import PROJECT_KEY


def sync_connect(table):
    return Deta(str(PROJECT_KEY)).Base(table)


async def connect(table):
    return Deta(str(PROJECT_KEY)).Base(table)


@contextlib.asynccontextmanager
async def DbCount(table):
    db = await connect(table)
    try:
        yield len(next(db.fetch({})))
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbUpdate(table, data):
    key = data.get("key")
    if not key:
        raise AttributeError("a key is necessary")
    db = await connect(table)
    try:
        yield db.update(data, key)
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbAll(table):
    db = await connect(table)
    try:
        yield next(db.fetch({}))
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbCheckCode(table, code):
    db = await connect(table)
    try:
        if next(db.fetch({
            "code": code
        }))[0]:
            print('código', code, 'encontrado')
            yield True
    except IndexError:
        yield False
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbInsert(table, data):
    key = data.get("key")
    if not key:
        raise AttributeError("a key is necessary")
    db = await connect(table)
    try:
        yield db.insert(data)
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbDelete(table, key):
    db = await connect(table)
    try:
        yield db.delete(key=key)
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbPut(table, data):
    db = await connect(table)
    try:
        yield db.put(data)
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbGet(table, key):
    db = await connect(table)
    try:
        yield db.get(key=key)
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbSearchByName(table, name):
    db = await connect(table)
    try:
        yield next(db.fetch({'fullname?contains': name}))
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()

@contextlib.asynccontextmanager
async def DbSearch(table, query={}):
    db = await connect(table)
    try:
        yield next(db.fetch(query))
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbFirst(table, query={}):
    db = await connect(table)
    try:
        yield next(db.fetch(query))[0]
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()


@contextlib.asynccontextmanager
async def DbLast(table, query={}):
    db = await connect(table)
    try:
        yield next(db.fetch(query))[-1]
    except BaseException as e:
        raise ValueError(e)
    finally:
        db.client.close()
