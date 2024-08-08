from logging import getLogger, handlers, Formatter, DEBUG, Filter

# class InternalFileFilter(Filter):
#     def filter(self, record):
#         # ログレコードのファイル名が 'internal.py' の場合のみTrueを返す
#         return record.filename == '_internal.py'

def set_logger():
    # 全体のログ設定
    root_logger = getLogger()
    root_logger.setLevel(DEBUG)

    # ログが100KB溜まったらバックアップにして新しいファイルを作る設定
    rotating_handler = handlers.RotatingFileHandler(
        r'./log/app.log',
        mode="a",
        maxBytes=100 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    format = Formatter('%(asctime)s : %(levelname)s : %(filename)s - %(message)s')
    rotating_handler.setFormatter(format)
    root_logger.addHandler(rotating_handler)
    # # internal.py用のハンドラ
    # internal_handler = handlers.RotatingFileHandler(
    #     r'./log/internal.log',
    #     mode="a",
    #     maxBytes=100 * 1024,
    #     backupCount=3,
    #     encoding="utf-8"
    # )
    # internal_handler.setFormatter(format)
    
    # if InternalFileFilter():
    #     root_logger.addHandler(internal_handler)
    # else:
    #     root_logger.addHandler(rotating_handler)
