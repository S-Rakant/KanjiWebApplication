
document.addEventListener('DOMContentLoaded', function(){
    const details_button = document.querySelectorAll('.details_button');
    const table_contents = document.getElementById('top_container');
    const details_preview_contents = document.getElementById('details_preview');
    const return_review_list = document.getElementById('return_review_list');
    
    const kanji = document.getElementById('kanji');
    const kunyomi_roma = document.getElementById('kunyomi_roma');
    const kunyomi_ja = document.getElementById('kunyomi_ja');
    const onyomi_roma = document.getElementById('onyomi_roma');
    const onyomi_ja = document.getElementById('onyomi_ja');
    
    const delete_kanji_from_review_table_button = document.getElementById('delete_kanji_from_review_table');
    const exclude_button = document.getElementById('exclude_button');
    
    let current_pointed_kanjiID;
    
    var csrf_token = $('meta[name="csrf-token"]').attr('content');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
    
    const display_kanji_details = async(value) =>{
        console.log(value)
        data = await get_kanji_details_from_id(value);
        current_pointed_kanjiID = value;
        console.log(data);
        modify_none_data = modify_none(data);
        kanji.textContent = modify_none_data.kanji;
        kunyomi_roma.textContent = modify_none_data.kunyomi_roma;
        kunyomi_ja.textContent = modify_none_data.kunyomi_ja;
        onyomi_roma.textContent = modify_none_data.onyomi_roma;
        onyomi_ja.textContent = modify_none_data.onyomi_ja;

        add_hidden(table_contents);
        remove_hidden(details_preview_contents);
    }

    const get_kanji_details_from_id = (id) => {
        return new Promise((resolve, reject) => {
            let data = { 'id': id };
            $.ajax({
                type: "POST",
                url: "func/review_details",
                data: JSON.stringify(data),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                // headers: {
                //     'X-CSRFToken': $('meta[name=csrf-token]').attr('content')
                // },
                success: function (response) {
                    resolve(response);
                },
                error: function (error) {
                    reject(error);
                }
            });
        });
    }

    const modify_none = (data) => {
        res = data;
        key_arr = Object.keys(res);
        for(key of key_arr){
            console.log(res[key])
            if(res[key] == 'n/a' || res[key] == ''){
                res[key] = '<None>'
            }
        }
        return res;
    }

    const delete_kanji_from_review_table = () =>{
        return new Promise((resolve, reject) => {
            let data = { 'id': current_pointed_kanjiID };
            $.ajax({
                type: "POST",
                url: "func/delete_kanji_from_review_table",
                data: JSON.stringify(data),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                // headers: {
                //     'X-CSRFToken': $('meta[name=csrf-token]').attr('content')
                // },
                success: function (response) {
                    resolve(response);
                    location.reload();
                },
                error: function (error) {
                    reject(error);
                }
            });
        });
    }

    const exclude_selected_kanji = () => {
        const selected_kanji = document.querySelectorAll('input[name=user_check_in_review]:checked');
        send = [];
        for(let i=0; i<selected_kanji.length; i++){
            send.push(selected_kanji[i].value);
        }
        console.log(send);
        return new Promise((resolve, reject) => {
            $.ajax({
                type: "POST",
                url: "func/delete_checked_kanji_from_review_table",
                data: JSON.stringify(send),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                // headers: {
                //     'X-CSRFToken': $('meta[name=csrf-token]').attr('content')
                // },
                success: function (response) {
                    resolve(response);
                    location.reload();
                },
                error: function (error) {
                    reject(error);
                }
            });
        })
    }
    
    const add_hidden = (element) =>{
        element.classList.add('hidden');
    }
    
    const remove_hidden = (element) =>{
        element.classList.remove('hidden');
    }
    
    details_button.forEach(function(element){
        element.addEventListener('click', function(){
            display_kanji_details(element.value);
        })
    });

    return_review_list.addEventListener('click', function(){
        add_hidden(details_preview_contents);
        remove_hidden(table_contents);
    })

    delete_kanji_from_review_table_button.addEventListener('click', function(){
        delete_kanji_from_review_table();
    })

    exclude_button.addEventListener('click', function(){
        exclude_selected_kanji();
    })
})