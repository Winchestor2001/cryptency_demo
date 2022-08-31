//copyLink
function copyToClipboard() {
        var copyText = document.getElementById("ref-link").getAttribute('data-link');
        if (copyText === 'none'){
            return alert("У вас еще нет реф.ссылки");
        };
        navigator.clipboard.writeText(copyText).then(() => {
            alert("Реф.ссылка скопирована");
    });
    }




const btns = document.querySelectorAll(".tab-btn");

const btn_header = document.getElementById('btn_header')

btn_header.addEventListener('click', () => {
    left_content.classList.toggle('active')
})


const setBtn = document.querySelectorAll(".sett-btn");
const articles1 = document.querySelectorAll(".content1");
const setting = document.querySelector(".mySettings");
let left_content = document.querySelector('.left_content')

setting.addEventListener("click", function (e) {
    const id = e.target.dataset.bsTarget
    if (id) {
        // // remove selected from other buttons
        // btns.forEach(function (btn) {
        // btn.classList.remove("active");
        // });
        e.target.classList.add("active");
        // hide other articles
        articles1.forEach(function (article) {
            article.classList.remove("active");
        });

        const element = document.getElementById(id);
        element.classList.add("active");
    }
});


const purchase_text_btn = document.querySelectorAll(('.purchase_text_btn'))
purchase_text_btn.forEach(item => {
    // console.log(item.parentElement.children[1]);
    item.addEventListener('click', (e) => {
        item.parentElement.children[1].classList.toggle('d-none')
        if (item.children[1].style.transform == 'rotate(180deg)') {
            item.children[1].style.transform = 'rotate(0deg)';
        }
        else {
            item.children[1].style.transform = 'rotate(180deg)';
        }
    })
})




let videos_section = document.querySelector(".videos_section");
let video_card = document.querySelectorAll(".video_card");
let intro = document.querySelector(".intro");
video_card.forEach((item) => {
    item.addEventListener("click", function () {
        item.children[0].style.display = "none";
    });
});
// console.log(btn1.childNodes);


let input1 = document.querySelector('.password1')
let input2 = document.querySelector('.password2')
let input3 = document.querySelector('.password3')
let btn1 = document.querySelector('#pass1')
let btn2 = document.querySelector('#pass2')
let btn3 = document.querySelector('#pass3')
let error = document.querySelector('.error')
input2.addEventListener('blur', () => {

    if (input1.value.match(/^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{8,})$/)) {
        // console.log(input1.value);
        // console.log('True');
        error.classList.add('dNone')
    }
    else {
        error.classList.remove('dNone')
        // console.log('Error');
    }
});
let arr = [btn1, btn2, btn3]
arr.forEach(btn => {
    btn.addEventListener('click', () => {
        if (input1.type == 'password') {
            input1.type = 'text'
            input2.type = 'text'
            input3.type = 'text'
            btn1.children[0].classList.add('fa-eye-slash')
            btn1.children[0].classList.remove('a-eye')
            btn2.children[0].classList.add('fa-eye-slash')
            btn2.children[0].classList.remove('a-eye')
            btn3.children[0].classList.add('fa-eye-slash')
            btn3.children[0].classList.remove('a-eye')
        }
        else {
            input1.type = 'password'
            input2.type = 'password'
            input3.type = 'password'
            btn1.children[0].classList.remove('fa-eye-slash')
            btn1.children[0].classList.add('a-eye')
            btn2.children[0].classList.remove('fa-eye-slash')
            btn2.children[0].classList.add('a-eye')
            btn3.children[0].classList.remove('fa-eye-slash')
            btn3.children[0].classList.add('a-eye')
        }
    })
})


let file_get = document.querySelectorAll('.file_get')
file_get.forEach(item =>{
    item.addEventListener('click', function(){
        item.children[0].click()
    });
})
