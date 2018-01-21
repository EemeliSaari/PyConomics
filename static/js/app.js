// Entry point
$(function() {
    //debugging purposes
    createGraph("PIZZA");
});

function getData(symbol){
    //TODO
}

function updateGraph() {
    var symbol = document.getElementById('stockInput').value;

    if (symbol){
        // Update title
        var title = d3.select("#title").select("h2")
            .text(symbol);
    };
    //TODO update the graph
}

function createGraph(symbol) {

    var title = d3.select("#title").append("h2")
        .text(symbol)

    var width = 720;
    var height = 480;

    var parseTime = d3.timeParse("%d.%m.%Y");
    var format = d3.format(",.2f");
    var svg = d3.select("#chart").append("svg")
        .attr("width", width)
        .attr("height", height);

    var canva = d3.select("svg"),
        marging = {top: 20, right: 20, bottom:30, left:50},
        width = +svg.attr("width") - marging.left - marging.right
        height = +svg.attr("height") - marging.top - marging.bottom,
        g = svg.append("g")
            .attr("transform", "translate(" + marging.left + "," + marging.top + ")");

    var x = d3.scaleTime()
        .rangeRound([0, width]);
    
    var y = d3.scaleLinear()
        .rangeRound([height, 0]);

    var line = d3.line()
        .x(function(d) {return x(parseTime(d.date)); })
        .y(function(d) {return y(+d.close); });

    var url = "/data/" + symbol
    d3.json(url, function(error, data){

        if (error) throw error;
        console.log(data)
        x.domain(d3.extent(data, function(d) { return parseTime(d.date); }));
        y.domain(d3.extent(data, function(d) { return +d.close; }));

        g.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))
            .select(".domain")
            .remove();

        g.append("g")
            .call(d3.axisLeft(y))
            .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("Price");

        g.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "crimson")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 1)
            .attr("d", line)
            .text("Date");
    });
}