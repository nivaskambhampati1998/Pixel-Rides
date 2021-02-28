var x = document.getElementById("coords");
var lat;
var lng;

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  x.innerHTML = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Latitude: " + position.coords.latitude + 
  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Longitude: " + position.coords.longitude;

  var uluru = {lat: position.coords.latitude, lng: position.coords.longitude};

  lat = position.coords.latitude;
  lng = position.coords.longitude;

  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 14, center: uluru});
  
  var marker = new google.maps.Marker({position: uluru, map: map});
}

getLocation();