terms = document.getElementsByClassName("term");
clozes = document.getElementsByClassName("cloze");

for (i = 0; i < terms.length; i++) {
    var len = terms[i].innerHTML.length;
    for (j = 0; i < clozes.length; j++) {
        clozes[j].innerHTML = "[" + len + "]";
    }
}

