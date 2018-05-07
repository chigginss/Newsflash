 "use strict";

	var bias_key = new Map([
			['Left', 0],
			['Left-Center', 1],
			['Center', 2],
			['Right-Center', 3],
			['Right', 4],
			// ['NULL', 5]
			]);

let url = '/toptrending.json'

let margin = {top: 100, right: 100, bottom: 100, left: 100};

var width = 1400,
	height = 800,
	padding = 10, 
	clusterPadding = 15, 
	maxRadius = 120;

var n = 25, 
		m = 5; 

var z = new Map ([
		[0, '#3385ff'],
		[1, '#b3d1ff'],
		[2, '#ffe6cc'],
		[3, '#ff9999'],
		[4, '#ff6666'],
		[5, '#d9d9d9']
	])

var clusters = new Array(m);  

let radiusScale = d3.scaleLinear()
	.domain([5, 10])
	.range([70, maxRadius]);

function makeCircles(response) {
	let data = response;
	let nodes = data.map((d) => {

		let popularity = d.popularity || 5; 
		
		let author = d.author;
		if (author === null) {
				author = 'unknown';
		}

		let scaledRadius = radiusScale(popularity);

		let node = {
				title: d.title,
				source: d.source.name,
				author: author,
				description: d.description,
				url: d.url,
				urlToImage: d.urlToImage,
				popularity: popularity,
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

	let anchorGroup = svgContainer.append('g');
	// .attr('transform', 'translate');
	// (' + width / 2 + ',' + height / 2 + ')');

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
						div .html( d.title + "<hr>" + "<b>BY:</b>" + d.author.slice(0,20) + "<hr><b>SUMMARY:</b>" + d.description)  
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
						.attr('fill', (d) => z.get(d.cluster));
						
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
									.text((d) => d.title.slice(0, 35) + '...')
									.attr('font-family','Nunito Sans', 'sans-serif;')
									.attr('font-size', '11px')
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
									.attr('font-family','Nunito Sans', 'sans-serif;')
									.attr('font-size', '12px')
									.attr('font-weight', 'bold')
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
		// console.log(d.x, d.y, d.vx, d.vy);
		return "translate(" + d.x + "," + d.y +")";
	}

	function ticked() {
			groups
				.data(nodes)
				.attr("cx", function(d) { 
					if (isNaN(d.x)) {
						d.x = 0;
					}
					let new_x = Math.max(d.radius, Math.min(width - d.radius, d.x));         
					return d.x = new_x;
				})
				.attr("cy", function(d) { 
					if (isNaN(d.y)) {
						d.y = 0;
					}
					let new_y = Math.max(d.radius, Math.min(height - d.radius, d.y));
					return d.y = new_y;
				})
				.attr('transform', translate);
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
				var cluster = clusters[d.cluster];
				if (cluster === d) return;
				if (isNaN(cluster.x)) { cluster.x = 1; }
				if (isNaN(cluster.y)) { cluster.y = 1; }
				if (isNaN(d.x)) { d.x = 1; }
				if (isNaN(d.y)) { d.y = 1; }
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
			var r = d.radius + maxRadius + Math.max(padding, clusterPadding),
					nx1 = d.x - r,
					nx2 = d.x + r,
					ny1 = d.y - r,
					ny2 = d.y + r;
			quadtree.visit(function(quad, x1, y1, x2, y2) {

				if (quad.data && (quad.data !== d)) {
					if (isNaN(d.x)) { d.x = 1; }
					if (isNaN(d.y)) { d.y = 1; }
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
