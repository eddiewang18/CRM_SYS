function createSelect(select_name_attr,options_config){
    //  select_name_attr > 為 <select> 標籤 name屬性
    // options_config > 為一個陣列，型態如下 [{value:"",label:""}] > value用來表示選項option的name屬性,label用來表示選項的提示文字，有幾個選項就傳幾個物件
    
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
    
function createCheckbox(checkbox_name_attr,value_attr){
//  checkbox_name_attr > 為 <input type="checkbox"> 標籤的 name屬性

//  value_attr > 為 <input type="checkbox"> 標籤的 value 屬性

    // 1.建立select
    var checkboxEle = document.createElement("input");
    checkboxEle.setAttribute('name',checkbox_name_attr);
    checkboxEle.setAttribute('value',value_attr);
    checkboxEle.setAttribute('type',"checkbox");
    return checkboxEle;
}
    




//實現動態表格
//pkList裡面存primary key 的欄位的name屬性
function dynamic_table(tableID,addBtnID,delBtnID,pkList=[],titleRow=true,input_type_config){

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

    // 若使用者的資料表欄位有指定primary key 時， 
    // if(pkList.length>0){
    //     for(var i=0;i<firstTds.length;i++){
    //         if(pkList.includes(firstTds[i].getAttribute("name"))){
    //             pk_index.push(i);  
    //         }
    //     }
    // }

    var currentTrs = document.querySelectorAll("tr:not(.firstRow)"); //取得載入網頁時當前table中除索引列以外的各個資料列

    // 如果載入網頁時，當前table中有除索引列以外的各個資料列
    if(currentTrs.length>0){
        // 依序對那些列的各個儲存格欄位設置 belong_field(自訂屬性，用來標示此儲存格對應到db table中的哪個欄位) 與 id
        for(var i=0;i<currentTrs.length;i++){
            
            var tr_tds= currentTrs[i].querySelectorAll("td");

            for(var j=0;j<firstTds.length;j++){
                var firstTdEle = firstTds[j]; 
                //取得td元素的name屬性
                var name_attr = firstTdEle.getAttribute("name");

                tr_tds[j].setAttribute("belong_field",name_attr);
                tr_tds[j].setAttribute("id","td"+(i+1)+(j+1));
    
            }

        }
    }

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
                if(ele.parentNode.classList.contains("selected")){
                    ele.parentNode.classList.remove("selected");
                    
                }else{
                    ele.parentNode.classList.add("selected");
                    ele.addEventListener('click',function(){
                    //表格中欄位可被編輯的條件為: 你是一個新增列 或是 你不是pk的欄位
                    if(ele.parentNode.classList.contains("newRow") || !pkList.includes(ele.getAttribute("belong_field"))){
                        ele.setAttribute("contenteditable","true");
                        ele.addEventListener("keypress",function(e){
                            if(e.key=="Enter"){
                                e.preventDefault();
                            }
                        })
                      }
                    })

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