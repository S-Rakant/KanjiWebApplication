from . import models
from . import db

from flask import Blueprint, jsonify, abort, session, request
from flask_login import current_user, login_required
import sqlite3
from sqlalchemy import MetaData, Table
import sqlalchemy
from dotenv import load_dotenv
import os
from .models import Kanji

load_dotenv()
url = os.getenv('SQLITE_DB_URL')

func = Blueprint('func', __name__, url_prefix='/func')


@func.route('/fetch_data_from_kanjiID_session', methods=['GET'])
def fetch_data_from_kanjiID_session():
    #sessionが切れていたらloginを促す
    if(not current_user.is_authenticated):
        return jsonify({'message': 'Session was expired!'}), 400
    engine = sqlalchemy.create_engine(url, echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    kanjiID = session.query(models.Kanji_ID_Session).get(current_user.id)
    kanjiID_arr = set_kanji_id(kanjiID)
    kanji_answer = []
    for id in kanjiID_arr:
        #kanjiID_sessionのkanjiIDと一致する漢字をall_kanjiから取得
        kanji_data = session.query(models.Kanji).get(id)
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
    return jsonify(res)

@func.route('/review_details', methods=['POST'])
@login_required
def review_details():
    data = request.get_json()
    id = data.get('id')
    print(id)
    engine = sqlalchemy.create_engine(url, echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    match_kanjiID = session.query(Kanji).get(id)
    data = {
        'kanji_id': match_kanjiID.kanji_id,
        'kanji': match_kanjiID.kanji,
        'kunyomi_roma': match_kanjiID.kunyomi_roma,
        'kunyomi_ja': match_kanjiID.kunyomi_ja,
        'onyomi_roma': match_kanjiID.onyomi_roma,
        'onyomi_ja': match_kanjiID.onyomi_ja,
    }

    return jsonify(data)

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