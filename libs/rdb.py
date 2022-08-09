import socket

import redis


keepalive_options = {
    # socket.TCP_KEEPIDLE: 40,
    socket.TCP_KEEPCNT: 5,
    socket.TCP_KEEPINTVL: 10
}


def connect_redis(*args, **kwargs):
    kw_args = {
        "socket_connect_timeout": 15,
        "socket_timeout": 10,
        "socket_keepalive": True,
        "socket_keepalive_options": keepalive_options,
        "decode_responses": True
    }
    kw_args.update(kwargs)
    return redis.StrictRedis(*args, **kw_args)
