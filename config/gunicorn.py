def when_ready(server):
    open('/tmp/app-initialized', 'w').close()


bind = 'unix:///tmp/nginx.socket'
# worker_class = 'gevent'  # not necessary
timeout = 90  # not necesssary
