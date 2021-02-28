var lat;
var lng;

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  }
}

function showPosition(position) {
  var uluru = {lat: position.coords.latitude, lng: position.coords.longitude};

  lat = position.coords.latitude;
  lng = position.coords.longitude;

  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 14, center: uluru});
  
  var marker = new google.maps.Marker({position: uluru, map: map});
}

getLocation();

