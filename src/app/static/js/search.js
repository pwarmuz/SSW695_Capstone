
function frontPageSearch() {
    // Declare variables
    var input, filter, list, div, a, i;
    input = document.getElementById('search-bar');
    filter = input.value.toUpperCase();
    list = document.getElementById("book-list");
    //div = list.getElementsByTagName('div');
    div = $("#book-list").children();


    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < div.length; i++) {
        // search header links
        a = div[i].getElementsByTagName("a")[0];
        var books = div[i].getElementsByTagName("div");
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            div[i].style.display = "";
        } else {
            div[i].style.display = "none";
        }

        // search books
        for (var j = 0; j < books.length; j++) {
            if (books[j].innerHTML.toUpperCase().indexOf(filter) > -1) {
                div[i].style.display = "";
                books[j].style.display = "";
            } else {
                books[j].style.display = "none";
            }
        }
    }
}
