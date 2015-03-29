/*
Name          : TanXiao
Student Number: 13331235
Content       : Hw6(无扩展项)
*/
"use strict";
window.onload = function() {
    initialization();
    document.getElementById('puzzlearea').onmouseover = detection;
    document.getElementById('shufflebutton').onclick = start;
};

function initialization() {
    document.getElementById('puzzlearea').appendChild(document.createElement('div'));
    var x = document.getElementById('puzzlearea').children;
    x[x.length - 1].style.border = "2px solid white";
    for (var i = x.length - 1; i >= 0; i--) {
        x[i].style.width = "96px";
        x[i].style.height = "96px";
        x[i].style.position = "absolute";
        x[i].style.left = (100 * (i % 4)).toString() + "px";
        x[i].style.top = (100 * ((i - i % 4) / 4)).toString() + "px";
        // x[i].style.cssFloat = 'left';
        x[i].id = i;
        if (i != x.length - 1) {
            x[i].style.border = "2px solid black";
            x[i].style.backgroundImage = 'url(mop.jpg)';
            x[i].style.backgroundPosition = (100 * (4 - i % 4)).toString() + "px " + (100 * (4 - (i - i % 4) / 4)).toString() + "px";
        }
    }
}

function start() {
    for (var i = 100; i >= 0; i--) {
        var blank = document.getElementById('15');
        var x = document.getElementById(parseInt(Math.random() * 14).toString());
        if (judge(x, blank)) {
            move(x);
        }
    }
}

function move(elem) {
    var x = document.getElementById('15');
    var temp = x.style.left;
    x.style.left = elem.style.left;
    elem.style.left = temp;
    temp = x.style.top;
    x.style.top = elem.style.top;
    elem.style.top = temp;
}

function detection() {
    var x = window.event.srcElement;
    var blank = document.getElementById('15');
    x.onmouseleave = recover;
    if (judge(x, blank)) {
        x.style.borderColor = "red";
        x.style.color = "red";
        x.style.textDecoration = "underline";
    }
    x.onclick = function() {
        if (judge(x, blank)) {
            move(x);
        }
    };
}

function judge(elem, blank) {
    var disX = Math.abs(elem.offsetLeft - blank.offsetLeft);
    var disY = Math.abs(elem.offsetTop - blank.offsetTop);
    // alert(disX.toString()+disY.toString());
    if (Math.abs(disX - disY) == 100 && disX + disY == 100) {
        return true;
    } else {
        return false;
    }
}

function recover() {
    var x = window.event.srcElement;
    if (x.id != 15) {
        x.style.borderColor = "black";
        x.style.color = "black";
        x.style.textDecoration = "none";
    }

}
