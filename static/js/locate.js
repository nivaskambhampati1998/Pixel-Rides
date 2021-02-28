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
  x.innerHTML = "Lat: " + Number((position.coords.latitude).toFixed(6)) + ", Lng: " + Number((position.coords.longitude).toFixed(6));

}

getLocation();