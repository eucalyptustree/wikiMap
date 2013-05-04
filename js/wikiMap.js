var jsonStore   = {};                                   // jsonStore is used to cache the json data for each language & hour
var languageColors = {}                                 // languageColors is used to apply fill color by language to points rendered
var mlanguages   = ['en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','cs']
var curHours    = [];                                   // Hours and Languages arrays for determining what is displayed, and what should be displayed on the map
var curLan      = [];
var newHours    = [];
var newLan      = [];                     
var setHours    = [0,12];                               // Initial data value to display

// console.log('in wikimap.js');


function initialCache() {                               // Load data for all mlanguages.
    console.log('caching data for all mlanguages');
    // console.log(mlanguages);
    for (var i=0; i<mlanguages.length; i++)  {
        // console.log('curlan ', mlanguages[i]);
        loadData(mlanguages[i],-1);
    }
}

function loadData(lan,hour){                            // load data for a specified (lan)guage and hour
    var filename = lan+hour+'.json';
    d3.json("./data/"+filename, function(json) {        
            // console.log('loading data for: '+lan)            
            jsonStore[lan+hour] = json
            // console.log(jsonStore[lan+hour]);
            // if (lan === 'cs') {
            if (getKeys(jsonStore).length === 20) {     // This is kind of sloppy, but checks that all 20 data files are loaded, and then finishes the pageload - rendering the data points on the map, re-rendering countries (enables tooltip function), and removing the "Loading..." warning.
                console.log('done loading data, attempting to render');
                renderAll();
                renderCountries();
                passArgs([0,23],['en']);
                d3.select('#loadingText').remove();
                
                
                // introJs().start();
            }
            // }   
    });
}  

function renderMap() {                                  // Renders the blank map and initializes the points container
    var xy = d3.geo.mercator()
    path = d3.geo.path().projection(xy).pointRadius(2.0);
    var states = d3.select("#map")
        .append("svg")
        .append("g")
        //.attr("class", "states")
        .attr('id','states');    
        
    d3.select("svg").append('text')
        .text('Loading...')
        .attr('id','loadingText')
        .attr('x',210).attr('y',250);
        
    var points = d3.select("svg")                       // Create the points svg group
        .append("g")
        .attr('class','points');

    
    d3.json("./data/world-countries.json", function(collection) {    // Load in the states & equator data from the file 'world-countries.json'              
        // console.log(collection.features);
        states
            .selectAll("path")
            .data(collection.features)
            .enter().append("path")
            .attr("d", path)
            .attr('fill-opacity',0)
            // .attr("class", 'states')
            .append("title")
            .text(function(d) {
            // console.log(d.properties['name']);
            return d.properties['name']; 
            })
            .on("mouseover", function(){return tooltip;});
    });
    
    //adjust viewframe to fit window
    var translate = xy.translate();
    translate[0] = 300;
    translate[1] = 260;
    xy.translate(translate); // center the view
    xy.scale(96);
};

function clearMap() {                                   // Clear map to render fresh 
    console.log('clearing map');
    var curPoints = d3.selectAll('.points').style('visibility','hidden');}

function colorArray() {                                 // Establishes an array based on the color selection.
    // var mlanguages = ['en','de','fr','nl','it','ru','es','pl','sv','ja']         // 10 mlanguages
    // var colors = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b",  // 10 colors
            // "#e377c2","#7f7f7f","#bcbd22","#17becf"]
    var mlanguages = ['en','de','fr','nl','it','ru','es','pl','sv','ja',       // 20 mlanguages
     'pt','zh','vi','uk','ca','no','ceb','fi','war','cs']
    var colors = ['#1f77b4','#aec7e8','#ff7f0e','#ffbb78','#2ca02c','#98df8a',  //20 colors, taken from d3.scale.category20().
    '#d62728','#ff9896','#9467bd','#c5b0d5','#8c564b','#c49c94','#e377c2','#f7b6d2',
    '#7f7f7f','#c7c7c7','#bcbd22','#dbdb8d','#17becf','#9edae5']
    
    for (var i = 0; i < mlanguages.length; i++) { languageColors[mlanguages[i]]=colors[i]; }
    // console.log(languageColors);
}

function renderPoints(lan) {                            // Renders the data points for a given language.
    // console.log('rendering points for: '+lan);
    collection = jsonStore[lan+'-1'];
    // console.log(collection);
    d3.select("svg")
    .append('g')
    .selectAll("path")
    .data(collection.features)
    .enter().append("path")
    .attr("d", path)
    .attr("class",function(d) {                         // Apply a class to each point for it (l)anguage and (h)our, allowing for time- and language-specific masks.})
        return 'points '+d.properties.l+' '+d.properties.l+d.properties.h;
            })     
    .attr("stroke-width",0)
    .style("fill", function(d) {  return languageColors[lan]  })
    .style("opacity",function(d) {  return d.properties.e * 0.04;  })
    .style('visibility', 'hidden');
    
}

function renderAll() {                                  // Renders each language in turn
    for (var i = 0; i < mlanguages.length; i++) {
        // console.log('rendering ',mlanguages[i]);
        renderPoints(mlanguages[i]);
        }
    console.log('finished rendering');
}

function renderCountries() {                            // Draws a second map of the countries, with partial stroke opacity and 0 fill opacity, to display on top of the rendered data points. Enables the tooltip to work properly, and also aids visual acuity.
    d3.json("./data/world-countries.json", function(collection) {
        // console.log(collection.features);
        var states = d3.select("svg")
        .append("g").attr('id','states')
        .selectAll("path")
        .data(collection.features)
        .enter().append("path")
        .attr("d", path)
        .attr('fill-opacity',0)
        .attr('stroke-opacity',0.4)
        .append("title")
        .text(function(d) { 
        // console.log(d.properties['name']);
        return d.properties['name']; 
        })
        .on("mouseover", function(){return tooltip;});
    });
}

