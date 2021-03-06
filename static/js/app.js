// Entry point
$(function() {
    //debugging purposes
    let graph = new Graph();
    graph.create('ELISA')

    document.getElementById('searchButton').addEventListener("click", function() { graph.newGraph();}, false);
    //document.getElementById('max_scale').addEventListener("toggle", function() {graph.scaleGraph();}, false);
    //document.getElementById('1y_scale').addEventListener("toggle", function() {graph.scaleGraph();}, false);
    //document.getElementById('1m_scale').addEventListener("toggle", function() {graph.scaleGraph();}, false);
    //document.getElementById('1wk_scale').addEventListener("toggle", function() {graph.scaleGraph();}, false);
    $(document).ready()
});

var Graph = function(){
    var parseTime = d3.timeParse("%d.%m.%Y");

    var width = 720;
    var height = 480;

    var svg = d3.select("#chart").append("svg")
        .attr("width", width)
        .attr("height", height);

    var canva = d3.select("svg"),
        marging = {top: 20, right: 20, bottom:30, left:50},
        width = +svg.attr("width") - marging.left - marging.right
        height = +svg.attr("height") - marging.top - marging.bottom
        g = svg.append("g")
            .attr("transform", "translate(" + marging.left + "," + marging.top + ")");

    var x = d3.scaleTime()
        .rangeRound([0, width]);

    var y = d3.scaleLinear()
        .rangeRound([height, 0]);

    var data;

    var line = d3.line()
        .x(function(d) {return x(parseTime(d.date)); })
        .y(function(d) {return y(+d.close); });

    return{
        create : function(symbol){
            var title = d3.select("#title").append("h2")
                .text(symbol)

            var url = "/data/" + symbol
            d3.json(url, function(error, json){

                if (error) throw error;

                data = json;

                x.domain(d3.extent(json, function(d) { return parseTime(d.date); }));
                y.domain(d3.extent(json, function(d) { return +d.close; }));

                g.append("g")
                    .attr("transform", "translate(0," + height + ")")
                    .attr("class", "xAxis")
                    .call(d3.axisBottom(x));

                g.append("g")
                    .attr("class" , "yAxis")
                    .call(d3.axisLeft(y));

                g.append("path")
                    .datum(data)
                    .attr("class", "line")
                    .attr("fill", "none")
                    .attr("stroke", "crimson")
                    .attr("stroke-linejoin", "round")
                    .attr("stroke-linecap", "round")
                    .attr("stroke-width", 1)
                    .attr("d", line(json))
                    .text("Date");
            });
        },

        scaleGraph : function(){
            //TODO
            console.log("hello")
        },

        newGraph : function(){
            symbol = document.getElementById('stockInput').value;
            if (symbol){
                // Update title
                var title = d3.select("#title").select("h2")
                    .text(symbol);
                url = "/data/" + symbol
                d3.json(url, function(error, json){
                    if (error) throw error
                    
                    data = json;

                    //TODO handle 404 invalid search

                    x.domain(d3.extent(json, function(d) { return parseTime(d.date); }));
                    y.domain(d3.extent(json, function(d) { return +d.close; }));

                    this.svg = d3.select("#chart").transition();

                    this.svg.select(".line")
                        .duration(750)
                        .attr("d", line(json));

                    this.svg.select(".xAxis")
                        .duration(750)
                        .call(d3.axisBottom(x));

                    this.svg.select(".yAxis")
                        .duration(750)
                        .call(d3.axisLeft(y));
                });
            };
        }
    }
}
