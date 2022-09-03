let input1 = document.querySelector('.password1')
let input2 = document.querySelector('.password2')
let input3 = document.querySelector('.password3')

let error = document.querySelector('.error')
let error1 = document.querySelector('.error1')
input2.addEventListener('input', () => {
    if (input2.value.match(/^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{8,})$/)) {
        error.classList.add('dNone')
        input2.style.background = '#67e088'
    }
    else {
        error.classList.remove('dNone')
         input2.style.background = '#f76060'
    }
});
input3.addEventListener('input', ()=>{

    if (input3.value==input1.value){
        error1.classList.add('dNone')
        input3.style.background = '#67e088'
    }
    else{
        error1.classList.remove('dNone')
        input3.style.background = '#f76060'
    }
});

let btn1 = document.querySelector('#pass1')
let btn2 = document.querySelector('#pass2')
let btn3 = document.querySelector('#pass3')
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