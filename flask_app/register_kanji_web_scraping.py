import requests
from bs4 import BeautifulSoup
import jaconv
import sqlite3

EASY_DATABASE = 'easy_kaknji.db'
NORMAL_DATABASE = 'normal_kaknji.db'
HARD_DATABASE = 'hard_kaknji.db'

YOMI_REGIST_SIZE_MAX = 20

easy_levels = ['10', '9', '8', '7', '6', '5']
normal_levels = ['4', '3', '準2']
hard_levels = ['2', '準1', '1']

all_levels = [easy_levels, normal_levels, hard_levels]

easy_levels_url = []
normal_levels_url = []
hard_levels_url = []

url_dic = {
    'easy_levels': easy_levels_url,
    'normal_levels': normal_levels_url,
    'hard_levels': hard_levels_url,
}

# -----------------------------------------------------------------------------------
def register_kanji():
    for kanken_kyuu in easy_levels:
        print(f'----------------{kanken_kyuu}級-----------------')
        response = requests.get(f'https://dictionary.goo.ne.jp/kanji/level/10/')
        response.encoding='utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        kanji_items = soup.find_all('div', class_='kanji_item')

        for kanji_item in kanji_items:
            url = 'https://dictionary.goo.ne.jp' + kanji_item.find('a')['href']
            detail_kanji_response = requests.get(url)
            detail_kanji_response.encoding='utf-8'
            soup2 = BeautifulSoup(detail_kanji_response.text, 'html.parser')
            kanji_block = soup2.find('div', class_='kanji')

            try:
                kanji = kanji_block.find('span').get_text()
            except AttributeError as e:
                print(f"Error while extracting kanji: {e}")
                continue

            # kanji = kanji_block.find('span').get_text()
            print(f'漢字:{kanji}') #一が出力

            reads_block = soup2.find('div', class_='reads')
            reads_yomi_list = reads_block.find_all('span', class_='yomi')
            kanji_yomi_list = []
            for yomi in reads_yomi_list:
                yomi_text = yomi.get_text()
                if('［' not in yomi_text):
                    yomi_text = jaconv.kata2hira(yomi_text)
                    kanji_yomi_list.append(yomi_text)
            print(f'読みリスト:{kanji_yomi_list}')

            #---------------DATABASE-----------------
            EASY_DATABASE = 'easy_kaknji.db'

            con = sqlite3.connect(EASY_DATABASE)

            kanji_yomi_list_size = YOMI_REGIST_SIZE_MAX - len(kanji_yomi_list)
            None_list = [None] * kanji_yomi_list_size
            regist_value_tuple_temp = tuple(kanji_yomi_list + None_list)
            regist_value_tuple = (kanji,) + regist_value_tuple_temp 
            con.execute('INSERT INTO easy_kanjis VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        regist_value_tuple)
            print('登録しました')
            con.commit()
            con.close()


            
            
