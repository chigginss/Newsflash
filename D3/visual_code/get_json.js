"use strict";

let endPoint = "https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal,the-new-york-times,bbc-news,techcrunch,the-washington-post,cnn,fox-news,breitbart-news,time,wired,business-insider,usa-today,politico,cnbc,engadget,nbc-news,cbs-news,abc-news,associated-press,fortune&apiKey=";
let apiKey = "b033aef85417499e96a7cd8148b0e7d4";
let url = endPoint + apiKey;

let d;

function displayData(results) {
    console.log(results);
    return results;
}

function getJson() {
    $.getJSON(url, displayData);
}

getJson();