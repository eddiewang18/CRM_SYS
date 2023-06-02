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

	if(trDadEle!==null){
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



//檢核日期區間查詢欄位

function dateIntervalExamine(sdate_selector,edate_selector,edate_err_selector,date_field_cname)
{	
	// sdate_selector 日期起欄位的css selector
	// edate_selector 日期迄欄位的css selector
	// edate_err_selector 顯示日期迄錯誤訊息欄位的css selector > 當檢核沒過時，要顯示msg的地方
	// date_field_cname 日期龍味的中文顯示名稱
	var sdate = document.querySelector(sdate_selector);
	var edate = document.querySelector(edate_selector);
	var date_err =  document.querySelector(edate_err_selector);
	if(sdate.value.length>0 || edate.value.length>0)
	{
		if(!(sdate.value.length>0 && edate.value.length>0))
		{
			date_err.innerHTML=`欄位 ${date_field_cname}起 及 ${date_field_cname}訖 均需輸入`;
			return false;
		}
	}
	if(sdate.value.length>0 && edate.value.length>0)
	{
		if(sdate.value>edate.value)
		{
			date_err.innerHTML=`欄位 ${date_field_cname}起 需小於 ${date_field_cname}訖`;
			return false;

		}

	}
	date_err.innerHTML='';
	return true;
}

function fieldChangeLinkage(data,targetFieldName,effectEleName,effectEleId,ajax_url,effectEleIdActualVal,effectEleIdShowVal){
	var changed_ele_val = data[targetFieldName];
	var effeted_id_val = data[effectEleName];
	$.ajax({
		url:ajax_url,
		method:"GET",
		dataType:"json",
		data:{
			changed_ele_name:changed_ele_val
		},
		success:function(response)
		{
			console.log(response);
			var option_html = "";
			for(var obj of response)
			{
				var effect_ele_actual_val = obj[effectEleIdActualVal];
				var effect_ele_show_val = obj[effectEleIdShowVal];
				option_html+=`<option value="${effect_ele_actual_val}">${effect_ele_show_val}</option>`;
			}
			$(effectEleId).html(option_html); 
			$(effectEleId).val(effeted_id_val);
		}
		})	
}


// 下拉選單欄位連動
function selectFieldChangeLinkage(targetFieldId,effectEleId,ajax_url,effectEleIdActualVal,effectEleIdShowVal,effectEleErrId)
    {
      // targetFieldId > 觸發欄位連鎖的欄位id
      // effectEleId > 受連動影響的欄位id
      // ajax_url> 發送的目的url
      // effectEleIdActualVal > 受連動影響的欄位實際值
      // effectEleIdShowVal > 受連動影響的欄位顯示值
      // effectEleErrId >受連動影響的欄位錯誤訊息區塊id
      document.addEventListener("change",function(e)
      {
        if(e.target.id===targetFieldId)
        {
          
            var changed_ele = e.target;
            var changed_ele_parent = e.target.parentNode.parentNode.parentNode;
            var effect_ele = changed_ele_parent.querySelector(effectEleId); //受連動影響的欄位元素
            var changed_ele_val = changed_ele.value;
            $.ajax(
              {
                url:ajax_url,
                method:"GET",
                dataType:"json",
                data:
                {
                  changed_ele_name:changed_ele_val
                },
                success:function(response)
                {
                    console.log(response);
                    var option_html = "";
                        for(var obj of response)
                        {
                            var effect_ele_actual_val = obj[effectEleIdActualVal];
                            var effect_ele_show_val = obj[effectEleIdShowVal];
                            option_html+=`<option value="${effect_ele_actual_val}">${effect_ele_show_val}</option>`;
                        }
                        effect_ele.innerHTML =  option_html;
						if(effectEleErrId!==undefined)
						{
							document.getElementById(effectEleErrId).innerHTML='';
						}
                        
                }
              })

            console.log("-------------------");
        }
      })
    }


//取得動態表格中的增刪改資料，並用js中物件作為返回值
function getFrontEndDataFunc(extra_fields_value,input_type_cfg){               
	// extra_fields_value 當將動態表格的資料轉成js的物件資料後，
   //  若還想增加其他欄位資料的內容(非動態表格中的欄位內容)，
   //  則可以在此物件的key值輸入欄位name屬性，
   //  value輸入該欄位的css selector值。
	   
		var table = document.getElementById('table1');
	   var firstTrTd= table.querySelector(".firstRow").querySelectorAll("td");
	   var fieldNameList = [];
	   //var cpnyid_val = document.querySelector("select#id_cpnyid").value;
	   for(var i of firstTrTd){
		   fieldNameList.push(i.getAttribute("name"));
	   }
	   
	   var frontEndData ={
	   "insert":[],
	   "update":[],
	   "delete":[],
	   "all_visible_data":[]
	   };
   
   
	   for(var action in frontEndData){
		   var table_tr ;
		   if(action==="insert"){
			   table_tr = document.querySelectorAll(".newRow");
		   }else if(action==="update"){
			   table_tr = document.querySelectorAll(".updateRow");
		   }else  if(action==="delete"){
			   table_tr = document.querySelectorAll(".deletedRow");
		   }else{
			   table_tr =  document.querySelectorAll("#table1 tr:not(.deletedRow):not(.titleRow)");
		   }
   
		   
		   for(var tr of table_tr){
			   var obj_data={};
			   var tr_td = tr.querySelectorAll("td");
			   for(var i=0;i<tr_td.length;i++){
				   var key = fieldNameList[i];
				   var values;
				   tr_td_name_attr = tr_td[i].getAttribute("belong_field");
				   input_type = input_type_cfg[tr_td_name_attr]['inputType'];
				   if(input_type==='checkbox'){
					   values = tr_td[i].querySelector("input").value.trim();
				   }
				   else if(input_type==='select'){
					   values = tr_td[i].querySelector("select").value.trim();
				   }else{
					   values = tr_td[i].textContent.trim();
				   }
				   
				   obj_data[key]=values;
			   }

			   if(extra_fields_value!==undefined)
			   {	
				   for(var n in extra_fields_value)
				   {	
					   var fv = document.querySelector(extra_fields_value[n]).value;
					   if(n!==undefined)
					   {
						   obj_data[n]=fv;
					   }
					   
				   }
			   }

			   frontEndData[action].push(obj_data);
   
		   }
   
	   }

	   return frontEndData;
   }