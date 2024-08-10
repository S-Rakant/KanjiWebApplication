from . import models
from . import db

from flask import Blueprint, jsonify, abort, session, request
from flask_login import current_user, login_required
from sqlalchemy import MetaData, Table
import sqlalchemy
import os
from .models import Kanji, Review, Kanji_ID_Session, Review_KanjiID_Session
import ast
import random
from .myLogger import getLogger
from .local_config import LocalConfig

from flask_wtf.csrf import CSRFError


func = Blueprint('func', __name__, url_prefix='/func')

# logger = getLogger(__name__)


@func.route('/fetch_data_from_kanjiID_session', methods=['GET'])
@func.errorhandler(CSRFError)
def fetch_data_from_kanjiID_session():
    #sessionが切れていたらloginを促す
    if(not current_user.is_authenticated):
        return jsonify({'message': 'Session was expired!'}), 400
    kanjiID = Kanji_ID_Session.query.get(current_user.id)
    kanjiID_arr = set_kanji_id(kanjiID)
    kanji_answer = []
    for id in kanjiID_arr:
        kanji_data = Kanji.query.get(id)
        kanji_answer.append(
            {
            'kanji':kanji_data.kanji,
            'kunyomi_roma':kanji_data.kunyomi_roma,
            'kunyomi_ja':kanji_data.kunyomi_ja,
            'onyomi_roma':kanji_data.onyomi_roma,
            'onyomi_ja':kanji_data.onyomi_ja,
            }
        )
    res = {'kanji_answer':kanji_answer, 'kanji_id':kanjiID_arr}
    # logger.info(f'UserName:[{current_user.username}]--**fetch_data_from_kanjiID_session**')
    return jsonify(res), 200

@func.route('/fetch_data_from_review_sessiom_table', methods=['GET'])
@func.errorhandler(CSRFError)
def fetch_data_from_review_session_table():
    #sessionが切れていたらloginを促す
    if(not current_user.is_authenticated):
        return jsonify({'message': 'Session was expired!'}), 400
    match_id = Review_KanjiID_Session.query.get(current_user.id)
    review_kanji_id_list = [
        match_id.kanji_data0,
        match_id.kanji_data1,
        match_id.kanji_data2,
        match_id.kanji_data3,
        match_id.kanji_data4,
        match_id.kanji_data5,
        match_id.kanji_data6,
        match_id.kanji_data7,
        match_id.kanji_data8,
        match_id.kanji_data9
        ]
    review_kanji_data = []
    for i in range(0, 10):
        if(not review_kanji_id_list[i] == None):
            match_kanji_id = Kanji.query.get(review_kanji_id_list[i])
            temp = {
                'kanji': match_kanji_id.kanji,
                'kunyomi_roma': match_kanji_id.kunyomi_roma,
                'kunyomi_ja': match_kanji_id.kunyomi_ja,
                'onyomi_roma': match_kanji_id.onyomi_roma,
                'onyomi_ja': match_kanji_id.onyomi_ja,
            }
            review_kanji_data.append(temp)
    
    review_kanji_id_list = [i for i in review_kanji_id_list if i != None]
    res = {'review_kanji_id':review_kanji_id_list, 'review_kanji_data':review_kanji_data}
    # logger.info(f'UserName:[{current_user.username}]--**fetch_data_from_review_sessiom_table**')
    return jsonify(res), 200



@func.route('/review_details', methods=['POST'])
@func.errorhandler(CSRFError)
@login_required
def review_details():
    data = request.get_json()
    id = data.get('id')
    match_kanjiID = Kanji.query.get(id)
    data = {
        'kanji_id': match_kanjiID.kanji_id,
        'kanji': match_kanjiID.kanji,
        'kunyomi_roma': match_kanjiID.kunyomi_roma,
        'kunyomi_ja': match_kanjiID.kunyomi_ja,
        'onyomi_roma': match_kanjiID.onyomi_roma,
        'onyomi_ja': match_kanjiID.onyomi_ja,
    }
    # logger.info(f'UserName:[{current_user.username}]--**fetch_review_details_data**')
    return jsonify(data)

@func.route('/delete_kanji_from_review_table', methods=['POST'])
@func.errorhandler(CSRFError)
@login_required
def delete_kanji_from_review_table():
    data = request.get_json()
    kanji_id = int(data.get('id'))
    match_user_id = Review.query.get(current_user.id)
    review_kanji_id_string = match_user_id.review_kanjiID_json
    string_to_list = ast.literal_eval(review_kanji_id_string)
    string_to_list.remove(kanji_id)
    
    db.session.delete(match_user_id)
    miss_kanjiID_table = Review(user_id=current_user.id, review_kanjiID_json=str(string_to_list))
    db.session.add(miss_kanjiID_table)
    db.session.commit()
    # logger.info(f'UserName:[{current_user.username}]--**delete_kanji_from_review_table**')
    return jsonify({'message': 'success'}), 200

@func.route('/delete_checked_kanji_from_review_table', methods=['POST'])
@func.errorhandler(CSRFError)
@login_required
def delete_checked_kanji_from_review_table():
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
        # logger.info(f'UserName:[{current_user.username}]--**delete_checked_kanji_from_review_table**')
        return jsonify({'message': 'update review table'}), 200
    
@func.route('/get_kanjiID_missed_before', methods=['GET'])
@func.errorhandler(CSRFError)
@login_required
def get_kanjiID_missed_before():
    match_user_id = Review.query.get(current_user.id)
    if(match_user_id == None):
        string_to_list = []
    else:
        review_kanji_id_string = match_user_id.review_kanjiID_json
        string_to_list = ast.literal_eval(review_kanji_id_string)
    # logger.info(f'UserName:[{current_user.username}]--**get_kanjiID_missed_before**')
    return jsonify(string_to_list)


def set_kanji_id(kanji_id_query):
    kanjiID_arr = [
        kanji_id_query.kanji_data0,
        kanji_id_query.kanji_data1,
        kanji_id_query.kanji_data2,
        kanji_id_query.kanji_data3,
        kanji_id_query.kanji_data4,
        kanji_id_query.kanji_data5,
        kanji_id_query.kanji_data6,
        kanji_id_query.kanji_data7,
        kanji_id_query.kanji_data8,
        kanji_id_query.kanji_data9,
    ]
    return kanjiID_arr