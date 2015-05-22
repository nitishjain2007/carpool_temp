function initialize1(){
	var defaultBounds = new google.maps.LatLngBounds(
		new google.maps.LatLng(28.459496500000000000, 77.026638300000060000)
		);
	var input1 = document.getElementById('start');
	var options = {
		bounds: defaultBounds,
		componentRestrictions: {country: 'in'}
	};
	var autocomplete1 = new google.maps.places.Autocomplete(input1, options);
	google.maps.event.addListener(autocomplete1, 'place_changed', function () {
	            var place = autocomplete1.getPlace();
	            document.getElementById('startlat').value = place.geometry.location.lat();
	            document.getElementById('startlong').value = place.geometry.location.lng();
	            makeroutecheck();
	        });
}
google.maps.event.addDomListener(window, 'load', initialize1);
function initialize2(){
	var defaultBounds = new google.maps.LatLngBounds(
		new google.maps.LatLng(28.459496500000000000, 77.026638300000060000)
		);
	var input2 = document.getElementById('end');
	var options = {
		bounds: defaultBounds,
		componentRestrictions: {country: 'in'}
	};
	var autocomplete2 = new google.maps.places.Autocomplete(input2, options);
	google.maps.event.addListener(autocomplete2, 'place_changed', function () {
	            var place = autocomplete2.getPlace();
	            document.getElementById('endlat').value = place.geometry.location.lat();
	            document.getElementById('endlong').value = place.geometry.location.lng();
	            makeroutecheck();
	        });
}
google.maps.event.addDomListener(window, 'load', initialize2);