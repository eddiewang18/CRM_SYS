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


function modal_table_selected(tr_dad_selector,selected_class,titleRow_class){
	// 綁定 table(tr 父元素)
	var trDadEle = document.querySelector(tr_dad_selector);
	trDadEle.onclick = function(e){
		if(e.target.tagName==="TD" && ! e.target.parentNode.classList.contains(titleRow_class)){
			if(! e.target.parentNode.classList.contains(selected_class)){
			  //實現整張table只會被選中(forcus)一列(底色變灰)
			  var already_selected_rows = document.getElementsByClassName(selected_class);
			  if(already_selected_rows.length>0){
				for(var selected_row of already_selected_rows){
				  selected_row.classList.remove(selected_class);
				}
			  }

			  e.target.parentNode.classList.add(selected_class);
			}else{
			  e.target.parentNode.classList.remove(selected_class)
			}
		}
	}

  }


//發送ajax請求時須加上下列這段程式碼來通過django的csrf_token驗證機制
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
 }   