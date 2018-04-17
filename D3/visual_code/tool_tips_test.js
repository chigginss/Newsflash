'use strict';

var width = 2000,
    height = 600,
    padding = 1.5, // separation between same-color circles/groups
    clusterPadding = 6, // separation between different-color circles/groups
    maxRadius = 12;

var tooltip = d3.select("body").append("div")   
        .attr("class", "tooltip");

var n = 20, // total number of circles/groups
    m = 5; // number of distinct clusters

var color = d3.scale.category10()
    .domain(d3.range(m));

// The largest node for each cluster.
var clusters = new Array(m);

// let endPoint = "https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal,the-new-york-times,bbc-news,techcrunch,the-washington-post,cnn,fox-news,breitbart-news,time,wired,business-insider,usa-today,politico,cnbc,engadget,nbc-news,cbs-news,abc-news,associated-press,fortune&apiKey=";
// let apiKey = "b033aef85417499e96a7cd8148b0e7d4";
// let url = endPoint + apiKey;

// function displayData(results) {
//     return results;
// }

// function getJson() {
//   let d = $.getJSON(url, displayData);
// }

// getJson();

// d3.json("", function(error, data) {
  for (var i = 0; i < data.length; i++) {
    var obj = data[i];
    for (var key in obj) {
      // var cluster = div;
      // var r = 100; // popularity * 100 radius
      var t = obj['title']; // title
      var s = obj['source']; // source
      var a = obj['author']; // author
      var des = obj['description']; // description
      var p = outlets.get(s)[0]; // number to scale
      var b = outlets.get(s)[1];
      d = {
        cluster: div,
        radius: r,
        title: t,
        description: des,
        source: s
      };
      // d = {cluster: div, radius: r};
      // console.log(key+"="+obj[key]);
    }
    if (!clusters[i] || (r > clusters[i].radius)) clusters[i] = d;
    groups.push(d);

    console.log(d);
  }

d3.layout.pack()
  .sort(null)
  .size([width, height])
  .children(function(d) { return d.values; })
  .value(function(d) { return d.radius * d.radius; })
  .groups({values: d3.nest()
    .key(function(d) { return d.cluster; })
    .entries(groups)});

var force = d3.layout.force()
    .groups(groups)
    .size([width, height])
    .gravity(.02)
    .charge(0)
    .on("tick", tick)
    .start();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var node = svg.selectAll("circle")
    .data(groups)
  .enter().append("circle")
    .style("fill", function(d) { return color(d.cluster); })
    .call(force.drag);

node.append("text")
    .text(function(d) {
      return d.name;
    })
    .attr("dx", -10)
    .text(function(d) {
      return d.news_source
    })
    .style("stroke", "white");

node.selectAll("circle").transition()
    .duration(750)
    .delay(function(d, i) {
      return i * 5;
    })
    .attrTween("r", function(d) {
      var i = d3.interpolate(0, d.radius);
      return function(t) {
        return d.radius = i(t);
      };
    });

node.transition()
    .duration(750)
    .delay(function(d, i) { return i * 5; })
    .attrTween("r", function(d) {
      var i = d3.interpolate(0, d.radius);
      return function(t) { return d.radius = i(t); };
    });

    var tooltip = d3.select("body").append("div")   
        .attr("class", "tooltip");
    
    node.on("mousemove", function(d) {
        tooltip.transition().duration(200).style("opacity", .9);      
        tooltip.html("|authors:"+d.authors+"|source:"+d.news_source +"|title:"+d.art_title+ 
          "|description:"+d.art_description+"|popularity:"+d.popularity)  
        .style("left", (d3.event.pageX) + 15 + "px")     
        .style("top", (d3.event.pageY - 28) + "px");    
    })                  
    .on("mouseout", function(d) {       
        tooltip.transition().duration(500).style("opacity", 0);   
    });

function tick(e) {
  node
      .each(cluster(10 * e.alpha * e.alpha))
      .each(collide(.5))
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
}

// Move d to be adjacent to the cluster node.
function cluster(alpha) {
  return function(d) {
    var cluster = clusters[d.bias];
    if (cluster === d) return;
    var x = d.x - cluster.x,
        y = d.y - cluster.y,
        l = Math.sqrt(x * x + y * y),
        r = d.radius + cluster.radius;
    if (l != r) {
      l = (l - r) / l * alpha;
      d.x -= x *= l;
      d.y -= y *= l;
      cluster.x += x;
      cluster.y += y;
    }
  };
}

// Resolves collisions between d and all other circles.
function collide(alpha) {
  var quadtree = d3.geom.quadtree(groups);
  return function(d) {
    var r = d.radius + maxRadius + Math.max(padding, clusterPadding),
        nx1 = d.x - r,
        nx2 = d.x + r,
        ny1 = d.y - r,
        ny2 = d.y + r;
    quadtree.visit(function(quad, x1, y1, x2, y2) {
      if (quad.point && (quad.point !== d)) {
        var x = d.x - quad.point.x,
            y = d.y - quad.point.y,
            l = Math.sqrt(x * x + y * y),
            r = d.radius + quad.point.radius + (d.cluster === quad.point.cluster ? padding : clusterPadding);
        if (l < r) {
          l = (l - r) / l * alpha;
          d.x -= x *= l;
          d.y -= y *= l;
          quad.point.x += x;
          quad.point.y += y;
        }
      }
      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
    });
  };
}
