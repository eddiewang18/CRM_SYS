function createSelect(select_name_attr,options_config){
    //  select_name_attr > 為 <select> 標籤 name屬性
    // options_config > 為一個陣列，型態如下 [{value:"",label:""}] 
    // > value用來表示選項option的name屬性,label用來表示選項的提示文字，有幾個選項就傳幾個物件
    
        // 1.建立select
        var selectEle = document.createElement("select");
        selectEle.setAttribute('name',select_name_attr);
        // 2.利用迴圈建構option
        option_str = "";
        for(var option of options_config){
            option_value = option['value'];
            option_label = option['label'];
            option_str+=`<option value="${option_value}">${option_label}</option>`;
        }
        selectEle.innerHTML = option_str;
        return selectEle;
    
    
    }
    


function updateValue(checkbox) {
    if (checkbox.checked) {
        checkbox.value = 1;
    } else {
        checkbox.value = 0;
    }
    }    
function createCheckbox(checkbox_name_attr,value_attr){
//  checkbox_name_attr > 為 <input type="checkbox"> 標籤的 name屬性

//  value_attr > 為 <input type="checkbox"> 標籤的 value 屬性

    // 1.建立select
    var checkboxEle = document.createElement("input");
    checkboxEle.setAttribute('name',checkbox_name_attr);
    checkboxEle.setAttribute('value',value_attr);
    checkboxEle.setAttribute('type',"checkbox");
    checkboxEle.setAttribute("onchange", "updateValue(this)");
    return checkboxEle;
}

// 如果某些欄位用的是select 或 下拉選單那些欄位在查詢資料後可能就失去原本的輸入特性
// 為解決此問題，我們必須將其原本輸入的欄位特性給找回，並賦給他們原本的值

function reform_field_feat(field_feat,response_data){
	// field_feat 為一個物件，物件的key存select或checkbox field的name屬性，物件的
    // 值則須依欄位的輸入類別來做決定
    // e.g. field_feat=[{checkbox:{name:"label_enable",check:{"1":true,"0":false}}},{select:{name:"",value_label:[{value:"",label:""}] }}]
    console.log("reform_field_feat");
    for(var input of field_feat)
    {
        for(var input_type in input)
        {
            var name_attr = input[input_type].name;
            var currentTds = document.querySelectorAll(`td[belong_field='${name_attr}']`);
            for(var i =0 ;i<currentTds.length;i++)
            {   
                var input_ele ;
                var td_ele = currentTds[i];
                // var content = td_ele.textContent.trim();
                var content =response_data[i][input[input_type]['name']]
                // console.log("======================");
                // console.log(`td_ele:${td_ele.id}`);
                // console.log(`content:${content}`);
                // console.log("======================");
                if(input_type==="checkbox")
                {
                    input_ele =  createCheckbox(name_attr,content);
                    td_ele.textContent="";
                    if(input[input_type]['check'][content])
                    {
                        input_ele.checked=true;
                    }else{
                        input_ele.checked=false;
                    }
                    td_ele.appendChild(input_ele);
                }
                if(input_type==="select")
                {
                    input_ele =  createSelect(name_attr,input.value_label);
                    td_ele.textContent="";
                    input_ele.value=content;
                    td_ele.appendChild(input_ele);
                }
                

            }
        }
    }


}




function init_table(firstTds){
    var currentTrs = document.querySelectorAll("tr:not(.firstRow)"); //取得載入網頁時當前table中除索引列以外的各個資料列

      // 如果載入網頁時，當前table中有除索引列以外的各個資料列
    if(currentTrs.length>0)
    {   
        // 依序對那些列的各個儲存格欄位設置 belong_field(自訂屬性，用來標示此儲存格對應到db table中的哪個欄位) 與 id
        for(var i=0;i<currentTrs.length;i++){
            
            var tr_tds= currentTrs[i].querySelectorAll("td");
            if(tr_tds.length>0 && tr_tds[0].parentNode.parentNode.parentNode.id!=='qmodal_result_table')
            {   
             
                for(var j=0;j<firstTds.length;j++){
                    var firstTdEle = firstTds[j]; 
                    //取得td元素的name屬性
                    var name_attr = firstTdEle.getAttribute("name");
                    tr_tds[j].setAttribute("name",name_attr);
                    tr_tds[j].setAttribute("belong_field",name_attr);
                    tr_tds[j].setAttribute("id","td"+(i+1)+(j+1));
        
                }
            }


        }
    }  
}



