




Would have to either use a saved file (not live) or figure out a way to have standard output constantly override file
// Add json directly to D3 - http://www.tutorialsteacher.com/d3js/loading-data-from-file-in-d3js
d3.json("/data/users.json", function(error, data) {
    
    d3.select("body")
        .selectAll("p")
        .data(data)
        .enter()
        .append("p")
        .text(function(d) {
            return d.name + ", " + d.location;
        });

});

// Add CSV - http://www.tutorialsteacher.com/d3js/loading-data-from-file-in-d3js

<script>
d3.csv("/data/employees.csv", function(data) {
    for (var i = 0; i < data.length; i++) {
        console.log(data[i].Name);
        console.log(data[i].Age);
    }
});
</script>
