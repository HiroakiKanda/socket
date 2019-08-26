import logging

# フォーマットを定義
formatter = '%(levelname)s : %(asctime)s : %(message)s'

# ログレベルを DEBUG に変更
#logging.basicConfig(level=logging.DEBUG, format=formatter)

# ログレベルを DEBUG に変更
logging.basicConfig(filename='socket.log', level=logging.DEBUG, format=formatter)

# 従来の出力
logging.info('error{}'.format('outputting error'))
logging.info('warning %s %s' % ('was', 'outputted'))
# logging のみの書き方
logging.info('info %s %s', 'test', 'test')
