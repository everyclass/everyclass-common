from contextlib import contextmanager
from typing import Dict, Optional

import psycopg2
from DBUtils.PooledDB import PooledDB
from psycopg2.extras import register_hstore, register_uuid

pool = None
cfg_schema = None
cfg_config = None


def init_pool(schema: Optional[str] = None, config: Optional[Dict] = None) -> None:
    """创建连接池"""
    # more information at https://cito.github.io/DBUtils/UsersGuide.html
    global pool, cfg_schema, cfg_config

    if schema:
        cfg_schema = schema
    else:
        if cfg_schema is None:
            raise RuntimeError("schema not set")
        schema = cfg_schema

    if config:
        cfg_config = config
    else:
        if cfg_config is None:
            raise RuntimeError("config not set")
        config = cfg_config

    final_option = dict(creator=psycopg2,
                        mincached=1,
                        maxcached=4,
                        maxconnections=4,
                        blocking=True,
                        options=f'-c search_path={schema}')
    final_option.update(config)

    pool = PooledDB(**final_option)


@contextmanager
def conn_context():
    if not pool:
        raise RuntimeError("Pool not initialized")
    conn = pool.connection()
    register_types(conn)
    yield conn
    conn.close()


MAX_TRIALS = 2


@contextmanager
def conn_context_with_retry():
    success = False
    trials = 0

    while not success and trials < MAX_TRIALS:
        try:
            with conn_context() as conn:
                yield conn
        except RuntimeError:
            # 连接池没有被初始化
            init_pool()
        else:
            success = True
        finally:
            trials += 1
    if not success:
        raise RuntimeError(f"DB connection context failed after {trials} trials")


def register_types(conn):
    real_conn = conn._con._con
    # conn 是 PooledDB（或PersistentDB）的连接，它的 _con 是 SteadyDB。而 SteadyDB 的 _con 是原始的 psycopg2 连接对象
    register_uuid(conn_or_curs=real_conn)
    register_hstore(conn_or_curs=real_conn)
