from flask_app import create_app
import sqlalchemy
from sqlalchemy import MetaData, Table
from flask_app import models


KANJI_DB = 'flask_app/save_db/kanji.db'
url = 'sqlite:////home/sousuke/projects/PythonApp/kanji_app/instance/sqlite.db'

app = create_app()
app.app_context().push() #Flaskのアプリケーションコンテキストを有効化 --? データベースへの接続(session)が可能になる

engine = sqlalchemy.create_engine(url, echo=False)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()
#------------------sqlite.dbから指定のテーブル自体を削除----------------------#
metadata = MetaData()
DROP_TABLE_NAME = 'kanjiID_table' #table name to drop in sqlite.db

table_to_drop = Table(DROP_TABLE_NAME, metadata, autoload_with=engine)
table_to_drop.drop(engine)
# #-----------------------------------------------------------------------#

# #------------------sqlite.dbから指定のテーブルデータのみを削除----------------------#
# DELETE_TABLE_NAME = 'all_kanji' #table name to delete in sqlite.db

# session.query(models.Kanji).delete()
# session.commit()
#-----------------------------------------------------------------------#



#------------------kanji.db --> sqlite.db kanjiにコピー-------------------#
# conn = sqlite3.connect(KANJI_DB)
# cursor = conn.cursor()
# items = cursor.execute('SELECT * FROM prob_kanjis')
# i = 1
# for item in items:
#     Kanji_table = models.Kanji(kanji_id = i, kanji=item[0], kunyomi_roma=item[1], kunyomi_ja=item[2], onyomi_roma=item[3], onyomi_ja=item[4])
#     session.add(Kanji_table)
#     i+=1
# session.commit()
# conn.close()
#-----------------------------------------------------------------------#

#==================sqlite.db kanjiにkanji_idを追加----------------------#
# session = db.session()
# metadata = MetaData()
# metadata.reflect(bind=db.engine)
# table = metadata.tables['kanji']
# query = table.select()
# items = session.execute(query)
# print(items)
#--------------------------------------------------------------------------#

