const start_button = document.getElementById('start-button');
const debug = document.getElementById('debug');
const top_container = document.getElementById('top_container');
const game_container = document.getElementById('game_answer_container');
const syutudai_kanji = document.getElementById('syutudai_kanji');

const study_mode = document.getElementById('study_mode');

const answer_block = document.getElementById('answer_block');
const explanation = document.getElementById('explanation_block');

const kunyomi_roma = document.getElementById('kunyomi_roma');
const kunyomi_ja = document.getElementById('kunyomi_ja');
const onyomi_roma = document.getElementById('onyomi_roma');
const onyomi_ja = document.getElementById('onyomi_ja');

const answer_form = document.getElementById('answer_form');
const next_prob_button = document.getElementById('next_prob_button');
const result_container = document.getElementById('result_container');

const return_to_home_button = document.getElementById('return_to_home');

const mistake = document.getElementById('mistake');




let prob_counter = 0;
let correct_counter = 0;  
let correct_rate = 0;
let all_kanji_id; //10個の漢字IDを保存しておく
let miss_kanji_id_arr; //ユーザが間違えた漢字IDを保存しておく
let missed_before_kanji_id = [];
let selected_game_mode = ''; //game_modeを保存しておく
let AMOUNT_PROBLEM = 0;
let correct_answer_kanji_id_for_review_mode = []

var csrf_token = $('meta[name="csrf-token"]').attr('content');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});



const game = async() => {
    console.log('gameに入りました')
    prob_counter = 0;
    correct_counter = 0;
    correct_rate = 0;
    all_kanji_id = [];
    miss_kanji_id_arr = [];
    missed_before_kanji_id = [];
    correct_answer_kanji_id_for_review_mode = [];
    const game_mode = document.querySelector('input[name="game-mode-select"]:checked'); //mode_select中のチェックが付いたものを抽出

    if(game_mode == null){
        window.alert('Select Game Mode');
    }
    else{
        game_mode_name(game_mode);
        await set_missed_before_kanji_id(); //過去に間違えたことのある漢字IDを取得しmissed_before_kanji_idに格納
        if(selected_game_mode == 'quiz'){
            AMOUNT_PROBLEM = 10;
        }
        updateMainAnswerContent();

        game_container.classList.remove('hidden');
        top_container.classList.add('hidden');
        result_container.classList.add('hidden');        
    }
};

