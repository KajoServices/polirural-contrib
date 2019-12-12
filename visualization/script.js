var svg = d3.select("svg"),
width   = +svg.attr("width"),
height  = +svg.attr("height");

//var graph_url = "graph.json"
function graph_url(topic) {
	var base_url = "http://178.62.250.117/api/v1/similarity_cluster/?";
	var params = new URLSearchParams({
		"username": "kajo_connect",
		"api_key": "3d0a2921a8b57cccf4214753bd53eed5f2dcab0f",
		"lang": "en",
		"topic": topic,
		"threshold": "0.6"
	});

	url = base_url + params.toString();
	console.log(url);
	return url;
}

var simulation, link, node;
var color = d3.scaleOrdinal(d3.schemeCategory10);

d3.json(graph_url("cereal production")).then(function(graph) {
	console.log(graph);
	//var color = d3.scaleOrdinal(d3.schemeCategory20);

	simulation = d3.forceSimulation()
    	.force("charge", d3.forceManyBody().strength(-1000))
    	.force("link", d3.forceLink().id(function(d) { return d.id; }).distance(50))
    	//.force("link", d3.forceLink().id(function(d) { return d.id; }))
    	//.force("charge", d3.forceManyBody().strength(-500))
		.force("center", d3.forceCenter(width / 2, height / 2))
    	.force("x", d3.forceX())
    	.force("y", d3.forceY());
    	//.alphaTarget(1)
    	//.on("tick", ticked);
	
	link = svg.append("g")
		.attr("class", "links")
		.attr("stroke", "#000")
		.attr("stroke-width", 1.5)
		.selectAll(".link");
	
	node = svg.append("g")
		.attr("class", "nodes")
		.attr("stroke", "#fff")
		.attr("stroke-width", 1.5)
		.selectAll(".node");

	restart(graph);
});

function restart(graph) {
	// Apply the general update pattern to the nodes.
	node = node.data(graph.nodes, function(d) { return d.id;});
	node.exit().remove();

	var g = node.enter().append("g")
		.attr("class", "node");

	g.append("circle")
		.attr("r", function(d) { return Math.sqrt(d.size)*3;})
		.attr("fill", function(d) { return d.color; })
		.attr("vector-effect", "non-scaling-stroke")
		.attr("stroke", "white")
		.attr("stroke-width", "2")
		.on("click", function(d) { return click(d.id)});
	
	g.append("text")
		.attr("text-anchor", "middle")
		.attr("font-weight", "bold")
		.style("font", "12px calibri")
		.attr("fill", "#2D0004")
		.attr("vector-effect", "non-scaling-stroke")
		.attr("stroke", "brown")
		.attr("stroke-width", ".1")
		.text(function(d) {
			return d.id.replace(/_/g,' ');
		})
		.attr('x', 0)
		.attr('y', -10)
		.on("click", function(d) { return click(d.id)});

	node = g.merge(node);

	// Apply the general update pattern to the links.
	link = link.data(graph.links, function(d) { return d.source.id + "-" + d.target.id; });
	link.exit().remove();
	link = link.enter().append("line").merge(link);

	// Update and restart the simulation.
	simulation.nodes(graph.nodes);
	simulation.force("link").links(graph.links);
	simulation.on("tick", ticked);
	simulation.alpha(1).restart();
}

function ticked() {
  link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  node.attr("transform", function(d) { 
  	return "translate(" + d.x + "," + d.y + ")"; });
}

function click(topic){
	console.log("click : " + topic);
	d3.json(graph_url(topic)).then(function(graph) {
		console.log(graph);
		restart(graph);
	});
}
