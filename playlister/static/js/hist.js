$(document).ready(function() {
    //var playlist = "{{ playlist }}"; from template

    var domains = {
        'danceability': [0, 1],
        'energy': [0, 1],
        'key': [0, 11], //not sure
        'loudness': [-60, 0],
        'mode': [0, 1],
        'speechiness': [0, 1],
        'acousticness': [0, 1],
        'instrumentalness': [0, 1],
        'valence': [0, 1],
        'tempo': [0, 220],
        'duration': 'unknown'
    }
    var features = ['danceability', 'energy', 'key', 'loudness',
            'mode', 'speechiness', 'acousticness',
            'instrumentalness', 'valence', 'tempo'
        ]
    // -- 'Global' Variables -- //
    var feature;
    var width = 500,
        height = 500,
        padding = 50;

    //for (var i = 0; i < features.length; i++) {
        // -- Create a single Histogram -- //
        feature = 'tempo';
        var map = playlist.map(function(i) {
            return i['fields'][feature]; })

        var histogram = d3.layout.histogram()
            .bins(12)
            (map);

        var yscale = d3.scale.linear()
            .domain([0, d3.max(histogram.map(function(i) {
                return i.length }))])
            .range([0, height - 20]); //20 accounts for title width

        var xscale = d3.scale.linear()
            .domain(domains[feature])
            .range([0, width]);

        var xaxis = d3.svg.axis()
            .scale(xscale)
            .orient("bottom");

        var canvas = d3.select("body").append("svg")
            .attr("width", width + padding)
            .attr("height", height + 2 * padding)
            .append("g")
            .attr("transform", "translate(20,0)")

        var group = canvas.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(xaxis);

        var bars = canvas.selectAll(".bar")
            .data(histogram)
            .enter()
            .append("g");

        bars.append("rect")
            .attr("x", function(d) {
                return xscale(d.x); })
            .attr("y", function(d) {
                return 500 - yscale(d.y); })
            .attr("width", function(d) {
                return xscale(d.dx); })
            .attr("height", function(d) {
                return yscale(d.y); })
            .attr("fill", "salmon")

        //creates value labels on bar chart
        // bars.append("text")
        //     .attr("x", function(d) {
        //         return xscale(d.x); })
        //     .attr("y", function(d) {
        //         return 500 - yscale(d.y); })
        //     .attr("dy", "20px")
        //     .attr("dx", function(d) {
        //         return xscale(d.dx) / 2 })
        //     .attr("fill", '#fff')
        //     .attr("text-anchor", "middle")
        //     .text(function(d) {
        //         return d.y })
        //     .attr("font-family", "Tahoma")

        //create title
        bars.append("text")
            .text(feature)
            .attr("x", (width / 2))
            .attr("y", 12)
            .attr("text-anchor", "middle")
            .attr("font-family", "Tahoma")
    //}

});