//實現動態表格
//pkList裡面存primary key 的欄位的name屬性
function dynamic_table(tableID,addBtnID,delBtnID,pkList=[],titleRow=true,input_type_config,multiple_selected=true){

/*
input_type_config > 應傳進一個 物件包裹各個物件的參數，每個物件表示每個欄位輸入的特性(文字輸入,下拉選單,checkbox....)
input_type_config = {

    col_name_attr :{
		inputType : "input",
	},

    col_name_attr :{
		inputType : "checkbox",
		name : 
	},
	
	col_name_attr :{
		inputType : "select",
		name:'',
		option : [{name:"",label:""},.....]
	},

}
    
multiple_selected > 判斷動態表格支不支持多重選中資料列 , true : 可 , false : 不可

*/

    var table = document.getElementById(tableID);
    var add = document.getElementById(addBtnID);
    var del = document.getElementById(delBtnID);
    var firstTr = table.querySelectorAll("tr")[0]; // 第一列
    var firstTds = firstTr.querySelectorAll("td"); // 第一列裡的儲存格欄位
    // var pk_index = [];

    //取的當前table的總列數
    function getCurrentTableRowsLen(){
        var len = table.querySelectorAll("tr").length;
        return len;
    }
    if(titleRow){
        // 若第一列為索引則為其添加樣式
        firstTr.classList.add("firstRow");

    }
    init_table(firstTds);
    // 新增table列的相關操作
    add.addEventListener("click",function(){
        var tr = document.createElement("tr");
        tr.classList.add("newRow");//凸顯這一列是當前新增的
        var current_rowsLen = getCurrentTableRowsLen();
        tr.setAttribute("id","tr"+(current_rowsLen+1))//給個id(或許用不到)
        for(var i=0;i<firstTds.length;i++){
            var firstTdEle = firstTds[i];
            //取得td元素的name屬性
            var name_attr = firstTdEle.getAttribute("name");

            
            var td = document.createElement("td");
            td.setAttribute("belong_field",name_attr);
            td.setAttribute("id","td"+(current_rowsLen)+(i+1));

            // console.log(input_type_config);
            // console.log(`name_attr:${name_attr}`);
            // console.log(input_type_config[name_attr]);
            var input_type = input_type_config[name_attr]['inputType'];
            if(input_type==="checkbox"){
                td.appendChild(createCheckbox(input_type_config[name_attr]['name'],input_type_config[name_attr]['value']));
            }
            else if(input_type==="select"){
                //console.log(input_type_config[name_attr]['option']);
                td.appendChild(createSelect(input_type_config[name_attr]['name'],input_type_config[name_attr]['option']));
            }else{

            }
            tr.appendChild(td);

        }

        table.appendChild(tr);
        console.log("add new row!");
    });


    del.addEventListener("click",function(){
        var selected_rows = document.querySelectorAll(".selected");
        for(var sr of selected_rows){
            if(!sr.classList.contains("newRow")){
                if(sr.classList.contains("updateRow")){
                    sr.classList.remove("updateRow");
                }
                sr.classList.add("deletedRow"); //如果是刪除原有已存在資料庫的數據，這我們先把列給隱藏(讓之後api可以知道要刪除哪筆數據)
                sr.style.display="none";
            }else{
                sr.parentNode.removeChild(sr);
            }
        }
    })


        table.addEventListener("click",function(e){
            var ele_value;
            var ele = e.target;
            if(ele.tagName=="TD" && !(ele.parentNode.classList.contains("firstRow"))){


                if(ele.parentNode.classList.contains("selected") && multiple_selected){
                    ele.parentNode.classList.remove("selected");
                    
                }else{
					
					
					if(!multiple_selected)
					{
						

					  //實現整張table只會被選中(forcus)一列(底色變灰)
					  var already_selected_rows = document.getElementsByClassName("selected");
					  if(already_selected_rows.length>0){
						for(var selected_row of already_selected_rows){
						  selected_row.classList.remove("selected");
						}
					  }
	
					}
                    
					ele.parentNode.classList.add("selected");
					
					
                    ele.addEventListener('click',function(){


                    //判斷哪些欄位可被編輯
                    ele.setAttribute("contenteditable","true");
                    ele.addEventListener("keypress",function(e){
                        if(e.key=="Enter"){
                            e.preventDefault();
                        }
                    })
                    try {
                        if((pkList.includes(ele.getAttribute("belong_field")) && !(ele.parentNode.classList.contains("newRow"))))
                        {
                            ele.setAttribute("contenteditable","false");
                        }
                        if(ele.childNodes[0].tagName==="SELECT")
                        {
                            ele.setAttribute("contenteditable","false");
                        }
                        if( ele.childNodes[0].type==="checkbox")
                        {
                            ele.setAttribute("contenteditable","false");
                        }
                    } catch (e) {
                        
                    }


                    })

                    //當使用者對一個原有數據列進行修改，則標記該列已被更改
                    ele.addEventListener("input", function() {
                        // console.log("contenteditable element changed");
                        if(!this.parentNode.classList.contains("updateRow") && !(this.parentNode.classList.contains("newRow"))){
                            this.parentNode.classList.add("updateRow");
                        }
                    });
                    
                }

                ele.addEventListener('blur',function(){
                        ele.setAttribute("contenteditable","false");

                    })
            }
    })
    // 當動態表格中的欄位輸入為checkbox時，修改動作的相關處理
    document.addEventListener('change',function (e) {
        if(e.target.tagName.toLowerCase()==="input" && e.target.type==="checkbox")
        {
            if(!e.target.parentNode.parentNode.classList.contains("updateRow") && !(e.target.parentNode.parentNode.classList.contains("newRow"))){
                e.target.parentNode.parentNode.classList.add("updateRow");
            }
        }
      })
}



