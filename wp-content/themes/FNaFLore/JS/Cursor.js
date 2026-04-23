$(document).mousemove(function(e){
    $("#Cursor").css({left:e.pageX, top:e.pageY});
});

function CursorShow() {
	document.getElementById('Cursor').style.display = 'block';
}

function CursorHide() {
	document.getElementById('Cursor').style.display = 'none';
}