"use strict";

  // var outlets = new Map([
  //     ['CNN', {popularity: 10, bias: 'Left'}],
  //     ['The New York Times', {popularity: 10, bias: 'Left-Center'}],
  //     ['The Washington Post', {popularity: 10,bias: 'Left-Center'}],
  //     ['Wired', {popularity: 9,bias: 'Left-Center'}],
  //     ['BBC News', {popularity: 9,bias: 'Left-Center'}],
  //     ['The Wall Street Journal', {popularity: 9,bias: 'Right-Center'}],
  //     ['TechCrunch', {popularity: 8,bias:'Left-Center'}],
  //     ['Fox News', {popularity: 8,bias: 'Right'}],
  //     ['Bloomberg', {popularity: 8,bias: 'Left-Center'}],
  //     ['USA Today', {popularity: 8,bias: 'Center'}],
  //     ['Time', {popularity: 8,bias: 'Center'}],
  //     ['Engadget', {popularity: 6,bias: 'Left-Center'}],
  //     ['Politico', {popularity: 6,bias: 'Left-Center'}],
  //     ['Fortune', {popularity: 7,bias: 'Right-Center'}],
  //     ['NBC News', {popularity: 7,bias: 'Left-Center'}],
  //     ['ABC News', {popularity: 7,bias: 'Left-Center'}],
  //     ['CNBC', {popularity: 7,bias: 'Left-Center'}],
  //     ['CBS News', {popularity: 7,bias: 'Left-Center'}],
  //     ['Breitbart News', {popularity: 6,bias: 'Right'}],
  //     ['Associated Press', {popularity: 6,bias: 'Center'}],
  //     ['Business Insider', {popularity: 6,bias: 'Left-Center'}]
  //     ]);

  var bias_key = new Map([
      ['Left', 0],
      ['Left-Center', 1],
      ['Center', 2],
      ['Right-Center', 3],
      ['Right', 4],
      ['NULL', 5]
      ]);

// let endPoint = "https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal,the-new-york-times,bbc-news,techcrunch,the-washington-post,cnn,fox-news,breitbart-news,time,wired,business-insider,usa-today,politico,cnbc,engadget,nbc-news,cbs-news,abc-news,associated-press,fortune&apiKey=";
// let apiKey = "1ec5e2d27afa46efaf95cfb4c8938f37";
let url = "/toptrendingjson"

let margin = {top: 100, right: 100, bottom: 100, left: 100};

var width = 2000,
  height = 700,
  padding = 10, 
  clusterPadding = 15, 
  maxRadius = 100;

var n = 20, 
    m = 6; 

var z = d3.scaleOrdinal(d3.schemeCategory20);
    // clusters = new Array(m);

var clusters = new Array(m);  

let radiusScale = d3.scaleLinear()
  .domain([1, 10])
  .range([60, maxRadius]);

  console.log(radiusScale(10));

function makeCircles(response) {
  let data = response.articles;
  let nodes = data.map((d) => { 

    let scaledRadius = radiusScale(outlets.get(d.source.name).popularity);
  d = {
    title: d.title,
    source: d.source.name,
    author: d.author,
    description: d.description,
    url: d.url,
    popularity: outlets.get(d.source.name).popularity,
    bias: outlets.get(d.source.name).bias,
    cluster: bias_key.get(outlets.get(d.source.name).bias),
    radius: scaledRadius
  };

  if (!clusters[bias_key.get(d.bias)] || (d.radius > clusters[bias_key.get(d.bias)].radius)) {
    clusters[bias_key.get(d.bias)] = d;
  }

  return d;
  });
  console.log(nodes);
  console.log(clusters);

  var svgContainer = d3.select("body")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append('g').attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');

  let div = d3.select("body").append("div") 
    .attr("class", "tooltip")       
    .style("opacity", 0);

  let circles = svgContainer.append('g')
        .datum(nodes)
        .selectAll('.circle')
          .data(d => d)
        .enter().append('circle')
            .attr('r', (d) => d.radius)
            .attr('fill', (d) => z(d.cluster))
        // .append("text")
        //     .text(function (d) {
        //     return d.title;
        //   })
        //     .attr("dx", -10)
        //     .attr("dy", ".35em")
        //     .text(function (d) {
        //     return d.title
        //   })
        // .style("stroke", "gray")
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


  let simulation = d3.forceSimulation(nodes)
        .velocityDecay(0.2)
        .force("x", d3.forceX().strength(.0005))
        .force("y", d3.forceY().strength(.0005))
        .force("collide", collide)
        .force("cluster", clustering)
        .on("tick", ticked);
        // .on("tick");

  function ticked() {
      circles
        .attr('cx', (d) => d.x)
        .attr('cy', (d) => d.y);
  }

  // function tick(e) {
  //   circles.each(cluster(10 * e.alpha * e.alpha))
  //       .each(collide(.5))
  //   //.attr("transform", functon(d) {});
  //   .attr("transform", function (d) {
  //       var k = "translate(" + d.x + "," + d.y + ")";
  //       return k;
  //   })

  // }

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

$.get(url, makeCircles);