//傳送動態表格中 新增 刪除 修改的資料
function submitJsonData2BackEnd(submitBtnID,tableID,input_type_config,backEndURL){
    var submitBtn= document.getElementById(submitBtnID);
    var table = document.getElementById(tableID);
    var firstTrTd= table.querySelector(".firstRow").querySelectorAll("td");
    var fieldNameList = [];
    for(var i of firstTrTd){
         fieldNameList.push(i.getAttribute("name"));
    }
    var frontEndData ={
     "insert":[],
     "update":[],
     "delete":[],
     };
 
     submitBtn.addEventListener('click',function(){
         for(var action in frontEndData){
         var table_tr ;
         if(action==="insert"){
             table_tr = document.querySelectorAll(".newRow");
         }else if(action==="update"){
             table_tr = document.querySelectorAll(".updateRow");
         }else{
             table_tr = document.querySelectorAll(".deletedRow");
         }
         for(var tr of table_tr){
             var obj_data={};
             var tr_td = tr.querySelectorAll("td");
             for(var i=0;i<tr_td.length;i++){
                var key = fieldNameList[i];
                var values;
                tr_td_name_attr = tr_td[i].getAttribute("belong_field");
                input_type = input_type_config[tr_td_name_attr]['inputType'];
                if(input_type==='checkbox'){
                    values = tr_td[i].querySelector("input").value;
                }
                else if(input_type==='select'){
                    values = tr_td[i].querySelector("select").value;
                }else{
                    values = tr_td[i].textContent;
                }
                
                obj_data[key]=values;
             }
             frontEndData[action].push(obj_data);
         }
 
         }
         console.log(frontEndData);
		 //發送ajax請求時須加上下列這段程式碼來通過django的csrf_token驗證機制
        //  function getCookie(name) {
        //     let cookieValue = null;
        //     if (document.cookie && document.cookie !== '') {
        //         const cookies = document.cookie.split(';');
        //         for (let i = 0; i < cookies.length; i++) {
        //             const cookie = cookies[i].trim();
        //             // Does this cookie string begin with the name we want?
        //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
        //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        //                 break;
        //             }
        //         }
        //     }
        //     return cookieValue;
        // }
        // const csrftoken = getCookie('csrftoken');
		//發送ajax請求時須加上上面這段程式碼來通過django的csrf_token驗證機制
        //  $.ajax({

        //     url:backEndURL,
        //     method:"POST",
        //     dataType:"json",
        //     headers: {'X-CSRFToken': csrftoken}, //在headers中要提供csrftoken，讓client發送請求時攜帶csrftoken資訊
        //     data:{
        //         postData:JSON.stringify(frontEndData),
                
        //     },
        //     success:function(response){
        //         console.log("OK");
        //     }


        // })

     }
     
     )
 
}