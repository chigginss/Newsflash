 "use strict";

  var bias_key = new Map([
      ['Left', 0],
      ['Left-Center', 1],
      ['Center', 2],
      ['Right-Center', 3],
      ['Right', 4],
      ['NULL', 5]
      ]);

let url = '/toptrending.json'

let margin = {top: 100, right: 100, bottom: 100, left: 100};

var width = 1600,
  height = 600,
  padding = 10, 
  clusterPadding = 15, 
  maxRadius = 80;

var n = 30, 
    m = 6; 

var z = d3.scaleOrdinal(d3.schemeCategory20);

var clusters = new Array(m);  

let radiusScale = d3.scaleLinear()
  .domain([1, 10])
  .range([30, maxRadius]);

function makeCircles(response) {
  let data = response;
  let nodes = data.map((d) => { 

    let scaledRadius = radiusScale(d.popularity);
    // console.log(d.title, d.bias);
    // console.log(bias_key.get(d.bias))
    let node = {
        title: d.title,
        source: d.source.name,
        author: d.author,
        description: d.description,
        url: d.url,
        urlToImage: d.urlToImage,
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
    .selectAll('g')
    .data(nodes)
    .enter().append('g')
      .attr('class', 'node')
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


    let textLabels = anchorGroup.selectAll('.node')
                    .data(nodes)
                    .append("text")
                    .text((d) => d.title.slice(0, 35) + '...')
                    .attr('font-family', 'sans-serif')
                    .attr('font-size', '12px')
                    .attr('fill', 'black')
                    .attr('dy', '0')
                    .attr('text-anchor', 'middle')
                    .attr('dominant-baseline','central')
                    .call(wrap, 60)
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
                    .attr('y', -30)
                    .attr('text-anchor', 'middle')
                    .attr('dominant-baseline','central')

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
        // .attr("cx", function(d) { return d.x = Math.max(d.radius, Math.min(width - d.radius, d.x)); })
        // .attr("cy", function(d) { return d.y = Math.max(d.radius, Math.min(height - d.radius, d.y)); });
    }


  function wrap(text, width) {
    text.each(function() {
      var text = d3.select(this),
          words = text.text().split(/\s+/).reverse(),
          word,
          line = [],
          count = 0,
          // lineNumber = 0,
          // lineHeight = 2, // ems
          // y = text.attr('y'),
          // dy = parseFloat(text.attr("dy")),
          dy = -1,
          tspan = text.text(null)
            .append("tspan")
            .attr("x", -25)
            // .attr("y", y)
            .attr("dy", dy);
      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(" "));
        if (tspan.node().getComputedTextLength() > width) {
          line.pop();
          tspan.text(line.join(" "));
          line = [word];
          if (count === 1) {
            dy === 6;
          } else {
            dy = 12;
          }    
          count += 1      
          // let xoff = -(tspan.node().getComputedTextLength() / 2.0);
          tspan = text.append("tspan")
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline','middle')
                .attr("x", -4)
                // .attr("y", y)
                .attr("dy", dy).text(word);
                // ++lineNumber * lineHeight + dy
        }
      }
    });
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

$.get(url, makeCircles);
