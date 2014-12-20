/*
student number: 13331235
Name: TanXiao
Content: Lab5
            Ex1~Ex4,Ex5-1
*/
function changearea() {
    $("#t1").css("font-size", "24pt");
    x = document.getElementById('Bling');
    if (x.checked == true) {
        $("#t1").css("color", "green");
        $("#t1").css("text-decoration", "underline blink line-through");
        $('body').css("background-image", "url(hundred-dollar-bill.jpg)");
    } else {
        $("#t1").css("color", "black");
        $("#t1").css("text-decoration", "none");
        $('body').css("background-image", "none");
    }
}

function changetext() {
    var str = document.getElementById('t1').value.toUpperCase();
    var part = str.split('.');
    str = part.join('-izzle.')
    document.getElementById('t1').value = str;
}
