import copy
import datetime
import os

from flask import current_app


def plugin_available(plugin_name: str) -> bool:
    """
    check if a plugin (Sentry, apm, logstash) is available in the current environment.
    :return True if available else False
    """
    mode = os.environ.get("MODE", None)
    if mode:
        return mode.lower() in current_app.config[f"{plugin_name.upper()}_AVAILABLE_IN"]
    else:
        raise EnvironmentError("MODE not in environment variables")


__load_time = datetime.datetime.now()


def print_config(app, logger):
    """启动时输出当前配置项"""
    # 如果当前时间与模块加载时间相差一分钟之内，认为是第一次 spawn（进程随着时间的推移可能会被 uwsgi 回收），
    # 在 1 号 worker 里打印当前配置
    import uwsgi
    if uwsgi.worker_id() == 1 and (datetime.datetime.now() - __load_time) < datetime.timedelta(minutes=1):
        # 这里设置等级为 warning 因为我们希望在 sentry 里监控重启情况
        logger.warning(f'App (re)started in `{app.config["CONFIG_NAME"]}` environment')

        logger.info('Below are configurations we are using:')
        logger.info('================================================================')
        for key, value in app.config.items():
            if key not in app.config.PRODUCTION_SECURE_FIELDS:
                if any(map(lambda t: isinstance(value, t), (dict,))):
                    value = copy.copy(value)
                    for k in value.keys():
                        if "{}.{}".format(key, k) in app.config.PRODUCTION_SECURE_FIELDS:
                            value[k] = '[secret]'
                logger.info('{}: {}'.format(key, value))
            else:
                logger.info("{}: [secret]".format(key))
        logger.info('================================================================')
