import socket

import redis


keepalive_options = {
    # socket.TCP_KEEPIDLE: 40,
    socket.TCP_KEEPCNT: 2,
    socket.TCP_KEEPINTVL: 5
}


def connect_redis(*args, **kwargs):
    kw_args = {
        "socket_connect_timeout": 8,
        "socket_timeout": 5,
        "socket_keepalive": True,
        "socket_keepalive_options": keepalive_options,
        "decode_responses": True
    }
    kw_args.update(kwargs)
    return redis.StrictRedis(*args, **kw_args)
