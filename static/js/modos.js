
  function toggleTheme() {
    const temaActual = document.documentElement.getAttribute('data-theme');
    const nuevoTema = (temaActual === 'dark') ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nuevoTema);
    localStorage.setItem('theme', nuevoTema);
    cambiarIcono(nuevoTema)
  }

function cambiarIcono(tema) {
    const divIconos = document.getElementById('iconos-modo');
    const sol = document.getElementById('sol').cloneNode(true);
    const luna = document.getElementById('luna').cloneNode(true);
    while (divIconos.firstChild) {
        divIconos.removeChild(divIconos.firstChild);
      }

      if (tema=== 'dark') {
        luna.style.display = 'block'
        luna.style.filter = 'invert(1)'
        divIconos.appendChild(luna);

      } else {
        sol.style.display = 'block'
        divIconos.appendChild(sol);
      }
}


  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

  const temaGuardado = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', temaGuardado);
  cambiarIcono(temaGuardado)



  
  document.addEventListener("DOMContentLoaded", function() {
    let btnMas = document.getElementById('btnMas');
    let btnMenos = document.getElementById('btnMenos');

    const minFontSize = 12; 
    const maxFontSize = 16; 

    // Cargar tamaño de fuente guardado
    let savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        document.body.style.fontSize = savedFontSize + 'px';
    }

    btnMas.addEventListener('click', () => {
        changeFontSize(2);
    });

    btnMenos.addEventListener('click', () => {
        changeFontSize(-2);
    });

    function changeFontSize(delta) {
        const body = document.body;
        let currentFontSize = parseInt(window.getComputedStyle(body).fontSize);
        let newFontSize = currentFontSize + delta;
        
        if (newFontSize >= minFontSize && newFontSize <= maxFontSize) {
            body.style.fontSize = newFontSize + 'px';
            // Guardar el nuevo tamaño de fuente en localStorage
            localStorage.setItem('fontSize', newFontSize);
        }
    }
});
