var RideByMe = RideByMe || {};

(function(R) {


  // The view for the app, of course
  R.AppView = Backbone.View.extend({
    el: '#map',

    initialize: function() {
      var self = this,
          cloudmadeUrl = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png',
          cloudmadeAttribution = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
          cloudmade = new L.TileLayer(cloudmadeUrl, {maxZoom: 18, attribution: cloudmadeAttribution});

      // Init the model
      self.model = new R.TransitModel();

      // Render thyself when the transit data show up
      self.model.bind('change', self.render, self);

      self.map = new L.Map('map');
      self.stops = new L.GeoJSON();
      self.routes = new L.GeoJSON();

      self.map.addLayer(cloudmade);
      self.map.addLayer(self.stops);
      self.map.addLayer(self.routes);

      self.map.on('locationfound', onLocationFound);
      self.map.on('locationerror', onLocationError);

      self.map.locate();

      function onLocationFound(e) {
        // Fetch the first batch of surveys
        // self.model.fetch({ data: {lon:e.latlng.lng, lat:e.latlng.lat, radius:800} });

        self.model.fetch({ data: {lon:-75.1591, lat:39.9376, radius:800} });
      }

      function onLocationError(e) {
        alert(e.message);
      }
    },

    render: function() {
      var self = this,
          center = self.model.get('center'),
          latLng = new L.LatLng(center.lat, center.lon),
          circle = new L.Circle(latLng, center.radius);

      // self.stops.addGeoJSON(self.model.get('stops'));
      self.routes.addGeoJSON(self.model.get('routes'));

      self.map.setView(latLng, 15);
      self.map.addLayer(circle);
    }
  });
})(RideByMe);

$(document).ready(function() {
  RideByMe.app = new RideByMe.AppView();
});