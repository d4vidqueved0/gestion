
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
    console.log(tema)
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
