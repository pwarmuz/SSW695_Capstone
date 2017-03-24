
function frontPageSearch() {
    // Declare variables
    var input, filter, list, div, a, i;
    input = document.getElementById('jumbo-search');
    filter = input.value.toUpperCase();
    list = document.getElementById("book-list");
    books = list.getElementsByTagName('div');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < books.length; i++) {
        if (books[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            books[i].style.display = "";
        } else {
            books[i].style.display = "none";
        }
    }
}