const set_missed_before_kanji_id = () =>{
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "GET",
            url: "func/get_kanjiID_missed_before",
            success: function (response) {
                resolve(response);
                console.log(response);
                missed_before_kanji_id = response;
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}

/**---------------------------------------ここから----------------------------------------
 * 問題番号の漢字データをロードするload_kanji_dataを作成
 * ->load_kanji_dataで問題番号の漢字データ(漢字と読み)を取得する。
 * ->updateMainAnswerContent,updateExplanationContent毎に/func/にrequest
 * ->json形式で保持
 */
const load_kanji_data = () => {
    console.log('load kanji data' + selected_game_mode);
    if(selected_game_mode == 'quiz'){
        return fetch('/func/fetch_data_from_kanjiID_session')
        .then(response => {
            if(response.ok){
                return response.json();
            }
            if(response.status = 400){
                console.log('Error 400');
                window.alert('Your session was expired! Please reload and login again')
                throw new Error(response.statusText); //警告メッセージを表示させてlogin.htmlに遷移させたい
            }
        })
        .then(data => {
            console.log(data.kanji_answer[prob_counter]);
            prob_num_data = data.kanji_answer[prob_counter];
            all_kanji_id = data.kanji_id;
            console.log('kanji_id = ' + all_kanji_id)
            return prob_num_data;
        })
    }
    else if(selected_game_mode == 'review'){
        return fetch('/func/fetch_data_from_review_sessiom_table')
        .then(response => {
            if(response.ok){
                return response.json();
            }
            if(response.status = 400){
                console.log('Error 400');
                window.alert('Your session was expired! Please reload and login again')
                throw new Error(response.statusText); //警告メッセージを表示させてlogin.htmlに遷移させたい
            }
        })
        .then(data => {
            console.log('review_kanji_id_list = ' + data.review_kanji_id);
            console.log('review_kanji_data = ' + JSON.stringify(data.review_kanji_data));
            AMOUNT_PROBLEM = data.review_kanji_id.length; //問題数をreview_tableに保存されている漢字の数、max=10に設定
            if(data.review_kanji_id.length > 0){
                prob_num_data = data.review_kanji_data[prob_counter];
                all_kanji_id = data.review_kanji_id;
                return prob_num_data;
            }
            else if(data.review_kanji_id.length == 0){
                prob_num_data = null;
                all_kanji_id = [];
                console.log('kanji_id = ' + all_kanji_id);
                return prob_num_data;
            }
        })
    }
}
/**----------------------------------------------------------------------------------- */

const game_mode_name = (game_mode) => {
    let result = '';
    if(game_mode.value == 'quiz'){
        selected_game_mode = 'quiz'
        result = 'Kanji Quiz';
    }
    else if(game_mode.value == 'review'){
        selected_game_mode = 'review';
        result = 'Review';
    }
       
    change_mode_title(result);
};
            
const change_mode_title = (result) => {
    study_mode.textContent = result;
};


const toHiragana = t => {
    const katakanaRegex = /[\u30A1-\u30FA]/g;
    return t.replace(katakanaRegex, x => String.fromCharCode(x.charCodeAt(0) - 0x60));
  };

const updateMainAnswerContent = async() => {
    console.log('updateMainAnswerContentに入りました');
    prob_num_data = await load_kanji_data(); //非同期処理
    console.log('prob_num_data = ' + prob_num_data);
    if(prob_num_data != null){ //reviewの場合に最初の問題で、nullとなる可能性がある
        kanji = prob_num_data['kanji'];
        console.log('load_kanjiからデータ:' + kanji + 'を受け取りました');
        const question_num = document.getElementById('question_number');
        question_num.textContent = prob_counter+1; //〇問目を更新
        syutudai_kanji.textContent = kanji; //出題漢字を更新
        console.log('kanji_id = ' + all_kanji_id[prob_counter])
        if(missed_before_kanji_id.includes(all_kanji_id[prob_counter])){
            mistake.classList.remove('hidden');
        }
        else{
            mistake.classList.add('hidden');
            console.log('過去に間違えた漢字ではありません.')
        }
        
        answer_block.classList.remove('hidden'); //漢字の説明を隠し、送信ボタンを表示
        explanation.classList.add('hidden');
    }
    else{ //prob_numがnullの場合
        show_result('review_null');
    }
};

const updateExplanationContent = async(event) => {
    console.log('updateExplanationContentに入りました')
    event.preventDefault(); //submitでページ遷移されるのを防止
    let answer_value = document.getElementById('input_answer')
    let user_answer = answer_value.value
    answer_form.reset();
    prob_num_data = await load_kanji_data(selected_game_mode); //非同期処理

    if(prob_num_data['onyomi_ja'] == ''){
        prob_num_data['onyomi_hiragana'] = '';    
    }
    else{
        prob_num_data['onyomi_hiragana'] = toHiragana(prob_num_data['onyomi_ja']); //音読みのカタカナ読みを平仮名にしたもの追加
    }
    check_answer(prob_num_data, user_answer);
    update_details(kunyomi_roma, prob_num_data['kunyomi_roma']);
    update_details(kunyomi_ja, prob_num_data['kunyomi_ja']);
    update_details(onyomi_roma, prob_num_data['onyomi_roma']);
    update_details(onyomi_ja, prob_num_data['onyomi_ja']);

    answer_block.classList.add('hidden'); //送信ボタンを隠す
    explanation.classList.remove('hidden'); //漢字の説明を表示
};

const update_details = (updated, updator) =>{
    if(updator == 'n/a' || updator == ''){
        updated.textContent = '<None>';
    }
    else{
        updated.textContent = updator;
    }
}

const check_answer = (prob_num_data, user_answer) =>{
    const correct_or_incorrect = document.getElementById('correct_or_incorrect');
    if(user_answer == ''){
        correct_or_incorrect.classList.remove('correct')
        correct_or_incorrect.classList.add('incorrect')
        correct_or_incorrect.textContent = 'Incorrect answer';
        console.log('miss ID = ' + all_kanji_id[prob_counter]);
        miss_kanji_id_arr.push(all_kanji_id[prob_counter]);
        console.log('now miss kanjiID = ' + miss_kanji_id_arr);
        return;
    }
    result = [];
    let kunyomi_ja = prob_num_data['kunyomi_ja']; //"やわ、やわらぐ、やわらげる、なご、なごむ、なごやか"
    let onyomi_ja_katakana = prob_num_data['onyomi_ja']; //"ワ、オ"
    let onyomi_ja_hiragana = prob_num_data['onyomi_hiragana']; //"わ、お"

    let kunyomi_roma = prob_num_data['kunyomi_roma'];
    let onyomi_roma = prob_num_data['onyomi_roma']

    let divided_string_list_ja = kunyomi_ja.split("、").concat(onyomi_ja_katakana.split("、")).concat(onyomi_ja_hiragana.split("、"));
    let answer_data_ja = divided_string_list_ja.filter(item => (item != '' && item != 'n/a'));
    let divided_string_list_roma = kunyomi_roma.split(",").concat(onyomi_roma.split(","));
    let nospace_divided_string_list_roma = divided_string_list_roma.map(function(item){
        return item.replace(/\s+/g, '');
    });
    let answer_data_roma = nospace_divided_string_list_roma.filter(item => (item != '' && item != 'n/a'));
    let answer_data = answer_data_ja.concat(answer_data_roma);
    console.log('answer_data = ' + answer_data);
    console.log('user_answer = ' + user_answer);
    if(answer_data.includes(user_answer)){ //correct answer
        correct_or_incorrect.classList.remove('incorrect')
        correct_or_incorrect.classList.add('correct')
        correct_or_incorrect.textContent = 'correct answer!!';
        correct_counter++;
        console.log('correct_counter = ' + correct_counter); //for debug
        console.log('now miss kanjiID = ' + miss_kanji_id_arr);
        if(selected_game_mode == 'review'){
            correct_answer_kanji_id_for_review_mode.push(all_kanji_id[prob_counter]);
        }
    }
    else{ //wrong answer
        correct_or_incorrect.classList.remove('correct')
        correct_or_incorrect.classList.add('incorrect')
        correct_or_incorrect.textContent = 'Incorrect answer';
        console.log('miss ID = ' + all_kanji_id[prob_counter]);
        miss_kanji_id_arr.push(all_kanji_id[prob_counter]);
        console.log('now miss kanjiID = ' + miss_kanji_id_arr);
    }
};


const trans_next_prob = () => {
    prob_counter++; //問題番号をインクリメント
    if(prob_counter < AMOUNT_PROBLEM){ //fordebug
        updateMainAnswerContent();
    }
    else{
        show_result('not_null');
    }
};

const show_result = async(whether_null) => {
    if(whether_null == 'not_null'){
        const correct_answer_rate = document.getElementById('correct_answer_rate');
        correct_answer_rate.textContent = correct_counter*10;
        correct_rate = correct_counter*10; //grobalに登録
        console.log('correct_answer_kanji_id_for_review_mode = ' + correct_answer_kanji_id_for_review_mode);
    
        result_container.classList.remove('hidden');
        game_container.classList.add('hidden');
        if(selected_game_mode == 'quiz'){
            let data = {
                'score' : correct_rate
            }
            console.log(JSON.stringify(data))
            /**
             * flask-WTFを使用し、CSRF対策を行う場合,
             * AjaxのPOSTリクエストにCSRFトークンを含める必要がある.
             * トークンがないと400エラーとなる
             */
            $.ajax({
                type: "POST",
                url: "manage/regist_ranking",
                data: JSON.stringify(data),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                // headers: {
                //     'X-CSRFToken': $('meta[name=csrf-token]').attr('content')
                // },
                success: function (response) {
                    console.log('return into ajax from regist_ranking', response);
                },
                error: function (xhr, status, error) {
                    window.alert('Your session was expired! Please reload and login again');
                    console.log('regist_ranking_Error', error);
                    console.log('XHR:', xhr);
                    console.log('Status:', status)
                }
            });
            //review_tableを更新
            update_review_table();
        }
        else if(selected_game_mode == 'review'){
            console.log('answer_kanji_id_list_for_review = ' + correct_answer_kanji_id_for_review_mode)
            $.ajax({
                type: "POST",
                url: "manage/delete_correct_answer_kanji_from_review_table",
                data: JSON.stringify(correct_answer_kanji_id_for_review_mode),
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function (response) {
                    console.log('delete_correct_answer_kanji_from_review_table', response);
                },
                error: function (xhr, status, error) {
                    window.alert('Your session was expired! Please reload and login again');
                    console.log('delete_correct_answer_kanji_from_review_table_Error', error);
                    console.log('XHR:', xhr);
                    console.log('Status:', status)
                }
            });
        }
    }
    else if(whether_null == 'review_null'){
        const score_literal_container = document.getElementById('score_literal_container');
        score_literal_container.textContent = 'You have not made any mistakes yet!'
        result_container.classList.remove('hidden');
        game_container.classList.add('hidden');
        console.log('correct_answer_kanji_id_for_review_mode = ' + correct_answer_kanji_id_for_review_mode);
    }
}

const update_review_table = () => {
    try{
        $.ajax({
            type: "POST",
            url: "manage/regist_mistake_kanjiID",
            data: JSON.stringify(miss_kanji_id_arr),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            // headers: {
            //     'X-CSRFToken': $('meta[name=csrf-token]').attr('content')
            // },
            error: function (xhr, status, error) {
                window.alert('Your session was expired! Please reload and login again');
                console.log('regist_mistake_kanjiID_Error', error);
                console.log('XHR:', xhr);
                console.log('Status:', status)
            },
            success: function (response) {
                console.log('response from regist_mistake_kanjiID', response);
            }
        });
    }catch(error){
        console.log('Error', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    start_button.addEventListener('click', function() {
        game();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    answer_form.addEventListener('submit', function(event) {
        updateExplanationContent(event);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    next_prob_button.addEventListener('click', function() {
        trans_next_prob();
    });
});
