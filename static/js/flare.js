var lfeff = {
    // variables
    cx: screen.width/4,
    cy: screen.height/2.7,
    lx:0,
    ly:0,
    px: screen.width/4,
    py: screen.height/2.7,
    mobj:0,
    max:400,
    // initialization
    init : function() {
        this.mobj = document.getElementById('main_area');
        this.resize();
        this.lx = this.cx / 2;
        this.ly = this.cy / 2;
    },
    // refreshing mouse positions
    mousemove : function(x,y) {
        // if (window.event) e = window.event;
        // this.lx = (e.x || e.clientX);
        // this.ly = (e.y || e.clientY);
        this.lx = x;
        this.ly = y;
    },
    // window resizing
    resize : function() {
        lfeff.cx = lfeff.mobj.offsetWidth  * 0.5;
        lfeff.cy = lfeff.mobj.offsetHeight  * 0.5;
    },
    // main draw lens function
    draw : function() {
        lfeff.px -= (lfeff.px - lfeff.lx) * .1;
        lfeff.py -= (lfeff.py - lfeff.ly) * .1;
        // lfeff.drawLens('l1', 0.7, 1, 0, 0);
        // lfeff.drawLens('l2', 0.5, 2, 0, 0);
        // lfeff.drawLens('l3', 0.3, 3, 0, 0);
        // lfeff.drawLens('l4', 0.2, 10, 0, 0);
        // lfeff.drawLens('l5', 0.7, -1, 0, 0);
        // lfeff.drawLens('l6', 0.5, -2, 0, 0);
        // lfeff.drawLens('l7', 0.3, -3, 0, 0);
        lfeff.drawLens('l8', 1.0, -0.7, 0, 0);
        // looping current function
        setTimeout(lfeff.draw, 24);
    },
    // draw each lens function
    drawLens : function(id, scale, distance, x, y) {
        var vx = (this.cx - this.px) / distance;
        var vy = (this.cy - this.py) / distance;
        var d = this.max * scale;
        css = document.getElementById(id).style;
        css.top = Math.round(vy - (d * 0.5) + this.cy + y) + 'px';
        css.left = Math.round(vx - (d * 0.5) + this.cx + x) + 'px'
        css.width = Math.round(d) + 'px'
        css.height = Math.round(d) + 'px'
    }
}

var lfeff1 = {
    // variables
    cx: screen.width/1.8,
    cy: screen.height/2.7,
    lx:0,
    ly:0,
    px: screen.width/1.8,
    py: screen.height/2.7,
    mobj:0,
    max:400,
    // initialization
    init : function() {
        this.mobj = document.getElementById('main_area1');
        this.resize();
        this.lx = this.cx / 2;
        this.ly = this.cy / 2;
    },
    // refreshing mouse positions
    mousemove : function(x,y) {
        // if (window.event) e = window.event;
        // this.lx = (e.x || e.clientX);
        // this.ly = (e.y || e.clientY);
        this.lx = x;
        this.ly = y;
    },
    // window resizing
    resize : function() {
        lfeff1.cx = lfeff1.mobj.offsetWidth  * 0.5;
        lfeff1.cy = lfeff1.mobj.offsetHeight  * 0.5;
    },
    // main draw lens function
    draw : function() {
        lfeff1.px -= (lfeff1.px - lfeff1.lx) * .1;
        lfeff1.py -= (lfeff1.py - lfeff1.ly) * .1;
        // lfeff1.drawLens('l11', 0.7, 1, 0, 0);
        // lfeff1.drawLens('l21', 0.5, 2, 0, 0);
        // lfeff1.drawLens('l31', 0.3, 3, 0, 0);
        // lfeff1.drawLens('l41', 0.2, 10, 0, 0);
        // lfeff1.drawLens('l51', 0.7, -1, 0, 0);
        // lfeff1.drawLens('l61', 0.5, -2, 0, 0);
        // lfeff1.drawLens('l71', 0.3, -3, 0, 0);
        lfeff1.drawLens('l81', 1.0, -0.7, 0, 0);
        // looping current function
        setTimeout(lfeff1.draw, 24);
    },
    // draw each lens function
    drawLens : function(id1, scale, distance, x, y) {
        var vx = (this.cx - this.px) / distance;
        var vy = (this.cy - this.py) / distance;
        var d = this.max * scale;
        css = document.getElementById(id1).style;
        css.top = Math.round(vy - (d * 0.5) + this.cy + y) + 'px';
        css.left = Math.round(vx - (d * 0.5) + this.cx + x) + 'px'
        css.width = Math.round(d) + 'px'
        css.height = Math.round(d) + 'px'
    }
}

window.onload = function() {
    // initialization
    lfeff.init();
    // start
    lfeff.draw();
    // // binding onmousemove event
    // document.onmousemove = function(e) {
    //     if (window.event) e = window.event; // for IE
    // var i = 0;
    // for (i=0;i<screen.width*1000;i++){
    //     if(i%1000==0){
    //         console.log(i/1000);
    //         lfeff.mousemove(i/1000,i/1000);    
    //     }
    // }

    lfeff1.init();
    // start
    lfeff1.draw();
    // // binding onmousemove event
    // document.onmousemove = function(e) {
    //     if (window.event) e = window.event; // for IE
    // var i = 0;
    // for (i=0;i<screen.width*1000;i++){
    //     if(i%1000==0){
    //         console.log(i/1000);
    //         lfeff1.mousemove(i/1000,i/1000);    
    //     }
    // }

    var pos1 = screen.width/2;
    var i1 = 8;
    setTimeout(1000);
    var id1 = setInterval(frame1, 10);
    lfeff1.mousemove(pos1,screen.height/2.5);
    // setTimeout(frame, 1000);
    function frame1() {
        if (pos1 < (screen.width/5.4)){
          clearInterval(id1);
        } else {
          pos1 = pos1 - i1;
          lfeff1.mousemove(pos1,screen.height/2.5); 
        }
    }


    var pos = screen.width/2.7;
    var i = 3;
    setTimeout(1000);
    var id = setInterval(frame, 10);
    lfeff.mousemove(pos,screen.height/2.5);
    // setTimeout(frame, 1000);
    function frame() {
        if (pos > (screen.width/2)){
          clearInterval(id);
        } else {
          pos = pos + i;
          lfeff.mousemove(pos,screen.height/2.5); 
        }
    }


    
}