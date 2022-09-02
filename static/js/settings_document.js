let file_get = document.querySelector('.file_get')
let file_get2 = document.querySelector('.file_get2')
let filea = document.querySelector('.file_inp');
let filea2 = document.querySelector('.file_inp2');
const reader = new FileReader();
let preview = document.querySelector('.file_img');
let preview2 = document.querySelector('.file_img2');
preview.style.display = 'none'
preview2.style.display = 'none'


file_get.addEventListener('click', ()=>{
    filea.click()
});
file_get2.addEventListener('click', ()=>{
    filea2.click()
});

function previewFile(event) {
    let preview = event.path[2].children[0]
    let file = event.path[0].files[0]
    let reader = new FileReader();
    reader.onloadend = function () {
        preview.style.display = 'block'
        preview.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.src = ""
    }
    preview.style.display = 'none'
  }


(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')
    // console.log(forms);

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()