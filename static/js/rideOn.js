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

  var begin = "https://www.google.com/maps/dir/?api=1&origin=";
  var mid = "&destination=";
  var end = "&travelmode=driving&dir_action=navigate";

  var destLat = ''
  var destLng = ''

  console.log(lat);

  var url = begin + lat + "," + lng + mid + destLat + "," + destLng + end;

  console.log(url);
  var x = document.getElementById("gmaps");
  x.innerHTML = "<a href=\"" + url + "\">Go to google maps</a>";

  // https://stackoverflow.com/questions/3896871/google-map-driving-direction-source-code-for-their-example

}

getLocation();