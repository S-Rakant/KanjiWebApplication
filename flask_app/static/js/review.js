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


    const display_kanji_details = async(value) =>{
        console.log(value)
        data = await get_kanji_details_from_id(value);
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
})