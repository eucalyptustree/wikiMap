function moveSliders(startTime, endTime){
    console.log("Move sliders in streamgraph");
    $('#draggable1').css('left', String(startTime*(600/23))+'px');
    $('#draggable2').css('left', String(endTime*(600/23))+'px');
    setCovers();
  }

function setCovers(){
    $('#top-wrapper').html();
          var position1 = $("#draggable1").position().left;
          var position2 = $("#draggable2").position().left;
          if(position2 > position1){
              //Only one div
              $('#top-wrapper').html('<div class="cover" style="left:'+String(position1)+'px;width:'+String(position2-position1)+'px"></div>');
          }else{
              //Two divs
              var position1 = $("#draggable1").position().left;
              var position2 = $("#draggable2").position().left;           
              $('#top-wrapper').html('<div class="cover" style="left:0px;width:'+String(position2)+'px"></div>');
              $('#top-wrapper').append('<div id="top-wrapper2"><div class="cover" id="rightCover" style="left:'+String(position1)+'px;"></div></div>');
              $('#rightCover').css('width', String($("#top-wrapper2").width()-position1)+'px');

          }
  }
  
// runs on load (in html head)
function streamgraphLoad() {
  $(function() {
    var step = $("#containment-wrapper").width()/23;
    $( ".draggable" ).draggable({ axis: "x",containment: "#containment-wrapper", scroll: false, grid: [ step, step ] });
    for (var i=0;i<24;i++){
        $('#x-axis').append('<div class="axisLabel" style="position:relative;display:inline-block;width:20px;left:'+String((step-20)*i)+'px;">'+String(i)+'</div>');
    }
    $('#x-axis').append('<div id="x-axisText" style="position:relative;width:100%;text-align:center">TIME OF DAY IN HOURS, UTC</div>');
    $( ".draggable" ).draggable({
    
      drag: function() {
        setCovers();
      },
stop: function() {
           var start = parseInt(($("#draggable1").position().left/600)*23);
           var end = parseInt(($("#draggable2").position().left/600)*23);
           var setTimes = [end,start]
           var setLans = getChecks();
           console.log('passing args:'+'['+end+','+start+']');
           console.log(setLans);
          passArgs(setTimes,setLans);
     }
    });

  });

 }
  
 
// runs in body  

