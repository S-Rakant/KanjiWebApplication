from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from flask_wtf.csrf import CSRFError
from .models import Ranking, Review
from datetime import datetime
from .init import db

import sqlalchemy
import ast
from .myLogger import getLogger
from .local_config import LocalConfig


# url = LocalConfig.SQLALCHEMY_DATABASE_URI

manage = Blueprint('manage', __name__, url_prefix='/manage')

# logger = getLogger(__name__)

@manage.route('/regist_ranking', methods=['GET', 'POST'])
@manage.errorhandler(CSRFError)
def regist_ranking():
    update = 'none update'
    if(not current_user.is_authenticated):
        return jsonify({'message': 'Session was expired!'}), 400
    data = request.get_json()

    match_id = Ranking.query.get(current_user.id)
    if(match_id == None):
        pass
    elif(data.get('score') >= match_id.score):
        update = 'update'
        db.session.delete(match_id)
    else:
        return jsonify({'message': 'Ranking Registered Successfully'}), 200
    
    playtime = datetime.now()
    formatted_time = playtime.strftime('%Y-%m-%d %H:%M:%S') #usernameがuniqueな値(primary key)のため、登録時にエラー
    ranking_table = Ranking(user_id=current_user.id, username=current_user.username, score=data.get('score'), playtime=formatted_time)
    db.session.add(ranking_table)
    db.session.commit()
    db.session.close()
    # logger.info(f'UserName:[{current_user.username}]--**regist_ranking - {update}**')
    return jsonify({'message': 'Ranking Registered Successfully'}), 200

@manage.route('/regist_mistake_kanjiID', methods=['POST'])
@manage.errorhandler(CSRFError)
def regist_mistake_kanjiID():
    miss_kanjiID = request.get_json()
    match_id = Review.query.get(current_user.id)
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
        db.session.delete(match_id)
    miss_kanjiID_table = Review(user_id=current_user.id, review_kanjiID_json=str(review_kanjiID))
    db.session.add(miss_kanjiID_table)
    db.session.commit()
    print('regist_mistake_kanjIID = ' + str(miss_kanjiID))
    # logger.info(f'UserName:[{current_user.username}]--**regist_mistake_kanjiID**')
    return jsonify({'message': 'regist_mistake KanjiID Successfully!'}), 200

@manage.route('/delete_correct_answer_kanji_from_review_table', methods=['POST'])
@manage.errorhandler(CSRFError)
@login_required
def delete_correct_answer_kanji_from_review_table():
    match_uer_id = Review.query.get(current_user.id)
    checked_kanjiID_list = request.get_json()
    if(checked_kanjiID_list == []):
        return jsonify({'message': 'no checked kanji'}), 200
    else:
        user_review_kanji_list = match_uer_id.review_kanjiID_json
        string_to_user_review_kanji_list = ast.literal_eval(user_review_kanji_list)
        to_int_checked_kanji_list = []
        for item in checked_kanjiID_list:
            to_int_checked_kanji_list.append(int(item))
        removed_list = [item for item in string_to_user_review_kanji_list if item not in to_int_checked_kanji_list]
        db.session.delete(match_uer_id)
        update_missed_kanjiID = Review(user_id=current_user.id, review_kanjiID_json=str(removed_list))
        db.session.add(update_missed_kanjiID)
        db.session.commit()
        # logger.info(f'UserName:[{current_user.username}]--**delete_correct_answer_kanji_from_review_table**')
        return jsonify({'message': 'update review table'}), 200

    