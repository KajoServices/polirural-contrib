// Based on: d3-force: minimal working example
// https://bl.ocks.org/puzzler10/4efcb280a23c2f9b824879771ae41592
var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");
    
d3.json('graph.json').then(function(graph) {    
    console.log(graph)

    // NODES
    //set up the simulation 
    //nodes only for now 
    var simulation = d3.forceSimulation().nodes(graph.nodes);	
                        
    //add forces
    //we're going to add a charge to each node 
    //also going to add a centering force
    simulation
        .force("charge_force", d3.forceManyBody())
        .force("center_force", d3.forceCenter(width / 2, height / 2));

    //draw circles for the nodes 
    var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(graph.nodes)
            .enter()
            .append("circle")
            .attr("r", 5)
            .attr("fill", "red");  

    //add tick instructions: 
    simulation.on("tick", tickActions);

    // LINKS
    //Create the link force 
    //We need the id accessor to use named sources and targets 
    var link_force =  d3.forceLink(graph.links)
                            .id(function(d) { return d.id; })

    //Add a links force to the simulation
    //Specify links  in d3.forceLink argument   
    simulation.force("links", link_force)

    //draw lines for the links 
    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
        .attr("stroke-width", 2);        
                        
    function tickActions() {
        //update circle positions each tick of the simulation 
        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
            
        //update link positions 
        //simply tells one end of the line to follow one node around
        //and the other end of the line to follow the other node around
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
    }                    
});
