

//檢核輸入的長度
function checkStrLen(testStr,min,max){
    var str_len = testStr.length;
    if(str_len>=min && str_len<=max){
        return [true];
    }
    return [false,' 需輸入的長度為'+min+'~'+max+'個字元'];
}


// 檢核英數字組合
function checkEngNumCombination(testStr){
    
    var pat1 = "^[\\dA-z]+$";
    var regex1 = new RegExp(pat1);
    if(regex1.test(testStr)){
        return [true];
    }
    return [false,' 僅能是英數字的組合'];
}

function fieldRequired(testStr){
    if(testStr.length<1){
        return [false," 不可空白"]
    }
    return [true]
}

// 輸入欄位的元素(field_ele_id)  輸入欄位名稱的元素(field_name_ele) 可否空白(blank) 欄位值長度範圍(min,max) 顯示警告訊息的區塊id(err_msg_block_id) 其他檢核函數> check_func_list
// 至少會做的檢核 :
//     1.可否空白 > 1.1如果 不可空白 會再做> 長度的檢核

function FieldExamine(field_ele_id,field_name_ele_id,blank,min,max,err_msg_block_id,check_func_list){
    
    this.field_ele = document.getElementById(field_ele_id);
    this.field_name_ele = document.getElementById(field_name_ele_id);
    this.err_msg_block_ele= document.getElementById(err_msg_block_id);
    this.field_name = this.field_name_ele.textContent ;
    this.field_tag_name = this.field_ele.tagName
    
    var self = this;


    function examine(field_ele,field_name_ele,field_name,field_tag_name){
        var input_txt ; //輸入的欄位內容
        // var checkMsg = '';
        var check_msg_list = [];
        if(field_tag_name.toLowerCase()==='input'){
            input_txt=field_ele.value;
        }else{
            input_txt = field_ele.textContext;
        }
    
        if(!blank){
            if(!fieldRequired(input_txt)[0]){
                check_msg_list.push(field_name+fieldRequired(input_txt)[1]);
            }
            // if(input_txt.length<1){
            //     check_msg_list.push(field_name+" 不可空白");
            // }
            if(!checkStrLen(input_txt,min,max)[0]){
                // checkMsg+= field_name+checkStrLen(input_txt,min,max)[1]+"<br/>";
                check_msg_list.push(field_name+checkStrLen(input_txt,min,max)[1]);
            }
        }
    
        if(check_func_list.length>0){
            for(var func of check_func_list){
                if(!func(input_txt)[0]){
                    // checkMsg+= field_name+func(input_txt)[1]+"<br/>";
                    check_msg_list.push(field_name+func(input_txt)[1]);
                }
            }
        }
        // console.log(check_msg_list);

        return check_msg_list;
        
    }

    this.executeField = function(){
        var msg='';
        var msg_list = examine(self.field_ele,self.field_name_ele,self.field_name,self.field_tag_name);
        // console.log(msg_list);
        if(msg_list.length>0){
            for(var i=0;i<msg_list.length;i++){
                msg+=msg_list[i];
                if(i!==msg_list.length-1){
                    msg+="<br/>";
                }
            }
           
        }
        self.err_msg_block_ele.innerHTML = msg;
    }

    this.field_ele.addEventListener('keyup',this.executeField)
    
}



