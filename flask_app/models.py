from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


from .init import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password_hash = db.Column(db.String(128))

    #パスワードをハッシュ化
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #入力されたパスワードが登録されたパスワードハッシュと一致するかを確認
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Kanji(db.Model):
    __tablename__ = 'all_kanji'
    kanji_id = db.Column(db.Integer, primary_key = True)
    kanji = db.Column(db.String)
    kunyomi_roma = db.Column(db.String)
    kunyomi_ja = db.Column(db.String)
    onyomi_roma = db.Column(db.String)
    onyomi_ja = db.Column(db.String)

class Ranking(db.Model):
    __tablename__ = 'ranking'
    user_id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String, nullable = False)
    score = db.Column(db.Integer, nullable = False)
    playtime = db.Column(db.String, nullable = False)

class Kanji_ID_Session(db.Model):
    __tablename__ = 'kanjiID_session'
    user_id = db.Column(db.Integer, primary_key = True, nullable = False)

    #all_kanji tableのkanji_idをユーザごとに保存
    kanji_data0 = db.Column(db.Integer, nullable = False)
    kanji_data1 = db.Column(db.Integer, nullable = False)
    kanji_data2 = db.Column(db.Integer, nullable = False)
    kanji_data3 = db.Column(db.Integer, nullable = False)
    kanji_data4 = db.Column(db.Integer, nullable = False)
    kanji_data5 = db.Column(db.Integer, nullable = False)
    kanji_data6 = db.Column(db.Integer, nullable = False)
    kanji_data7 = db.Column(db.Integer, nullable = False)
    kanji_data8 = db.Column(db.Integer, nullable = False)
    kanji_data9 = db.Column(db.Integer, nullable = False)

class Review(db.Model):
    __tablename__ = 'review_table'
    user_id = db.Column(db.Integer, primary_key = True, nullable = False)
    review_kanjiID_json = db.Column(db.String) #間違えた漢字IDをText型で保存.処理するときはJSON型として処理可能.

class Review_KanjiID_Session(db.Model):
    __tablename__ = 'review_kanjiID_session'
    user_id = db.Column(db.Integer, primary_key = True, nullable = False)
    kanji_data0 = db.Column(db.Integer, nullable = True)
    kanji_data1 = db.Column(db.Integer, nullable = True)
    kanji_data2 = db.Column(db.Integer, nullable = True)
    kanji_data3 = db.Column(db.Integer, nullable = True)
    kanji_data4 = db.Column(db.Integer, nullable = True)
    kanji_data5 = db.Column(db.Integer, nullable = True)
    kanji_data6 = db.Column(db.Integer, nullable = True)
    kanji_data7 = db.Column(db.Integer, nullable = True)
    kanji_data8 = db.Column(db.Integer, nullable = True)
    kanji_data9 = db.Column(db.Integer, nullable = True)