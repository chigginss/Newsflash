  "use strict";

  var bias_key = new Map([
      ['Left', 0],
      ['Left-Center', 1],
      ['Center', 2],
      ['Right-Center', 3],
      ['Right', 4],
      ['NULL', 5]
      ]);

let url = "/topsearch.json"

let margin = {top: 100, right: 100, bottom: 100, left: 100};

var width = 1200,
  height = 600,
  padding = 10, 
  clusterPadding = 15, 
  maxRadius = 100;

var n = 30, 
    m = 6; 

// var color_scale = d3.scale.linear().domain([0, median_area, max_area]).range(['blue', 'purple', 'red']);
var z = d3.scaleOrdinal(['blue', '#8000ff', 'purple', '#cc0066','red']);

var clusters = new Array(m);  

let radiusScale = d3.scaleLinear()
  .domain([1, 10])
  .range([50, maxRadius]);

 function makeCircles(response) {

  let nodes = [];

  let data = response;
  nodes = data.map((d) => {

  if (d.popularity === null) {
    d.popularity = 2;
  }
    
  let scaledRadius = radiusScale(d.popularity);

    let node = {
        title: d.title,
        source: d.source.name,
        author: d.author,
        description: d.description,
        url: d.url,
        popularity: d.popularity,
        bias: d.bias,
        cluster: bias_key.get(d.bias),
        radius: scaledRadius
    };

  if (!clusters[bias_key.get(d.bias)] || (d.radius > clusters[bias_key.get(d.bias)].radius)) {
    clusters[bias_key.get(d.bias)] = node;
  }

  return node;
  });

 var svgContainer = d3.select("body")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        

  let anchorGroup = svgContainer.append('g').attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');

  let div = d3.select("body").append("div") 
    .attr("class", "tooltip")       
    .style("opacity", 0);

  let groups = anchorGroup
        // .datum(nodes)
        // .selectAll('.circle')
        //   .data(d => d)
        .selectAll('g')
        .data(nodes)
        .enter().append('g')
        .attr('class','node')
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)) 
        .on("mouseover", function(d) {
            div.transition()    
                .duration(200)    
                .style("opacity", .9);    
            div .html( "TITLE: " + d.title+ "<br/>AUTHOR:" + d.author +"<br/>SUMMARY:" + d.description + "<br/>SOURCE:" + d.source + "<br/>BIAS:" + d.bias)  
                .style("left", (d3.event.pageX) + "px")   
                .style("top", (d3.event.pageY - 28) + "px");  
            })          
        .on("mouseout", function(d) {   
            div.transition()    
                .duration(500)    
                .style("opacity", 0); 
        });  

let circles = groups
        .append('circle')
            .attr('r', (d) => d.radius)
            .attr('fill', (d) => z(d.cluster));


    function makeTspans(text, data) {
    text.each( function(d) {
      let this_text = d3.select(this),
          words = this_text.text().split(/\s+/).reverse(),
          word,
          line = [],
          // count = 0,
          lineNumber = 0,
          // lineHeight = 2, // ems
          x = 0,
          y = this_text.attr('y'),
          // dy = parseFloat(text.attr("dy")),
          dy = 1;
      let tspan = this_text.text(null)
                           .append("tspan")
                           .attr("x", x)
                           .attr("y", y)
                           .attr("dy", dy + "em");
      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(" "));
        if (tspan.node().getComputedTextLength() > d.radius) {
          line.pop();
          tspan.text(line.join(" "));
          line = [word];
          tspan = this_text.append("tspan")
                .attr('x', x)
                .attr('y', y)
                .attr("dy", dy + 'em')
                .text(word);
          lineNumber++;
        }
      }
      this_text.attr('y', -0.65 * lineNumber + "em");

    });
  }

  let textLabels = anchorGroup
                  .selectAll('g')
                  .data(nodes)
                  .append("text")
                  .text((d) => d.title.slice(0, 40) + '...')
                  .attr('font-family', 'sans-serif')
                  .attr('font-size', '12px')
                  .attr('fill', 'black')
                  .attr('text-anchor', 'middle')
                  .call(makeTspans, nodes)
                  .on("click", function (d) {
                          window.open(d.url);
                    });
            
                    
  let textSource = anchorGroup.selectAll('.node')
                  .data(nodes)
                  .append("text")
                  .text((d) => d.source)
                  .attr('font-family', 'sans-serif')
                  .attr('font-size', '12px')
                  .attr('fill', 'black')
                  .attr('y', -32)
                  .attr('text-anchor', 'middle')


  let simulation = d3.forceSimulation(nodes)
        .velocityDecay(0.2)
        .force("x", d3.forceX().strength(.0005))
        .force("y", d3.forceY().strength(.0005))
        .force("collide", collide)
        .force("cluster", clustering)
        .on("tick", ticked);

   function translate(d) {
    return "translate(" + d.x + "," + d.y +")";
  }

  function ticked() {
      groups
        .data(nodes)
        .attr('transform', translate)
  }

  function dragstarted(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

  function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }

  function dragended(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

  function clustering(alpha) {
      nodes.forEach(function(d) {
        // debugger;
        var cluster = clusters[d.cluster];
        if (cluster === d) return;
        var x = d.x - cluster.x,
            y = d.y - cluster.y,
            l = Math.sqrt(x * x + y * y),
            r = d.radius + cluster.radius;
        if (l !== r) {
          l = (l - r) / l * alpha;
          d.x -= x *= l;
          d.y -= y *= l;
          cluster.x += x;
          cluster.y += y;
        }
      });
  }

  function collide(alpha) {
    var quadtree = d3.quadtree(nodes)
        .x((d) => d.x)
        .y((d) => d.y)
        .addAll(nodes);

    nodes.forEach(function(d) {
      var r = d.r + maxRadius + Math.max(padding, clusterPadding),
          nx1 = d.x - r,
          nx2 = d.x + r,
          ny1 = d.y - r,
          ny2 = d.y + r;
      quadtree.visit(function(quad, x1, y1, x2, y2) {

        if (quad.data && (quad.data !== d)) {
          var x = d.x - quad.data.x,
              y = d.y - quad.data.y,
              l = Math.sqrt(x * x + y * y),
              r = d.radius + quad.data.radius + (d.cluster === quad.data.cluster ? padding : clusterPadding);
          if (l < r) {
            l = (l - r) / l * alpha;
            d.x -= x *= l;
            d.y -= y *= l;
            quad.data.x += x;
            quad.data.y += y;
          }
        }
        return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
      });
    });
  }

}

$('#search-form').submit(function (e) { 
    // debugger;
    e.preventDefault();
    let s = d3.selectAll('svg');
    s.remove();
    $.post('/topsearch.json',$(e.target).serialize(), function (data) {
        makeCircles(data);
    }) 
});

// $('#search-dropdown').submit(function (e) { 
//     // debugger;
//     e.preventDefault();
//     let s = d3.selectAll('svg');
//     s.remove();
//     $.post('/topsearch.json',$(e.target).serialize(), function (data) {
//         makeCircles(data);
//     }) 
// });


