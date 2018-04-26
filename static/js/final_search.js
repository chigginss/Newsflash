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
var z = d3.scaleOrdinal(d3.schemeCategory20);

var clusters = new Array(m);  

let radiusScale = d3.scaleLinear()
  .domain([1, 10])
  .range([50, maxRadius]);

 function makeCircles(response) {

  let nodes = [];

  let data = response;
  nodes = data.map((d) => {

  let scaledRadius = radiusScale(d.popularity);

    if (d.popularity === 'NULL') {
      d.popularity = 1
    }

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

  let circles = anchorGroup
        .datum(nodes)
        .selectAll('.circle')
          .data(d => d)
        .enter().append('g').attr('class','node').append('circle')
            .attr('r', (d) => d.radius)
            .attr('fill', (d) => z(d.cluster))
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

  // if (circles === null) {
  //   console.log('Sorry, No Data at this time! Please search again');
  // }


  let textLabels = anchorGroup.selectAll('.node')
                    .data(nodes)
                    .append("text")
                    .attr('x', (d) => d.x)
                    .attr('y', (d) => d.y)
                    .text((d) => d.title.slice(0, 35) + '...')
                    .attr('font-family', 'sans-serif')
                    .attr('font-size', '12px')
                    .attr('fill', 'black')
                    .on("click", function (d) {
                            window.open(d.url);
                      });
                    // .selectAll(".tick text")
                    //   .call(wrap, 80);
                    
    let textSource = anchorGroup.selectAll('.node')
                    .data(nodes)
                    .append("text")
                    .attr('x', (d) => d.x)
                    .attr('y', (d) => d.y)
                    .text((d) => d.source)
                    .attr('font-family', 'sans-serif')
                    .attr('font-size', '12px')
                    .attr('fill', 'black')


  let simulation = d3.forceSimulation(nodes)
        .velocityDecay(0.2)
        .force("x", d3.forceX().strength(.0005))
        .force("y", d3.forceY().strength(.0005))
        .force("collide", collide)
        .force("cluster", clustering)
        .on("tick", ticked);

  function ticked() {
      circles
        .attr('cx', (d) => d.x)
        .attr('cy', (d) => d.y);
      textLabels
        .attr('x', (d) => d.x - d.radius + 2)
        .attr('y', (d) => d.y);
      textSource
        .attr('x', (d) => d.x - d.radius + 2)
        .attr('y', (d) => d.y + 15);
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