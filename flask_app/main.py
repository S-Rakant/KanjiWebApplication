from flask_app import create_app
from . import models
from . import register_kanji as reg


from flask import render_template, request, abort
from flask import jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
import sqlite3
from sqlalchemy import desc
import sqlalchemy
import random
from dotenv import load_dotenv
import os
import ast
from .myLogger import set_logger, getLogger


from .models import Review, Kanji

load_dotenv()
url = os.getenv('SQLITE_DB_URL')


main = Blueprint('main', __name__)

set_logger()
logger = getLogger(__name__)

@main.route('/')
@login_required
def index():
    engine = sqlalchemy.create_engine(url, echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    #10位までのuserのスコアを取得
    ranking_infomations = models.Ranking.query.order_by(desc(models.Ranking.score)).limit(10)

    rank = 1
    ranking_data = []
    for row in ranking_infomations:
        ranking_data.append(
            {'rank':rank, 'username': row.username, 'score': row.score, 'playtime': row.playtime}
        )
        rank += 1

    
    select = session.query(models.Kanji_ID_Session).get(current_user.id)
    if(select != None):
        session.delete(select)

    #create kanjiID session for quiz
    st_point = 0
    fin_point = 1235
    range_size = 10
    kanji_id_arr = random_kanjiID_select(st_point, fin_point, range_size)
    kanji_id_session = models.Kanji_ID_Session(
        user_id = current_user.id,
        kanji_data0 = kanji_id_arr[0],
        kanji_data1 = kanji_id_arr[1],
        kanji_data2 = kanji_id_arr[2],
        kanji_data3 = kanji_id_arr[3],
        kanji_data4 = kanji_id_arr[4],
        kanji_data5 = kanji_id_arr[5],
        kanji_data6 = kanji_id_arr[6],
        kanji_data7 = kanji_id_arr[7],
        kanji_data8 = kanji_id_arr[8],
        kanji_data9 = kanji_id_arr[9],
        )
    session.add(kanji_id_session)
    session.commit()

    #create kanjiID session for review
    selected_review_kanjiID = []
    review_kanji_id_list = []
    match_id_review_table = session.query(models.Review).get(current_user.id)
    if(not match_id_review_table == None):
        review_kanji_id_string = match_id_review_table.review_kanjiID_json
        review_kanji_id_list = ast.literal_eval(review_kanji_id_string)
    else:
        review_table = models.Review(user_id = current_user.id, review_kanjiID_json = '[]')
        session.add(review_table)
        session.commit()

    for i in range(0, 10): #最大で10個idを格納,10よりも少ない場合は空いた場所にNoneを格納
        if(len(review_kanji_id_list) > 0):
            select_id = random.choice(review_kanji_id_list)
            selected_review_kanjiID.append(select_id)
            review_kanji_id_list.remove(select_id)
        else:
            selected_review_kanjiID.append(None)

    match_id_review_kanjiID_session = session.query(models.Review_KanjiID_Session).get(current_user.id)
    if(not match_id_review_kanjiID_session == None):
        session.delete(match_id_review_kanjiID_session)

    review_kanjiID_session_table = models.Review_KanjiID_Session(
        user_id = current_user.id,
        kanji_data0 = selected_review_kanjiID[0],
        kanji_data1 = selected_review_kanjiID[1],
        kanji_data2 = selected_review_kanjiID[2],
        kanji_data3 = selected_review_kanjiID[3],
        kanji_data4 = selected_review_kanjiID[4],
        kanji_data5 = selected_review_kanjiID[5],
        kanji_data6 = selected_review_kanjiID[6],
        kanji_data7 = selected_review_kanjiID[7],
        kanji_data8 = selected_review_kanjiID[8],
        kanji_data9 = selected_review_kanjiID[9],
    )
    session.add(review_kanjiID_session_table)
    session.commit()
    session.close()

    logger.info(f'UserName:[{current_user.username}]--**Index**')
    return render_template(
        'index.html',
        ranking_info = ranking_data,
    )

@main.route('/Infomation')
def infomation():
    logger.info(f'UserName:[{current_user.username}]--**Infomation**')
    return render_template(
        'infomation.html'
    )

@main.route('/Support')
def support():
    logger.info(f'UserName:[{current_user.username}]--**Support**')
    return render_template(
        'support.html'
    )

@main.route('/ReviewList')
@login_required
def review():
    engine = sqlalchemy.create_engine(url, echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    match_id_review = session.query(Review).get(current_user.id)
    miss_kanji_data = []
    if(match_id_review != None):
        miss_kanji_fromDB_list = ast.literal_eval(match_id_review.review_kanjiID_json)
        #間違えた漢字IDの「漢字の詳細」を辞書形式でmiss_kanji_dataに格納
        #render_templateの引数に指定
        for kanji_id in miss_kanji_fromDB_list:
            match_id_kanji = session.query(Kanji).get(kanji_id)
            miss_kanji_data.append({
                'kanji_id': match_id_kanji.kanji_id,
                'kanji': match_id_kanji.kanji,
                'kunoymi_roma': match_id_kanji.kunyomi_roma,
                'kunyomi_ja': match_id_kanji.kunyomi_ja,
                'onyomi_roma': match_id_kanji.onyomi_roma,
                'onyomi_ja': match_id_kanji.onyomi_ja,
                })
    logger.info(f'UserName:[{current_user.username}]--**Review_List**')
    return render_template(
        'review.html',
        miss_kanji_data=miss_kanji_data,
    )

def random_kanjiID_select(a, b, k):
    result_arr = []
    while(len(result_arr) < k):
        v = random.randint(a, b)
        if (v not in result_arr):
            result_arr.append(v)
    print(result_arr)
    return result_arr