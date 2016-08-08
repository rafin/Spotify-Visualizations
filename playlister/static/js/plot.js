var audio;
var titles;
var songs;
var sorted_genres;
var means;
var title = "";
var unencoded_title = "";
var username;
$(document).ready(function() {
    $('#title a').attr("href", window.location.origin);
    $('#get_data_button').click(function() {
        username = $("#user-input").val();
        $(".loading").show()
        $.ajax({
            url: window.location.origin + '/getplaylists/?username='.concat(username) + '&token='.concat(token),
            success: function (jsontitles) {
                $(".loading").hide()
                $('.error').remove();
                $('.pl_option').remove();
                if (jsontitles == 'no user') {
                    $("main").append('<div class="error">username is blank</div>');
                } else {
                    if (jsontitles.length > 0) {
                        titles = jsontitles.map(function(t) {
                            return t['0']
                        });
                        loadtitles(titles);
                        $('#graph_bar').show("fast");
                    } else {
                        $("main").append('<div class="error">user has no public playlists</div>');
                    }
                }
            },
            error: function (response) {
                console.log(response)
                $(".loading").hide()
            }
        }).responseJSON;

    })

    $(document).on('click', '#go_button', function() {
        if ($("#playlist_select").val() != "Select Playlist" && $("#y_select").val() != "y-values" && $("#x_select").val() != "x-values") {
            if ($("#playlist_select").val() != unencoded_title) {
                createscatter();
            }
        }
    })

    $(document).on('click', '#stats_toggle', function() {
        if ($("#right_aside").css("width") == '0px') {
            $("main").css("right", '201px');
            $("#right_aside").animate({ width: '200px' })
        } else if ($("#right_aside").css("width") == '200px') {
            $("#right_aside").animate({ width: '0px' })
            $("main").css("right", '0px');
        }
        if ($("main svg").length > 0) {
            clean_canvas();
            scatter(songs);
        }
    })

    $(window).resize(function() {
        if ($("main svg").length > 0) {
            clearTimeout(resizeTimer);
            var resizeTimer = setTimeout(function() {
                //delete old svg and tooltip and plot new one
                clean_canvas();
                scatter(songs);
            }, 250);
        }
    });

    function createscatter() {
        unencoded_title = $("#playlist_select").val();
        title = encodeURIComponent(unencoded_title);
        $(".loading").show()
        $.ajax({
            url: window.location.origin + '/getsongs/?title='.concat(title) + '&username='.concat(username),
            success: function(data) {
                $(".loading").hide()
                songs = data.songs;
                sorted_genres = data.sorted_genres;
                means = data.means;
                clean_canvas();
                scatter(songs);
            },
            error: function (response) {
                console.log(response)
                $(".loading").hide()
            }
        }).responseJSON
    }

    //lists all playlists into the 'pick playlist' selection box
    function loadtitles(titles) {
        for (var i = 0; i < titles.length; i++) {
            $("#playlist_select").append('<option class="pl_option">' + titles[i] + '</option>');
        }
    }


    function clean_canvas() {
        audio = document.getElementById('preview_song');
        audio.setAttribute('src', "")
        audio.pause();
        $(".genre_row").remove();
        $(".mean_row").remove();
        $("svg").remove();
        $(".tooltip").remove();
        $(".details").remove();
    }



    //---------------------------------------------------------------------------------------
    // Scatter Plot
    //---------------------------------------------------------------------------------------
    function scatter(playlist) {
        var x = $("#x_select").val().toLowerCase();
        var y = $("#y_select").val().toLowerCase();
        var dmax = d3.max(playlist, function(d) {
            return d['duration'] });
        var dmin = d3.min(playlist, function(d) {
            return d['duration'] });
        var omax = d3.max(playlist, function(d) {
            return d['order'] });
        var domains = {
            'order': [0, omax],
            'sort': [0, omax],
            'danceability': [-4, 100],
            'energy': [-4, 100],
            'loudness': [-50, 0],
            'speechiness': [-4, 100],
            'acousticness': [-4, 100],
            'instrumentalness': [-4, 100],
            'valence': [-4, 100],
            'tempo': [40, 220],
            'duration': [dmin - 15, dmax], //must get from input
            'popularity': [-4, 100],
            'release_date': [1900, 2020]
        }

        //generate data for sort option
        if (x == "sort") {
            playlist = playlist.sort(function(a, b) {
                return a[y] - b[y]; });
            for (var i = 0; i < playlist.length; i++) {
                playlist[i]['sort'] = i + 1;
            };
            playlist = playlist.sort(function(a, b) {
                return a['order'] - b['order']; });
        }

        // -- 'Global' Vars --
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

        //create SVG element
        var svg = d3.select("main")
            .append("svg")
            .attr("width", w - 20)
            .attr("height", h - 20)
            .style("opacity", 0);


        //ceate tooltip
        var tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        //draw dots
        svg.selectAll("circle")
            .data(playlist)
            .enter()
            .append("circle")
            .attr("cx", function(d) {
                return xscale(d[x]);
            })
            .attr("cy", function(d) {
                return yscale(d[y]);
            })
            .attr("r", 4)
            .attr("fill", function(d) {
                if (d["preview_url"] == "") {
                    return "#A4ADC9";
                } else {
                    return "#495780";
                }
            })
            .on("mouseover", function(d) {
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9)

                if (d3.event.pageX > w - 125) {
                    tooltip.html('<div class="tooltip"><b>' + d["name"] +
                            " : " + d["artist"] + "</div>")
                        .style("left", (d3.event.pageX - 150) + "px")
                        .style("top", (d3.event.pageY - 28) + "px");
                } else {
                    tooltip.html('<div class="tooltip"><b>' + d["name"] +
                            " : " + d["artist"] + "</div>")
                        .style("left", (d3.event.pageX) + "px")
                        .style("top", (d3.event.pageY - 28) + "px");
                }
                d3.select(this)
                    .style("r", 5)
                    .style("fill", "#8DF531")
            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(400)
                    .style("opacity", 0);
                d3.select(this)
                    .style("r", 4)
                    .style("fill", function(d) {
                        if (d["preview_url"] == "") {
                            return "#A4ADC9";
                        } else {
                            return "#495780";
                        }
                    });
            })
            .on("click", function(d) {
                audio = document.getElementById('preview_song');
                audio.pause();
                // details.transition()
                //     .duration(200)
                //     .style("opacity", 1);
                // details.html('<table><b>' +
                //     '<tr><th colspan="2">' + d['name'] + ': ' + d['artist'] + '</th></b></tr>' +
                //     '<tr><td>' + $("#x_select").val() + '</td><td>' + d[x] + '</td></tr>' +
                //     '<tr><td>' + $("#y_select").val() + '</td><td>' + d[y] + '</td></tr>' +
                //     '<table>');
                if (d["preview_url"] != "") {
                    if (audio.getAttribute('src') == d["preview_url"]) {
                        d3.select(this).attr("stroke", "none")
                        audio.setAttribute('src', "")
                    } else {
                        d3.selectAll("circle")
                            .attr("stroke", "none")
                        d3.select(this)
                            .attr("stroke", "#8DF531")
                            .attr("stroke-width", 3);
                        audio.setAttribute('src', d["preview_url"]);
                        audio.play();
                    }
                }
            });

        //create xaxis
        var xaxis = d3.svg.axis().scale(xscale).orient("bottom").ticks(10)
            .tickFormat(d3.format("d"));
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + (h - padding) + ")")
            .call(xaxis);
        svg.append("text")
            .attr("class", "x label")
            .attr("x", w - 40)
            .attr("y", h - 45)
            .style("text-anchor", "end")
            .text(x);

        //create yaxis
        var yaxis = d3.svg.axis().scale(yscale).orient("left").ticks(10)
            .tickFormat(d3.format("d"));
        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + padding + ",0)")
            .call(yaxis);
        svg.append("text")
            .attr("class", "y label")
            .attr("transform", "rotate(-90)")
            .attr("x", -40)
            .attr("y", 43)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text(y);

        //fade in plot
        svg.transition()
            .duration(400)
            .style("opacity", 1);

        d3.select("#go_button").on("click", function() {
            x = $("#x_select").val().toLowerCase();
            y = $("#y_select").val().toLowerCase();

            if ($("#playlist_select").val() == unencoded_title){
                if (x == "sort") {
                    playlist = playlist.sort(function(a, b) {
                        return a[y] - b[y]; });
                    for (var i = 0; i < playlist.length; i++) {
                        playlist[i]['sort'] = i + 1;
                    };
                    playlist = playlist.sort(function(a, b) {
                        return a['order'] - b['order']; });
                }


                xscale.domain(domains[x]);
                yscale.domain(domains[y]);

                svg.selectAll("circle")
                    .data(playlist)
                    .transition()
                    .duration(500)
                    .attr("cx", function(d) {
                        return xscale(d[x]);
                    })
                    .attr("cy", function(d) {;
                        return yscale(d[y]);
                    });

                // Update X Axis
                svg.select(".x.axis")
                    .transition()
                    .duration(500)
                    .call(xaxis);

                // Update Y Axis
                svg.select(".y.axis")
                    .transition()
                    .duration(500)
                    .call(yaxis);

                svg.select(".x.label")
                    .text(x)

                svg.select(".y.label")
                    .text(y)
            }

        });

        //create means bar
        console.log(means);
        var mtable = d3.select('#means table');

        var mtr = mtable.selectAll('tr')
            .data(means)
            .enter()
            .append('tr')
            .attr("class", "mean_row")

        var mtd = mtr.selectAll("td")
            .data(function(d) {
                return d3.values(d)
            })
            .enter()
            .append("td")
            .text(function(d) {
                return d
            });

        //create genres bar
        console.log(sorted_genres);
        var gtable = d3.select('#genres table');

        var gtr = gtable.selectAll('tr')
            .data(sorted_genres)
            .enter()
            .append('tr')
            .attr("class", "genre_row");

        var gtd = gtr.selectAll("td")
            .data(function(d) {
                return d3.values(d)
            })
            .enter()
            .append("td")
            .text(function(d) {
                return d
            });
        gtr.on("mouseover", function(d) {
                var row = d3.select(this).selectAll('td')
                    .style("font-weight", "bold")
                    .style("color", "#4DC2A3");
                svg.selectAll("circle")
                    .transition()
                    .duration(400)
                    .attr("fill", function(d) {
                        if (d["genre"].indexOf(row.text()) > -1) {
                            return "#FF5C46";
                        } else {
                            if (d["preview_url"] == "") {
                                return "#A4ADC9";
                            } else {
                                return "#495780";
                            }
                        }
                    })
                    .attr("r", function(d) {
                        if (d["genre"].indexOf(row.text()) > -1) {
                            return 6;
                        } else {
                            return 4;
                        }
                    });
            })
            .on("mouseout", function(d) {
                d3.select(this).selectAll('td')
                    .style("font-weight", "normal")
                    .style("color", "#041A0D");
                svg.selectAll("circle")
                    .transition()
                    .duration(400)
                    .attr("r", 4)
                    .attr("fill", function(d) {
                        if (d["preview_url"] == "") {
                            return "#A4ADC9";
                        } else {
                            return "#495780";
                        }
                    })
            })
            .on("click", function(d) {
                var row = d3.select(this).selectAll('td').text();
                //TODO
            });

    }

    //---------------------------------------------------------------------------------------
    function updateWindow() {
        var w = $('main').width();
        var h = $('main').height();
        console.log([w,h])
        return [w, h];
    }


});