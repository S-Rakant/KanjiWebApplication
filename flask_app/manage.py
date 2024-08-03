from flask import Blueprint, request, jsonify
from flask_login import current_user
from .models import Ranking, Review
from datetime import datetime

import sqlalchemy
from dotenv import load_dotenv
import os
import ast

load_dotenv()
url = os.getenv('SQLITE_DB_URL')

manage = Blueprint('manage', __name__, url_prefix='/manage')

#jsからuserのscoreと時刻、UserMixinからusernameの情報を受け取り、rankingデータベースに登録する
#呼び出しはjs内からデコレータを用いて行う

@manage.route('/regist_ranking', methods=['GET', 'POST'])
def regist_ranking():
    print('reach!!')
    if(not current_user.is_authenticated):
        return jsonify({'message': 'Session was expired!'}), 400
    engine = sqlalchemy.create_engine(url, echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    data = request.get_json()

    match_id = session.query(Ranking).get(current_user.id)
    if(match_id == None):
        pass
    elif(data.get('score') >= match_id.score):
        session.delete(match_id)
    else:
        return jsonify({'message': 'Ranking Registered Successfully'}), 200
    
    playtime = datetime.now()
    formatted_time = playtime.strftime('%Y-%m-%d %H:%M:%S') #usernameがuniqueな値(primary key)のため、登録時にエラー
    ranking_table = Ranking(user_id=current_user.id, username=current_user.username, score=data.get('score'), playtime=formatted_time)
    session.add(ranking_table)
    session.commit()
    session.close()
    return jsonify({'message': 'Ranking Registered Successfully'}), 200

@manage.route('/regist_mistake_kanjiID', methods=['POST'])
def regist_mistake_kanjiID():
    engine = sqlalchemy.create_engine(url, echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    miss_kanjiID = request.get_json()
    match_id = session.query(Review).get(current_user.id)
    review_kanjiID = []
    if(match_id == None):
        review_kanjiID = miss_kanjiID #list
    else:
        miss_kanji_fromDB_text = match_id.review_kanjiID_json
        #DBに保存されている文字列をlistに変換
        miss_kanji_fromDB_list = ast.literal_eval(miss_kanji_fromDB_text) #list
        #textをset型に変換しmisskanjiID_tableと結合--->currentDB_mistake_kanjiIDに代入
        temp = list(miss_kanjiID)+list(miss_kanji_fromDB_list) #list
        review_kanjiID_set = set(temp) #set
        review_kanjiID = list(review_kanjiID_set)
        session.delete(match_id)
    miss_kanjiID_table = Review(user_id=current_user.id, review_kanjiID_json=str(review_kanjiID))
    session.add(miss_kanjiID_table)
    session.commit()
    session.close()
    print('regist_mistake_kanjIID = ' + str(miss_kanjiID))
    return jsonify({'message': 'regist_mistake KanjiID Successfully!'}), 200

#MEMO
#(rankingに登録されているuseridとcurrent_user.idが一致する行があり∧受け取った方が高い)or(一致する行がない)
# ->ranking tableを更新
#受け取った方が低い
#->更新しない

    