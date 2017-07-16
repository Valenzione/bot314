token = '237044631:AAHpc82QrCa0s9_svHcFsqDZV87VsdSc5Dk'
db_uri = 'mongodb://heroku_76pgrdhp:ud0vc4uvbncdqbtnkptrn74h9i@ds057806.mlab.com:57806/heroku_76pgrdhp'

WEBHOOK_HOST = '46.101.182.19'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(token)
