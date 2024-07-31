import http.client
import urllib.parse
import pandas as pd
import json
import sqlite3
from dotenv import load_dotenv #dotenvで.envから環境変数を読み込み
import os
import random

from . import db, app
from sqlalchemy import MetaData, select, insert, delete, func

load_dotenv()

kanji_alive_api_url = os.getenv('KANJIALIVE_API_URL')
x_rapid_key = os.getenv('X-RAPID_KEY')
file_path_kanji_data = os.getenv('FILEPATH_KANJI_DATA')


PROB_KANJI_DATABASE = 'kanji.db'
USER_TO_SOLVE_PROB_DATABASE = 'user_to_solve_prob.db'


def get_kanji_from_excel():
    file_path = file_path_kanji_data
    df = pd.read_excel(file_path, usecols="A")
    a_colum_list = df.iloc[:, 0].tolist()
    return a_colum_list
    # print(a_colum_list)

#すべての漢字を登録
def register_prob_kanji():
    conn = http.client.HTTPSConnection(kanji_alive_api_url)

    headers = {
        'x-rapidapi-key': x_rapid_key,
        'x-rapidapi-host': kanji_alive_api_url
    }

    kanji_list = get_kanji_from_excel()

    con = sqlite3.connect(PROB_KANJI_DATABASE)

    for kanji in kanji_list[715:]: #request is up to 1000 per hour
        encoded_kanji = urllib.parse.quote(kanji)
        conn.request("GET", f"/api/public/kanji/{encoded_kanji}", headers=headers)

        res = conn.getresponse()
        data = res.read()
        str_data = data.decode("utf-8")
        json_to_dict_data = json.loads(str_data)
        kunyomi_roma = json_to_dict_data["kunyomi"]
        kunyomi_ja = json_to_dict_data["kunyomi_ja"]
        onyomi_roma = json_to_dict_data["onyomi"]
        onyomi_ja = json_to_dict_data["onyomi_ja"]
        con.execute("INSERT INTO prob_kanjis VALUES (?, ?, ?, ?, ?)",
                    (kanji, kunyomi_roma, kunyomi_ja, onyomi_roma, onyomi_ja))
        print(f'{kanji}を登録しました。')
        con.commit()
    con.close() #データベースに全ての漢字を登録したらclose()


#Userが各ラウンドごとに解く10個の漢字をランダムに抽出し登録
# def register_user_to_solve_kanjis():
#     with app.app_context():
#         metadata = MetaData()
#         metadata.reflect(bind=db.engine)
#         kanji_table = metadata.tables['kanji']
#         select_query = select(kanji_table).order_by(func.random()).limit(10)
#         result = db.session.execute(select_query).fetchall()
#         solve_table = metadata.tables['solve']
#         #delete current solve table
#         delete_query = delete(solve_table)
#         db.session.execute(delete_query)
#         #regist 10 kanjis
#         for item in result:
#             insert_query = insert(solve_table).values(
#                 kanji=item.kanji,
#                 kunyomi_roma=item.kunyomi_roma,
#                 kunyomi_ja=item.kunyomi_ja,
#                 onyomi_roma=item.onyomi_roma,
#                 onyomi_ja=item.onyomi_ja
#                 )
#             db.session.execute(insert_query)
#         db.session.commit()
        

def fetch_random_data_from_db(db_name, table_name, num):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT {num}")
    random_data = cursor.fetchall()
    return random_data
    
#----------------------------------------------------------------------------------------------#
# def regist_to_sqlitedb():


if __name__ == '__main__':
    register_prob_kanji()