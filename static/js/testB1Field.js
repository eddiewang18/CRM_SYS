// 按新增或修改按鈕時>進行計算區間起迄檢核 :
// 	1.只能輸入數值
// 	2.若是標籤互斥，則
// 		2.1 欄位[區間起] [區間訖]必須連續且互斥
// 		2.2 欄位[區間起] 必須小於 [區間訖]

// 判斷一字串是否為數值
function isNumber(value) {
    if (typeof value === "string" && value.length>0) {
        return !isNaN(value);
    }
    return false;
}

function cal_interval_check(){
    var calmin_eles = document.querySelectorAll('tr:not(.deletedRow) [belong_field="calmin"]');
    var calmax_eles =  document.querySelectorAll('tr:not(.deletedRow) [belong_field="calmax"]');
    for (var i = 0; i < calmin_eles.length; i++) {

        var calmin_ele = calmin_eles[i]; // 計算區間起元素
        var calmin_ele_val = calmin_ele.textContent.trim(); // 計算區間起欄位值

        var calmax_ele = calmax_eles[i];// 計算區間迄元素
        var calmax_ele_val = calmax_ele.textContent.trim();// 計算區間迄欄位值

        var last_calmax ;

        //如果輸入的值不是數值
        if(!isNumber(calmin_ele_val))
        {
            return [false,`第${i+1}列的 計算區間起 僅能輸入數值`]
        }
        if(!isNumber(calmax_ele_val))
        {
            return [false,`第${i+1}列的 計算區間迄 僅能輸入數值`]
        }
        calmin_ele_val =parseFloat(parseFloat(calmin_ele_val).toFixed(2)) ;
        calmax_ele_val = parseFloat(parseFloat(calmax_ele_val).toFixed(2)) ;
        if(calmin_ele_val>calmax_ele_val)
        {
            return [false,`第${i+1}列的 計算區間起 必須小於 計算區間迄`]
        }
        var xor_val = document.querySelector("span.field1 > select#id_xor");
        if(xor_val.value==="1" && last_calmax!==undefined)
        {
            var should_calmin_val = last_calmax+0.01;
            if(calmin_ele_val!==should_calmin_val)
            {
                return [false,`第${i+1}列的 計算區間起 應為 ${should_calmin_val}`];
            }
        }

        calmin_ele.textContent= parseFloat(calmin_ele_val).toFixed(2);
        calmax_ele.textContent=  parseFloat(calmax_ele_val).toFixed(2);
        last_calmax = calmax_ele_val;

    }
    return [true]

}

                
function delDeletedRow(){
    var del_rows = document.querySelectorAll("tr.deletedRow");
    for(var del_row of del_rows)
    {
        del_row.parentNode.removeChild(del_row);
    }
}
