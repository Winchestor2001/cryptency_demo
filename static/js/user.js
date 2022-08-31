let input1 = document.querySelector('.password1')
let input2 = document.querySelector('.password2')
let btn1 = document.querySelector('#pass1')
let btn2 = document.querySelector('#pass2')
console.log(btn1.childNodes);

let arr = [btn1,btn2]
arr.forEach(btn =>{
    btn.addEventListener('click',()=>{
        if (input1.type=='password') {
            input1.type = 'text'
            input2.type = 'text'
            btn1.children[0].classList.add('fa-eye-slash')
            btn1.children[0].classList.remove('a-eye')
            btn2.children[0].classList.add('fa-eye-slash')
            btn2.children[0].classList.remove('a-eye')
        }
        else{
            input1.type = 'password'
            input2.type = 'password'
            btn1.children[0].classList.remove('fa-eye-slash')
            btn1.children[0].classList.add('a-eye')
            btn2.children[0].classList.remove('fa-eye-slash')
            btn2.children[0].classList.add('a-eye')
        }
    })
})


let error = document.querySelector('.error')
let error1 = document.querySelector('.error1')
let input3 = document.querySelector('.password3')
input1.addEventListener('blur', ()=>{

    if (input1.value.match(/^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{8,})$/)){
        // console.log(input1.value);
        // console.log('True');
        error.classList.add('dNone')
    }
    else{
        error.classList.remove('dNone')
        // console.log('Error');
    }
});
input2.addEventListener('blur', ()=>{

    if (input2.value==input1.value){
        error1.classList.add('dNone')
    }
    else{
        error1.classList.remove('dNone')
    }   
});

input3.addEventListener('blur', ()=>{

    if (input1.value.match(/^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{8,})$/)){
        // console.log(input1.value);
        // console.log('True');
        error.classList.add('dNone')
    }
    else{
        error.classList.remove('dNone')
        // console.log('Error');
    }
});

