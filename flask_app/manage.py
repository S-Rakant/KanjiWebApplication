from flask import Blueprint, request, jsonify
from flask_login import current_user
from .models import Ranking
from datetime import datetime

import sqlalchemy
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv('SQLITE_DB_URL')

manage = Blueprint('manage', __name__, url_prefix='/manage')

#jsからuserのscoreと時刻、UserMixinからusernameの情報を受け取り、rankingデータベースに登録する
#呼び出しはjs内からデコレータを用いて行う

@manage.route('/regist_ranking', methods=['GET', 'POST'])
def regist_ranking():
    print('reach!!')
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


#MEMO
#(rankingに登録されているuseridとcurrent_user.idが一致する行があり∧受け取った方が高い)or(一致する行がない)
# ->ranking tableを更新
#受け取った方が低い
#->更新しない

    