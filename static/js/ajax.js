"use strict";

function updateFavorite(results) {
    let favorites = results;
    $('#search-dropdown').html(favorites);
}

function newUserTerms() {
    $.get('/searchforkeyword', user_terms, updateFavorites);
    console.log("Ajax Request Finished");
}

$('#search-form').on('click', newUserTerms);

