var titles;
var songs;
var title = "";
var unencoded_title = "";
var username;
var refined_songs;
var playlists = [];
var curr_playlists = [];
var confidence_intervals;

$(document).ready(function() {
    $('#title a').attr("href", window.location.origin);
    

    //initialize sliders
    $('.slider').slider({
        range: true,
        min: 0,
        max: 100,
        values: [0,100],
        animate: "fast"
    })
    $('#loudness').slider({
        min: -60,
        max: 0,
        values: [-60,0]
    })
    $('#release_date').slider({
        min: 1900,
        max: 2016,
        values: [1900,2016],
    })
    var sliders = ["danceability", "energy", "loudness", "speechiness", "acousticness",
                    "instrumentalness", "valence", "popularity", "release_date"]
    for (var i = 0; i < sliders.length; i++) {
        $("#" + sliders[i]).slider({
            slide: function(event, ui) {
                $("#" + event.target.id + "_val").html(ui.values[0] + " to " + ui.values[1]);
            }
        })
    }
    //end of slide initialization


    $('#get-data-button').click(function() {
        username = $("#user-input").val();
        $("#get-data-button").text('Loading...')
        $.ajax({
            url: window.location.origin + '/getplaylists/?username='.concat(username) + '&token='.concat(token),
            success: function (jsontitles) {
                $("#get-data-button").text('Retrieve Playlists')
                $('.error').remove();
                $('.pl_option').remove();
                // $('.pl_option').remove();
                if (jsontitles == 'no user') {
                    $("#user-group").append('<div class="error">username is blank</div>');
                } else {
                    if (jsontitles.length > 0) {
                        titles = jsontitles.map(function(t){ return t[0] });
                        loadtitles(titles);
                        $("#playlist-group").show("fast");
                        $("#filter-group").show("fast");
                        $("#sort-group").show("fast");
                    } else {
                        $("main").append('<div class="error">user has no public playlists</div>');
                    }
                }
            },
            error: function (response) {
                console.log(response)
                $("#get-data-button").text('Retrieve Playlists')
            }
        }).responseJSON;

    });


    $('#add-button').click(function() {
        var t = $("#playlist_select").val();
        if (t != null) {
            if (playlists.indexOf(t) == -1){
                $("#playlist-table").append("<tr><td class='pl-title' colspan='2'>" + 
                    $("#playlist_select").val() +
                    "</td><td class='remove-button'>-</td></tr>")
                playlists.push(t)
            }
        }
    })

    $('#playlist-table').on("click", ".remove-button", function() {
        $(this).parent().remove();
        var index = playlists.indexOf($(this).prev('td').text())
        playlists.splice(index, 1);
    })


    $('#gen-button').click(function() {
        if (playlists != []) {
            console.log(playlists)
            console.log(curr_playlists)
            console.log(arraysIdentical(playlists, curr_playlists))
            if (arraysIdentical(playlists, curr_playlists)) {
                generate_playlist();
            } else {
                retrieve_songs();
            }
        }
    });


    $("#save-button").click(function() {
        if ($("#save-input").val() == "") {
            new_name = "new playlist"
        } else {
            new_name = $("#save-input").val()
        }
        ids = refined_songs.map(function(s){ return s['id'] });
        // pass new_name and refined_songs into an ajax request
        // which will create the new playlist
        $("#save-button").text('Loading...')
        $.ajax({
            url: window.location.origin + '/newplaylist/?name='.concat(new_name) + '&songs='.concat(ids),
            success: function (response) {
                console.log(response)
                $(".error").remove()
                $("#save-button").text('Save Playlist')
            },
            error: function (response) {
                console.log(response)
                $("#save-group").append('<div class="error">new playlist has too many songs for plotify to handle, sorry for inconvenience</div>');
                $("#save-button").text('Save Playlist')
            }
        }).responseJSON;
    })


    //------Presets------//
    $("#exercise-button").click(function() {
        //var setvalues = [[38,100],[52,100],[-12,0],[0,48],[0,100],[0,100],[8,100],[0,100],[1900,2016]];
        preset(confidence_intervals);
    })

    $("#relaxing-button").click(function() {
        var setvalues = [[0,82],[0,42],[-60,-9],[0,15],[0,100],[0,100],[0,71],[0,100],[1900,2016]];
        preset(setvalues);
    })

    $("#acoustic-button").click(function() {
        var setvalues = [[0,77],[0,47],[-60,-5],[0,26],[58,100],[0,100],[0,71],[0,100],[1900,2016]];
        preset(setvalues);     
    })

    function preset(setvalues){
        var sliders = ["danceability", "energy", "loudness", "speechiness", "acousticness",
                    "instrumentalness", "valence", "popularity", "release_date"]
        for (var i = 0; i < sliders.length; i++) {
            $("#" + sliders[i]).slider( "values", setvalues[i])
            $("#" + sliders[i] + "_val").html(setvalues[i][0] + " to " + setvalues[i][1]);
        }
    } 
    //-------------------//


    function loadtitles(titles) {
        for (var i = 0; i < titles.length; i++) {
            $("#playlist_select").append('<option class="pl_option">' + titles[i] + '</option>');
        }
    }


    function retrieve_songs(){
        curr_playlists = playlists.slice();
        //encode playlist titles to be passed through url
        encoded_playlists = []
        for (var i = 0; i < playlists.length; i++){
            encoded_playlists.push(encodeURIComponent(playlists[i]));
        }
        $("#gen-button").text('Loading...')
        $.ajax({
            url: window.location.origin + '/getsongs/?title='.concat(encoded_playlists) + '&username='.concat(username) + '&token='.concat(token),
            success: function(data) {
                $("#gen-button").text('Generate New Playlist');
                songs = data.songs;
                if (songs == undefined) {
                    $("#playlist-group").append('<div class="error">Playlist not Specified</div>');
                } else {
                    confidence_intervals = data.intervals;
                    console.log(confidence_intervals);
                    $(".error").remove();
                    generate_playlist();
                }
            },
            error: function (response) {
                console.log(response)
                $("#gen-button").text('Generate New Playlist')
            }
        }).responseJSON
    }


    function generate_playlist() {
        ranges = get_ranges();
            //format: {"danceability": [min, max], ...}
        $('#song-list tr').remove()
        refined_songs = []
        //build refined_songs
        for (var i = 0; i < songs.length; i++) {
            for (var key in ranges) {
                add = true;
                boo = between(songs[i][key], ranges[key])
                if(!boo) {
                    add = false;
                    break;
                }
            }
            if(add) {
                refined_songs.push(songs[i])
            }
        }
        if($('#feature_select').val() == null) {
            $("#sort-group").append('<div class="error">Sort Feature not Specified</div>');
        } else {
            $(".error").remove()
            $("#results-group").show("fast");
            $("#save-group").show("fast");
            refined_songs = feature_sort(refined_songs)
            show_results(refined_songs);
        }

        function between(x, range) {
            return x >= range[0] && x <= range[1]
        }

    }

    function get_ranges() {
        ranges = {'danceability':[0,0],'energy':[0,0], 'loudness':[0,0], 'speechiness':[0,0],
                  'acousticness':[0,0],'instrumentalness':[0,0],'valence':[0,0], 'popularity':[0,0], 'release_date':[0,0]}
        ranges.danceability = $('#danceability').slider('values')
        ranges.energy= $('#energy').slider('values')
        ranges.loudness= $('#loudness').slider('values')
        ranges.speechiness= $('#speechiness').slider('values')
        ranges.acousticness= $('#acousticness').slider('values')
        ranges.instrumentalness= $('#instrumentalness').slider('values')
        ranges.valence= $('#valence').slider('values')
        ranges.popularity= $('#popularity').slider('values')
        ranges.release_date = $('#release_date').slider('values')
        return ranges
    }

    function feature_sort(songs) {
        feature = $('#feature_select').val().toLowerCase()
        direction = $('#direction_select').val()
        songs = songs.sort(function(a, b){
            return a[feature] > b[feature];
        });
        if(direction == "Descending"){
            songs = songs.reverse();
        }
        return songs;
    }

    function show_results(songs) {
        time = 0
        for(var i = 0; i < songs.length; i++) {
            $('#song-list').append('<tr><td>' +
                songs[i].name + '</td><td>' + songs[i].artist + '</td></tr>')
            time += songs[i].duration
        }
        $('#count-display').text(songs.length)
        time = Math.round(time / 60)
        hours = Math.floor(time / 60)
        time = time - (hours * 60)
        mins = time % 60
        if (hours) {
            $('#length-display').text(hours + " hrs " + mins + " mins")
        } else {
            $('#length-display').text(mins + " minutes")
        }

    }

    function arraysIdentical(a, b) {
        var i = a.length;
        if (i != b.length) return false;
        while (i--) {
            if (a[i] !== b[i]) return false;
        }
        return true;
    };

});


















