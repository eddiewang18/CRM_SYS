//讓所選的元素可以在頁面上移動
function moveModal(modalSelector){
	var modal = document.querySelector(modalSelector);
	modal.onmousedown= function(e){
		var diffx = e.pageX-this.offsetLeft;
		var diffy = e.pageY-this.offsetTop;

		document.onmousemove = function(e){
			modal.style.left = (e.pageX-diffx)+'px';
			modal.style.top = (e.pageY-diffy)+'px';

		}

		document.onmouseup = function(){
			document.onmousemove = null;
			document.onmouseup  = null;
		}

	}
}