function streamgraphBody() {
	console.log("streamgraph body");
var total = 0;
var margin = { top: 5, right: 40, bottom: 20, left: 30 };
var width=600;
var height = 500;
var currentChart = "normalized";
var dataInfo1 = ["./data/data.csv", "See Normalized Data", "percent% of language Wikipedia edits are made at time:00 UTC", "Wikipedia Edits Over 24 Hours - Normalized Data"];
var totalPercents = [];

var x = d3.scale.linear().domain([0, 23]).range([0, width]);
var y = d3.scale.linear().range([height, 0]);
var timearray = [];

var colorrange = ["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c", "98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5", "8c564b"];
var z = d3.scale.category20();

var svg = d3.select(".chart").append("svg")
  .append("g");

var stack = d3.layout.stack()
  .offset("zero")
  .values(function(d) { return d.values; })
  .x(function(d) { return d.time; })
  .y(function(d) {return d.value; });
  
var area = d3.svg.area().interpolate("cardinal")
    .x(function(d) { return x(d.time); })
    .y0(function(d) { return y(d.y0); })
    .y1(function(d) {return y(d.value + d.y0); });
    
var tooltip = d3.select(".chart")
   .append("div")
   .attr("class", "remove")
   .style("position", "absolute")
   .style("z-index", "20")
   .style("visibility", "hidden")
   .style("top", "85px")
   .style("left", "75px");
   

    
window.onload = function(){
    var chart = d3.csv(dataInfo1[0], function(csv) {
      data = csv;
      var languages = getChecks();
        drawChart(languages);
    });
}



function drawChart(languages){
console.log("drawing chart! Language array is:");
console.log(getChecks());
  var dimensions = d3.keys(data[0]).filter(function(key) { return key != "time"; });

  var layers = dimensions.map(function(name){

    if(languages.indexOf(name) != -1){
    return {
        key: name,
        values: data.map(function(d) { 
            return { time: d.time, value: +d[name], language: name };
        })
    };
    }else{
        return {
            key: name,
            values: data.map(function(d) { 
                return { time: d.time, value: 0, language: name };
            })
        };
    }
  });
  
  var total = 0;
  for(var i = 0; i < data.length; i++) { 
    var row = data[i];
        row = d3.values(row);
    var rowsum = 0;
    for (var j in row) {
        if(j!=0) {
            rowsum += +row[j];
        }
    }
    if(rowsum > total) {
        total = rowsum;
    }
    totalPercents[i] = rowsum;   
  }
  total = total + 0.2;
  y.domain([0, total]);
  

    
  svg.selectAll(".layer")
    .data(stack(layers))
    .enter().append("path")
    .attr("class", "layer")
    .attr("id", function(d){return d.key;})
    .attr("d", function(d) { return area(d.values); })
    .style("fill", function(d, i){ return z(i); })
    .on("mousemove", function(d, i) {
        var percent = d.values[parseInt(24*(d3.mouse(this)[0]/width))]['value'];
        if(dataInfo1[2] == "percent% of all Wikipedia edits made at time:00 UTC are made in language"){
            percent =  parseFloat(parseInt((percent/totalPercents[parseInt(24*(d3.mouse(this)[0]/width))])*10000))/100;
        }
        tooltipText = dataInfo1[2].replace("language", d.key);
        tooltipText = tooltipText.replace("percent", percent);
        tooltipText = tooltipText.replace("time", parseInt(24*(d3.mouse(this)[0]/width)));

        console.log(tooltipText);
        tooltip.html(tooltipText).style("visibility", "visible");
        svg.selectAll(".layer")
      .attr("opacity", 1);
    })
    .on("click", function(d, i) {
      svg.selectAll(".layer").transition()
      .duration(250)
      .attr("opacity", function(d, j) {
        return j != i ? 0.2 : 1;
    })})
    .on("mouseout", function(d, i) {
      tooltip.style("visibility", "hidden");
    })
    .transition()
    .duration(2000);
}


  $('.language').click(function() {
      var languageArray = [];

  d3.select(".chart svg").remove();
  svg = d3.select(".chart").append("svg").append("g");
  drawChart(getChecks());
  });
}

function drawChart(languages){
console.log("drawing chart! Language array is:");
console.log(getChecks());
  var dimensions = d3.keys(data[0]).filter(function(key) { return key != "time"; });

  var layers = dimensions.map(function(name){

    if(languages.indexOf(name) != -1){
    return {
        key: name,
        values: data.map(function(d) { 
            return { time: d.time, value: +d[name], language: name };
        })
    };
    }else{
        return {
            key: name,
            values: data.map(function(d) { 
                return { time: d.time, value: 0, language: name };
            })
        };
    }
  });

  y.domain([0, 50]);
  

    
  svg.selectAll(".layer")
    .data(stack(layers))
    .enter().append("path")
    .attr("class", "layer")
    .attr("id", function(d){return d.key;})
    .attr("d", function(d) { return area(d.values); })
    .style("fill", function(d, i){ return z(i); })
    .on("mousemove", function(d, i) {
        var percent = d.values[parseInt(24*(d3.mouse(this)[0]/width))]['value'];
        if(dataInfo1[2] == "percent% of all Wikipedia edits made at time:00 UTC are made in language"){
            percent =  parseFloat(parseInt((percent/totalPercents[parseInt(24*(d3.mouse(this)[0]/width))])*10000))/100;
        }
        tooltipText = dataInfo1[2].replace("language", d.key);
        tooltipText = tooltipText.replace("percent", percent);
        tooltipText = tooltipText.replace("time", parseInt(24*(d3.mouse(this)[0]/width)));

        console.log(tooltipText);
        tooltip.html(tooltipText).style("visibility", "visible");
        svg.selectAll(".layer")
      .attr("opacity", 1);
    })
    .on("click", function(d, i) {
      svg.selectAll(".layer").transition()
      .duration(250)
      .attr("opacity", function(d, j) {
        return j != i ? 0.2 : 1;
    })})
    .on("mouseout", function(d, i) {
      tooltip.style("visibility", "hidden");
    })
    .transition()
    .duration(2000);
}
 





