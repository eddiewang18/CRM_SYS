function moveContainer(){
    var draglist = document.querySelectorAll(".draggable");
    for(var d of draglist){
        d.addEventListener("mousedown",function(e){
            var clickX = this.offsetLeft;
            var clickY = this.offsetTop;
            var mouseFisrtX = e.clientX;
            var mouseFisrtY = e.clientY;
            var differX = mouseFisrtX-clickX;
            var differY = mouseFisrtY-clickY;
            var my = this;
    
            document.onmousemove = function (e) {
                var st = document.body.scrollTop;
                my.style.left = (e.clientX-differX)+"px";
                my.style.top = (e.clientY-differY+st)+"px";
                // this.style.top= (e.clientX-differX)+"px";
                // this.style.mouseFisrtY
            }
    
            document.onmouseup=function(e){
                document.onmousemove = null;
                document.onmouseup = null;
            }
    
        })
    }
}

