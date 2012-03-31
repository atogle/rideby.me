var RideByMe = RideByMe || {};

(function(R) {
  // The view for the app, of course
  R.AppView = Backbone.View.extend({
    el: '#map',

    radius: 800,
    center: new L.LatLng(39.952335, -75.163789),

    initialize: function() {
      var self = this,
          cloudmadeUrl = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png',
          cloudmadeAttribution = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
          cloudmade = new L.TileLayer(cloudmadeUrl, {maxZoom: 18, attribution: cloudmadeAttribution});

      // Init the model to fetch routes and stations
      self.model = new R.TransitModel();

      // Render thyself when the transit data show up
      self.model.bind('change', self.render, self);

      // Init the map
      self.map = new L.Map('map');

      // Init all of the overlays
      self.stopLayer = new L.GeoJSON();
      self.routeLayer = new L.GeoJSON();
      self.walkshedLayer = new L.Circle(self.center, self.radius, {
        color: '#000',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.2
      });

      // Add all of the layers to the map in the appropriate z-order
      self.map.addLayer(cloudmade);
      self.map.addLayer(self.stopLayer);
      self.map.addLayer(self.routeLayer);
      self.map.addLayer(self.walkshedLayer);

      // Setup the route layer when the geojson gets parsed
      self.routeLayer.on("featureparse", function (e) {
        e.layer.bindPopup('<p>'+e.properties.short_name+': '+e.properties.long_name+'</p>');
      });

      // Do a model fetch when geolocation finishes
      self.map.on('locationfound', function(e){
        // self.model.fetch({ data: {lon:e.latlng.lng, lat:e.latlng.lat, radius:self.radius} });
        self.model.fetch({ data: {lon:-75.1591, lat:39.9376, radius:self.radius} });
      });
      // Do a model fetch for city hall if geolocation fails
      self.map.on('locationerror', function(e){
        self.model.fetch({ data: {lon:self.center.lng, lat:self.center.lat, radius:self.radius} });
        alert(e.message);
      });

      self.map.locate();
    },

    render: function() {
      var self = this,
          walkshed = self.model.get('walkshed'),
          latLng = new L.LatLng(walkshed.lat, walkshed.lon);

      // Update walkshed
      self.walkshedLayer.setLatLng(latLng);

      // Update stops
      self.stopLayer
        .clearLayers()
        .addGeoJSON(self.model.get('stops'));
      // Update routes
      self.routeLayer
        .clearLayers()
        .addGeoJSON(self.model.get('routes'));

      // Zoom to the point
      self.map.setView(latLng, 15);
    }
  });
})(RideByMe);

$(document).ready(function() {
  RideByMe.app = new RideByMe.AppView();
});