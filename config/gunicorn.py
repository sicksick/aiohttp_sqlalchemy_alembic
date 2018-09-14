bind = '0.0.0.0:8080'

backlog = 1024

workers = 1
# uvloop Ultra fast asyncio event loop https://github.com/MagicStack/uvloop
worker_class = 'aiohttp.GunicornUVLoopWebWorker'
worker_connections = 1000
timeout = 60 * 60


errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
