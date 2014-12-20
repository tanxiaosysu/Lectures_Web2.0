/*
student number: 13331235
Name: TanXiao
Content: HomeWork5
            额外功能1、2
*/
"use strict";
var custom = "      o\n" +
    "  ----#----\n" +
    "      #\n" +
    "     / \\\n" +
    "=====\n" +
    "      o\n" +
    "   _-_#-_-\n" +
    "      #\n" +
    "     / \\\n" +
    "=====\n" +
    "    _ o\n" +
    "   / \\#\\_/\n" +
    "      #\n" +
    "     / \\\n" +
    "=====\n" +
    "      o\n" +
    "   _-_#-_-\n" +
    "      #\n" +
    "     / \\\n" +
    "=====\n" +
    "      o\n" +
    "  ----#----\n" +
    "      #\n" +
    "     / \\\n" +
    "=====\n" +
    "      o\n" +
    "   -_-#_-_\n" +
    "      #\n" +
    "     / \\\n" +
    "=====\n" +
    "      o _\n" +
    "   \\_/#/ \\\n" +
    "      #\n" +
    "     / \\\n" +
    "=====\n" +
    "      o\n" +
    "   -_-#_-_\n" +
    "      #\n" +
    "     / \\\n";
ANIMATIONS["Custom"] = custom;

var AsciiMate = [];
var t;
var count = 0;

function start() {
    document.getElementById("start").disabled = true;
    document.getElementById("stop").disabled = false;
    document.getElementById("flash").disabled = true;
    GetAscii();
    ProgramLoop();
}

function stop() {
    clearTimeout(t);
    document.getElementById("start").disabled = false;
    document.getElementById("stop").disabled = true;
    document.getElementById("flash").disabled = false;
    var x = document.getElementById('flash').value;
    document.getElementById('displayarea').value = ANIMATIONS[x];
}

function GetAscii() {
    var x = document.getElementById('flash').value;
    AsciiMate = ANIMATIONS[x].split('=====\n');
}

function ProgramLoop() {
    var speed = 0;
    speed = document.getElementById('speed').checked ? 50 : 200;
    SetFontsize();
    document.getElementById('displayarea').value = AsciiMate[count];
    count = (count + 1) % AsciiMate.length;
    t = setTimeout(ProgramLoop, speed);
}

function SetFontsize() {
    var fontsize = [];
    fontsize["small"] = "7pt";
    fontsize["medium"] = "12pt";
    fontsize["large"] = "24pt";
    var x = document.getElementsByName('size');
    for (var i = x.length - 1; i >= 0; i--) {
        if (x[i].checked) {
            document.getElementById("displayarea").style.fontSize = fontsize[x[i].value];
        }
    }
}
