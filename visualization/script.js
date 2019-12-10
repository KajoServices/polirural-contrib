var svg = d3.select("svg"),
width = +svg.attr("width"),
height = +svg.attr("height");

d3.json('graph.json').then(function(graph) {
	console.log(graph);
	//var color = d3.scaleOrdinal(d3.schemeCategory20);

	var simulation = d3.forceSimulation()
		.force("link", d3.forceLink().id(function(d) { return d.id; }))
	 	.force("charge", d3.forceManyBody().strength(-500))
		.force("center", d3.forceCenter(width / 2, height / 2));

	var tooltipdiv = d3.select("body").append("div")
		.attr("class", "tooltip")
		.style("opacity", 0);

	var link = svg.append("g")
		.attr("class", "links")
		.selectAll("line")
		.data(graph.links)
		.enter().append("line")
		.attr("stroke-width", function(d) { return Math.sqrt(1+d.value); });

	var node = svg.append("g")
		.attr("class", "nodes")
		.selectAll("g")
		.data(graph.nodes)
		.enter().append("g")
	var circles = node.append("circle")
		.attr("r", function(d) { return Math.sqrt(d.size)*3;})
		.attr("fill", function(d) { return d.color; })
		.attr("vector-effect", "non-scaling-stroke")
		.attr("stroke", "white")
		.attr("stroke-width", "2")
		.on("click", function(d) { return klick(d.id)})
		.call(d3.drag()
		.on("start", dragstarted)
		.on("drag", dragged)
		.on("end", dragended));

	var lables = node.append("text")
		.attr("text-anchor", "middle")
		.attr("font-weight", "bold")
		.style("font", "18px calibri")
		.attr("fill", "#2D0004")
		.attr("vector-effect", "non-scaling-stroke")
		.attr("stroke", "brown")
		.attr("stroke-width", ".1")
		.text(function(d) {
			return d.id.replace(/_/g,' ');
		})
		.attr('x', 0)
		.attr('y', -10)
		.on("click", function(d) { return klick(d.id)});

	node.append("title")
		.text(function(d) { return d.id; });

	simulation
		.nodes(graph.nodes)
		.on("tick", ticked);

	simulation.force("link").distance(100).strength(3)
		.links(graph.links);

	function ticked() {
		link
		.attr("x1", function(d) { return d.source.x; })
		.attr("y1", function(d) { return d.source.y; })
		.attr("x2", function(d) { return d.target.x; })
		.attr("y2", function(d) { return d.target.y; });

		node
		.attr("transform", function(d) {
			return "translate(" + d.x + "," + d.y + ")";
		})
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

	function klick(a){
		console.log("klick : "+a);
		//window.location.assign("/txtmining/similar/"+a);
	}
});