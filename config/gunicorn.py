

def when_ready(server):
    with open('/tmp/app-initialized', 'w') as nginx_app_init:  # noqa: S108
        nginx_app_init.close()


bind = 'unix:///tmp/nginx.socket'
timeout = 90  # not necesssary
