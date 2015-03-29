/*
Name          : TanXiao
Student Number: 13331235
Content       : Hw6(无扩展项)
*/
"use strict";
$(document).ready(function() {
    initialization();
    $('#puzzlearea').children().mouseover(function(event) {
        var x = event.target;
        var blank = $('#15');
        $(x).mouseleave(function(event) {
            var y = event.target;
            if (y.id != "15") {
                $(y).css({
                    "borderColor": "black",
                    "color": "black",
                    "textDecoration": "none"
                });
            }
        });
        if (judge($(x), blank)) {
            $(x).css({
                "borderColor": "red",
                "color": "red",
                "textDecoration": "underline"
            });
        }
    });

    $('#puzzlearea').children().click(function(event) {
        if (judge($(event.target), $('#15'))) {
            move(event.target);
        }
    });
    $('#shufflebutton').click(function() {
        for (var i = 1000; i >= 0; i--) {
            var blank = $('#15');
            var temp = '#' + parseInt(Math.random() * 14).toString();
            var x = $(temp);
            if (judge($(x), blank)) {
                move(x);
            }
        }
    });

    function initialization() {
        $('#puzzlearea').append("<div></div>");
        var x = $('#puzzlearea').children();
        x.addClass("game");
        x.last().addClass("blank");
        for (var i = x.length - 1; i >= 0; i--) {
            $(x[i]).attr("id", i.toString());
            $(x[i]).css({
                "left": ((100 * (i % 4)).toString() + "px"),
                "top": ((100 * ((i - i % 4) / 4)).toString() + "px")
            });
            $(x[i]).css({
                "background-position": ((100 * (4 - i % 4)).toString() + "px " + (100 * (4 - (i - i % 4) / 4)).toString() + "px")
            });
        }
        $("div.game").css({
            "border": "2px solid black",
            "position": "absolute",
            "width": "96px",
            "height": "96px",
            "background-image": "url(mop.jpg)"
        });
        $("div.blank").css({
            "border": "2px solid white",
            "background": "none"
        });
    }

    function move(elem) {
        var x = $('#15');
        var temp = x.offset();
        x.offset($(elem).offset());
        $(elem).offset(temp);
    }

    function judge(elem, blank) {
        var disX = Math.abs(elem.offset().left - blank.offset().left);
        var disY = Math.abs(elem.offset().top - blank.offset().top);
        if (Math.abs(disX - disY) == 100 && disX + disY == 100) {
            return true;
        } else {
            return false;
        }
    }
});
