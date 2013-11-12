/* global google, d3 */

$(function () {
  // Lat/long for Boston
  var center = new google.maps.LatLng(42.3581, -71.0636);
  var DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  var $map = $('#map');

  var map = new google.maps.Map($map[0], {
    zoom: 14,
    minZoom: 13,
    maxZoom: 17,
    disableDefaultUI: true,
    center: center,
    styles: [
      {
        'stylers': [
          {'saturation': -90},
          {'lightness': 10}
        ]
      }
    ]
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    radius: 15,
    opacity: 0.7,
    gradient: [
      'rgba(255, 210, 0, 0)',
      'rgba(255, 210, 0, 1)',
      'rgba(255, 180, 0, 1)',
      'rgba(245, 165, 0, 1)',
      'rgba(230, 100, 0, 1)'
    ],
    map: map
  });

  function changeDay(day) {
    var data = [];
    var sum = 0;
    d3.csv(DAYS[day] + '.csv', function (err, entries) {
      entries.forEach(function (entry) {
        entry.count = parseInt(entry.count, 10);
        data.push(entry);
        sum += entry.count;
      });

      var taxiData = new google.maps.MVCArray();
      heatmap.setData(taxiData);
      var entry;
      for (var i = 0; i < data.length; i++) {
        entry = data[i];
        var latlong = new google.maps.LatLng(entry.latitude, entry.longitude);
        taxiData.push({location: latlong, weight: entry.count });
      }
    });
  }

  changeDay(3);

  $('#weekday').on('change', function () {
    var day = parseInt($(this).val(), 10);
    changeDay(day);
  });

});
