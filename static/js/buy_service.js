let get_file = document.querySelector('.get_file')
let get_file_input = document.querySelector('#get_file_input')
get_file.addEventListener('click', function(){
    get_file_input.click()
});
function clickInput(){
    let get_file_input = document.querySelector('#get_file_input')
    let send_file_btn = document.querySelector('#send_ava')
    send_file_btn.submit()
}