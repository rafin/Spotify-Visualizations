var audio
$(document).ready(function() {

    loadtitles();

    $( "#go_button" ).click(function() {
        create();
    })    

    $( window ).resize(function() {
        clearTimeout(resizeTimer);
        var resizeTimer = setTimeout(function(){
            create();
        }, 250);
    });

    function create() {
        var title = $( "#playlist_select").val();
        var x = $( "#x_select").val().toLowerCase();
        var y = $( "#y_select").val().toLowerCase();
        //delete old svg and tooltip and plot new one
        console.log(title)
        console.log(x)
        console.log(y)
        if(title != "Select Playlist" && x != "select x-values" && y != "select y-values"){
            var data = getdata(title);
            $("svg").remove();
            $(".tooltip").remove();
            $(".details").remove();
            plot(data, x, y);
        }
    }


    //lists all playlists into the 'pick playlist' selection box
    function loadtitles(){
        console.log("at loadtitles")
        var titles = $.ajax({async:false,
            url:'http://localhost:8000/getplaylists',
        }).responseJSON;
        titles = titles.map(function(t) {return t['fields']['title']});
        for (var i = 0; i < titles.length; i++){
            $("#ps select").append('<option>'+titles[i] + '</option>');
        }
        $("#ps").css("")
    }

    //given a playlist title, return the playlist model as a json derived object
    function getdata(title){
        console.log("at getdata")
        var data = $.ajax({async:false,
            url:'http://localhost:8000/getsongs/?title='.concat(title),
        }).responseJSON;

        //convert release dates from strings to integer year
        data = data.map(function(d){ 
            d['fields']['release_date'] = parseInt(d['fields']['release_date'].substring(0,4));
            return d;
        })

        return data;
    }

    //given json derived object playlist, plot the data on the page
    function plot(playlist, x, y){
        var dmin = 9999;
        var dmax = 0;

        console.log(playlist);
        if(x == 'duration' || y == 'duration'){
            dmax = d3.max(playlist, function(d) {return d['fields']['duration']});              
            dmin = d3.min(playlist, function(d) {return d['fields']['duration']});
        }
        console.log("dmin = " + dmin + "  dmax = " + dmax);
        var domains = {
            'danceability': [-4, 100],
            'energy': [-4, 100],
            'key': [-0.5,11], //not sure
            'loudness': [-50, 0],
            'mode': [-0.05, 1],
            'speechiness': [-4, 100],
            'acousticness': [-4, 100],
            'instrumentalness': [-4, 100],
            'valence': [-4, 100],
            'tempo': [40, 220], //must get from input
            'duration': [dmin - 15,dmax], //must get from input
            'popularity' : [-4, 100],
            'release_date' : [1900, 2020]
        }
        // -- 'Global' Vars -- //
        var dimens = updateWindow();
        var w = dimens[0];
        var h = dimens[1];
        var padding = 40;

        var xscale = d3.scale.linear()
            .domain(domains[x])
            .range([padding, w - padding]);

        var yscale = d3.scale.linear()
            .domain(domains[y])
            .range([h - padding, padding]);
        var xaxis = d3.svg.axis().scale(xscale).orient("bottom");

        // -- Creating a Single Graph -- //
        //create SVG element
        var svg = d3.select("#main")
            .append("svg")
            .attr("width", w)
            .attr("height", h);

        //create tooltip
        var tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        var details = d3.select("#right_bar").append("div")
            .attr("class", "details")
            .style("opacity", 0);

        //draw dots
        svg.selectAll("circle")
            .data(playlist)
            .enter()
            .append("circle")
            .attr("cx", function(d) {
                return xscale(d["fields"][x]);
            })
            .attr("cy", function(d) {
                return yscale(d["fields"][y]);
            })
            .attr("r", 4)
            .attr("fill", "#40BB65")
            .on("mouseover", function(d) {
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9)

                if(d3.event.pageX > w - 50){
                    tooltip.html('<div class="tooltip"><b>' + d["fields"]["title"] + 
                            " : " + d["fields"]["artist"] + "</div>")
                        .style("left", (d3.event.pageX - 150) + "px")     
                        .style("top", (d3.event.pageY - 28) + "px");   
                } else{
                    tooltip.html('<div class="tooltip"><b>' + d["fields"]["title"] + 
                            " : " + d["fields"]["artist"] + "</div>")
                        .style("left", (d3.event.pageX) + "px")     
                        .style("top", (d3.event.pageY - 28) + "px");   
                }

                d3.select(this)
                    .attr("r", 5)
                    .attr("fill", "#57FF8E")
            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(400)
                    .style("opacity", 0);
                d3.select(this)
                    .attr("r", 4)
                    .attr("fill", "#40BB65");
                var audio = document.getElementById('preview_song');
                audio.pause();
            })
            .on("click", function(d) {
                tooltip.transition()
                    .duration(400)
                    .style("opacity", 0);
                details.transition()
                    .duration(200)
                    .style("opacity", 1);
                details.html('<table><b>' +
                    '<tr><th colspan="2">' + d['fields']['title'] + ': ' + d['fields']['artist'] + '</th></b></tr>' + 
                    '<tr><td>' + 'Danceability' + '</td><td>' + d['fields']['danceability'] + '</td></tr>' +
                    '<tr><td>' + 'Energy' + '</td><td>' + d['fields']['danceability'] + '</td></tr>' +
                    '<tr><td>' + 'Loudness' + '</td><td>' + d['fields']['loudness'] + '</td></tr>' +
                    '<tr><td>' + 'Mode' + '</td><td>' + d['fields']['mode'] + '</td></tr>' +
                    '<tr><td>' + 'Speechiness' + '</td><td>' + d['fields']['speechiness'] + '</td></tr>' +
                    '<tr><td>' + 'Acousticness' + '</td><td>' + d['fields']['acousticness'] + '</td></tr>' +
                    '<tr><td>' + 'Instrumentalness' + '</td><td>' + d['fields']['instrumentalness'] + '</td></tr>' +
                    '<tr><td>' + 'Valence' + '</td><td>' + d['fields']['valence'] + '</td></tr>' +
                    '<tr><td>' + 'Tempo' + '</td><td>' + d['fields']['tempo'] + '</td></tr>' +
                    '<tr><td>' + 'Key' + '</td><td>' + d['fields']['key'] + '</td></tr>' +
                    '<tr><td>' + 'Popularity' + '</td><td>' + d['fields']['popularity'] + '</td></tr>' +
                    '<tr><td>' + 'Release Date' + '</td><td>' + d['fields']['release_date'] + '</td></tr></table>');
                var audio = document.getElementById('preview_song');
                if(d["fields"]["preview_url"] != ""){
                    audio.setAttribute('src', d["fields"]["preview_url"])
                    audio.play();
                }
            });

        //create xaxis
        var xaxis = d3.svg.axis().scale(xscale).orient("bottom").ticks(10)
            .tickFormat(d3.format("d"));
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(0," + (h - padding) + ")")
            .call(xaxis);
        svg.append("text")
            .attr("class", "label")
            .attr("x", w - 40)
            .attr("y", h - 45)
            .style("text-anchor", "end")
            .text(x);

        //create yaxis
        var yaxis = d3.svg.axis().scale(yscale).orient("left").ticks(10)
            .tickFormat(d3.format("d"));
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + padding + ",0)")
            .call(yaxis);
        svg.append("text")
            .attr("class", "label")
            .attr("transform", "rotate(-90)")
            .attr("x", -40)
            .attr("y", 43)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text(y);


        function updateWindow(){
            var w = $('#main').width();
            var h = $('#main').height();
            return [w,h];
        }


    }

});
