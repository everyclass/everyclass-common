from contextlib import contextmanager
from typing import Dict

import psycopg2
from DBUtils.PooledDB import PooledDB
from psycopg2.extras import register_hstore, register_uuid

pool = None


def init_pool(schema: str, config: Dict) -> None:
    """创建连接池"""
    # more information at https://cito.github.io/DBUtils/UsersGuide.html
    final_option = dict(creator=psycopg2,
                        mincached=1,
                        maxcached=4,
                        maxconnections=4,
                        blocking=True,
                        options=f'-c search_path={schema}')
    final_option.update(config)

    global pool
    pool = PooledDB(**final_option)


@contextmanager
def conn_context():
    if not pool:
        raise RuntimeError("Pool not initialized")
    conn = pool.connection()
    register_types(conn)
    yield conn
    conn.close()


def register_types(conn):
    real_conn = conn._con._con
    # conn 是 PooledDB（或PersistentDB）的连接，它的 _con 是 SteadyDB。而 SteadyDB 的 _con 是原始的 psycopg2 连接对象
    register_uuid(conn_or_curs=real_conn)
    register_hstore(conn_or_curs=real_conn)
