var down_text = document.getElementsByClassName('down-link');
var down_icon = document.getElementsByClassName('down-icon-link');

function hideText(down_text) {
    for (var i=0; i<down_text.length; i++) {
        $(down_text[i]).fadeOut(1000);
    }
}

function showIcon(down_icon) {
    for (var i=0; i<down_icon.length; i++) {
        $(down_icon[i]).fadeIn(1500);
    }
}

$(document).ready(function() {
    setTimeout(function() {
        $(hideText(down_text))
        $(showIcon(down_icon))
    }, 3000)
})

