'use strict';

var width = 2000,
    height = 600,
    padding = 1.5, // separation between same-color nodes
    clusterPadding = 6, // separation between different-color nodes
    maxRadius = 12;

var tooltip = d3.select("body").append("div")   
        .attr("class", "tooltip");
        // .attr("class", "tooltipContainer");
        // .style("position", "absolute")
        // .style("z-index", "10")
        // .style("visibility", "hidden")
        // .attr("class", "tooltip-news_source") 
        // .attr("class", "tooltip-art_title")
        // .attr("class", "tooltip-popularity")      
        // .attr("class", "tooltip-bias")   
        // .attr("class", "tooltip-class") 
        // .attr("class", "tooltip-info")           
        // .style("opacity", 60);   

var n = 20, // total number of nodes
    m = 5; // number of distinct clusters

var color = d3.scale.category10()
    .domain(d3.range(m));

// The largest node for each cluster.
var clusters = new Array(m);

var nodes = d3.range(n).map(function() {
  var i = Math.floor(Math.random() * m),
      r = Math.sqrt((i + 20) / m * -Math.log(Math.random())) * maxRadius,
      d = {
        bias: i,
        radius: r,
        x: Math.cos(i / m * 2 * Math.PI) * 20 + width / 2 + Math.random(),
        y: Math.sin(i / m * 2 * Math.PI) * 20 + height / 2 + Math.random(),
        art_title: "A Hard Lesson in Syria: Assad Can Still Gas His Own People", 
        authors:"David E. Sanger and Ben Hubbard", 
        news_source: "The New York Times",
        art_description:"The conflict in Syria has demonstrated a larger truth: While it is easy to blow up its chemical facilities, it is also relatively simple for the Assad government to reconstitute them elsewhere.", 
        popularity: 10, 
      };

  if (!clusters[i] || (r > clusters[i].radius)) clusters[i] = d;
  return d;
});

d3.layout.pack()
  .sort(null)
  .size([width, height])
  .children(function(d) { return d.values; })
  .value(function(d) { return d.radius * d.radius; })
  .nodes({values: d3.nest()
    .key(function(d) { return d.cluster; })
    .entries(nodes)});

var force = d3.layout.force()
    .nodes(nodes)
    .size([width, height])
    .gravity(.02)
    .charge(0)
    .on("tick", tick)
    .start();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var node = svg.selectAll("circle")
    .data(nodes)
  .enter().append("circle")
    .style("fill", function(d) { return color(d.bias); })
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
    
    node.on("mousemove", function(d) {
        tooltip.transition().duration(200).style("opacity", .9);      
        tooltip.html("bias:"+d.bias+"|authors:"+d.authors+"|source:"+d.news_source +"|title:"+d.art_title+ 
          "|description:"+d.art_description+"|popularity:"+d.popularity)  
        .style("left", (d3.event.pageX) + 15 + "px")     
        .style("top", (d3.event.pageY - 28) + "px");    
    })                  
    .on("mouseout", function(d) {       
        tooltip.transition().duration(500).style("opacity", 0);   
    });

// function wrap(text, width) {
//         text.each(function() {
//           var text = d3.select(this),
//               words = text.text().split(/\s+/).reverse(),
//               word,
//               line = [],
//               lineNumber = 0,
//               lineHeight = 1.1, // ems
//               y = text.attr("y"),
//               dy = parseFloat(text.attr("dy")),
//               tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
//           while (word = words.pop()) {
//             line.push(word);
//             tspan.text(line.join(" "));
//             if (tspan.node().getComputedTextLength() > width) {
//               line.pop();
//               tspan.text(line.join(" "));
//               line = [word];
//               tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
//             }
//           }
//         });
//       }  

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
  var quadtree = d3.geom.quadtree(nodes);
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
