/*
Name          : TanXiao
Student Number: 13331235
Content       : Lab5
*/
'use strict';
var Over = false;
var Win = false;
var wall = document.getElementsByClassName('boundary');

function GameReset() {
    Over = false;
    Win = false;
    for (var i = wall.length - 1; i >= 0; i--) {
        wall[i].style.backgroundColor = "#eeeeee";
    }
    document.getElementById('status').innerHTML = "Move your mouse over the \"S\" to begin.";
}

function GameLoop() {
    var gamearea = document.getElementById('maze');
    gamearea.onmouseleave = GameOver;
    for (var i = wall.length - 1; i >= 0; i--) {
        wall[i].onmouseover = GameOver;
    }
}

function GameStart() {
    GameReset();
    GameLoop();
}

function GameOver() {
    if (!Win) {
        Over = true;
        for (var i = wall.length - 1; i >= 0; i--) {
            wall[i].style.backgroundColor = "red";
        }
        document.getElementById('status').innerHTML = "You Lose!";
    }
}

function GameWin() {
    Win = true;
    if (!Over) {
        document.getElementById('status').innerHTML = "You Win!";
    }
}

window.onload = function() {
    document.getElementById('start').onclick = GameStart;
    document.getElementById('end').onmouseover = GameWin;
};
