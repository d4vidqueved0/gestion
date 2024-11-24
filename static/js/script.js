let btnModo = document.getElementById('btnModo');

console.log(body)

btnModo.addEventListener('click', cambiarModo)

function cambiarModo(){
    let body = document.getElementById('body');
    if (body.style.background == 'black'){
        body.style.background = 'white';
        body.style.color = 'black'
        btnModo.style.color = 'black';

    }else{
        body.style.background = 'black';
        body.style.color = 'white'
        btnModo.style.color = 'white';
    }
}