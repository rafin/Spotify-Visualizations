var titles;
var songs;
var title = "";
var unencoded_title = "";
var username;
var refined_songs;

$(document).ready(function() {
    $('#title a').attr("href", window.location.origin);

    $('.slider').slider({
        range: true,
        min: 0,
        max: 100,
        values: [0,100]
    })
    $('#loudness').slider({
        range: true,
        min: -60,
        max: 0,
        values: [-60,0]
    })

    //

    $('#get-data-button').click(function() {
        username = $("#user-input").val();
        $(".loading").show()
        $.ajax({
            url: window.location.origin + '/getplaylists/?username='.concat(username) + '&token='.concat(token),
            success: function (jsontitles) {
                $(".loading").hide()
                $('.error').remove();
                $('.pl_option').remove();
                // $('.pl_option').remove();
                if (jsontitles == 'no user') {
                    $("main").append('<div class="error">username is blank</div>');
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
                $(".loading").hide()
            }
        }).responseJSON;
    });


    $('#gen-button').click(function() {
        if ($("#playlist_select").val() != "Select Playlist") {
            if ($("#playlist_select").val() != unencoded_title) {
                retrieve_songs();
            } else {
                generate_playlist();
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
        $(".loading").show()
        $.ajax({
            url: window.location.origin + '/newplaylist/?name='.concat(new_name) + '&songs='.concat(ids),
            success: function (response) {
                console.log(response)
                $(".loading").hide()
            },
            error: function (response) {
                console.log(response)
                $(".loading").hide()
            }
        }).responseJSON;
    })


    function loadtitles(titles) {
        for (var i = 0; i < titles.length; i++) {
            $("#playlist_select").append('<option class="pl_option">' + titles[i] + '</option>');
        }
    }


    function retrieve_songs(){
        unencoded_title = $("#playlist_select").val();
        title = encodeURIComponent(unencoded_title);
        $(".loading").show()
        $.ajax({
            url: window.location.origin + '/getsongslite/?title='.concat(title) + '&username='.concat(username),
            success: function(data) {
                $(".loading").hide()
                songs = data.songs;
                generate_playlist()
            },
            error: function (response) {
                console.log(response)
                $(".loading").hide()
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

        $("#results-group").show("fast");
        $("#save-group").show("fast");
        refined_songs = feature_sort(refined_songs)
        show_results(refined_songs);

        function between(x, range) {
            return x >= range[0] && x <= range[1]
        }

    }

    function get_ranges() {
        ranges = {'danceability':[0,0],'energy':[0,0], 'loudness':[0,0], 'speechiness':[0,0],
                  'acousticness':[0,0],'instrumentalness':[0,0],'valence':[0,0], 'popularity':[0,0]}
        ranges.danceability = $('#danceability').slider('values')
        ranges.energy= $('#energy').slider('values')
        ranges.loudness= $('#loudness').slider('values')
        ranges.speechiness= $('#speechiness').slider('values')
        ranges.acousticness= $('#acousticness').slider('values')
        ranges.instrumentalness= $('#instrumentalness').slider('values')
        ranges.valence= $('#valence').slider('values')
        ranges.popularity= $('#popularity').slider('values')
        return ranges
    }

    function feature_sort(songs) {
        feature = $('#feature_select').val().toLowerCase()
        direction = $('#direction_select').val()
        songs = songs.sort(function(a, b){
            return a[feature] > b[feature]
        });
        if(direction == "Descending"){
            songs = songs.reverse();
            console.log("Descending")
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
});


