function getChecks() {                                  // Gets the currently checked mlanguages, returned as an array.
    var lanArray = [];
    var checkboxes = document.getElementsByClassName('language');            
    for (var i = 0, length = checkboxes.length; i < length; i++) {
        if (checkboxes[i].checked) {
            lanArray.push(checkboxes[i].value);
        }
    }
    // console.log(lanArray);
    return lanArray;
}
function genHours(times) {                              // Generates an array of hours based on a start (times[0]) and end time (times[1])
    var hours = []
    if (times[0] < times[1]) { 
        for (var i = times[0]; i <= times[1]; i++) {  hours.push(i);  } 
    }
    else if (times[0]===times[1]) { 
    } //what do?
    else if (times[0] > times[1]) {
        for (var i = times[0]; i <= 23; i++) {  hours.push(i);  }
        for (var i = 0; i <= times[1]; i++)  {  hours.push(i);  }
    }
    // console.log(hours);
    return hours;
}

function makeVisible(lan,hr) {                          // These two functions toggle visibility for a given lan(guage) and hr.
    d3.selectAll('.'+lan+hr).style('visibility','visible');  
}
function makeHidden(lan,hr)  {  
    d3.selectAll('.'+lan+hr).style('visibility','hidden');  
}
function makeVisibleLan(lan) {                          // These two functions toggle visibility for all points of a given lan(guage) (i.e. for hours 0-23)
    d3.selectAll('.'+lan).style('visibility','visible');  
}
function makeHiddenLan(lan)  {  
    d3.selectAll('.'+lan).style('visibility','hidden');  
}


function contains(a, obj) {                             // Using a contains function from this StackOverflow post: http://stackoverflow.com/questions/237104/array-containsobj-in-javascript
    for (var i = 0; i < a.length; i++) {
        if (a[i] === obj) {
            return true; }
    }
    return false;
}

function updateMap() {                                  // Updates the map based on the current state - hours, mlanguages. 
    console.log('updating map...');
    newLan = getChecks();
    // console.log('incoming mlanguages:');
    console.log(newLan);
    newHours = genHours(setHours);
    console.log(newHours);
    // console.log('newHours',newHours);
    // console.log('newLan',newLan);
    // console.log('curHours',curHours);
    // console.log('curLan',curLan);
    for (var i = 0; i < curLan.length; i++) {
        // console.log('a',i);
        // console.log(curLan[i]);
        if (!contains(newLan,curLan[i])) {
            // console.log('hiding: '+curLan[i]);
            makeHiddenLan(curLan[i]);
        }
    }
    for (var i = 0; i < curHours.length; i++) {
        // console.log('b',i);
        if (!contains(newHours, curHours[i])) {
            for (var j = 0; j < newLan.length; j++) {
                // console.log('hiding: '+newLan[j]);
                if (contains(curLan, newLan[j])) {
                    makeHidden(newLan[j], curHours[i]);
                }
            }
        }
    }
    
    for (var i = 0; i < newLan.length; i++) {
        // console.log('c',i);
        if (!contains(curLan, newLan[i])) {
            // console.log('displaying: '+newLan[i]);
            for (var j = 0; j < newHours.length; j++) {
                makeVisible(newLan[i],newHours[j]);
            }
        }
    }
    
    for (var i = 0; i<newHours.length; i++) {
        // console.log('d',i);
        if (!contains(curHours, newHours[i])) {
            // console.log('displaying: '+curLan[j]);
            for (var j = 0; j < curLan.length; j++) {
                makeVisible(curLan[j],newHours[i]);
            }
        }
    }
    curHours = newHours;
    curLan = newLan;
}

function passArgs(times,lans) {
                             // passes new times ([start, end]) and mlanguages (['lan1,'lan2',...,'lanN']) arrays to the updateMap function.
    console.log("Passing args");
    console.log("Time:");
    console.log(times);
    console.log("Languages:");
    console.log(lans);
    checkLans(lans);
    setHours = times;
    console.log("About to update map!");
    updateMap();
}


function checkLans(lans) {                              // Checks the checkboxes for the mlanguages in lans
    
    for (var i=0; i<mlanguages.length; i++) {
        // console.log(mlanguages[i]);
        if (contains(lans,mlanguages[i])) {  var curCheck = document.getElementById(mlanguages[i]+'Toggle').checked=true;  }
        else {  document.getElementById(mlanguages[i]+'Toggle').checked=false;  }
    }
    // updateMap();
}   


function checkAll() {                                   // Called by the "Select All" checkbox. Toggles all mlanguages on or off, and then calls updateMap
    if ( document.getElementById('allToggle').checked ) {
        document.getElementById('allToggle').checked=true;
        checkLans(mlanguages);
    }
    else {
        document.getElementById('allToggle').checked=false;
        checkLans([]);
    }
    updateMap();
}


    
function testOn() {                                     // Tester functions, used to quickly determine if the map has rendered properly.
    d3.selectAll('.pt').style('visibility','visible');
}
function testOff() {
    d3.selectAll('.pt').style('visibility','hidden');
}

function getKeys(obj) {                                 // from this stack overflow post: http://stackoverflow.com/questions/126100/how-to-efficiently-count-the-number-of-keys-properties-of-an-object-in-javascrip
    var keys = [],
        k;
    for (k in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, k)) {
            keys.push(k);
        }
    }
    return keys;
}

function mapInit() {
    renderMap();
    colorArray();
    initialCache();
    // passArgs([0,12],['en','de','fr']);
}


function testDisplay() {
    passArgs([0,12],['en','de','fr']);
}




