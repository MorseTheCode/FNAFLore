 var gfred = document.createElement('div'); gfred.setAttribute("id", "GFREDDY"); gfred.setAttribute("style", "display:block;"); function ITSME() { document.body.insertBefore(gfred, document.body.firstChild); 
 setTimeout(function () { window.setInterval(function(){ window.location.reload(true);}, 2000); }, 1000); audio.play(); }
 
 function REDEEMED() { localStorage.gfreddy = 1; location.href = "https://fnaflore.com/1987/";}