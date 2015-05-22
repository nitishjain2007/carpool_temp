var todayselected = 0;
$(function() {
	$('#datepicker').multiDatesPicker({ 
		minDate: 0,
		onSelect: function(dateText, inst) {
			var dates = $(this).val();
			var currentDate = new Date();
			var day = (currentDate.getDate()).toString();
			if(day.length == 1){
				day = '0' + day;
			}
			var month = (currentDate.getMonth() + 1).toString();
			if(month.length == 1){
				month = '0' + month;
			} 
			var year = currentDate.getFullYear();
			currentdate = month + "/" + day + "/" + year;
            var dates = dates.split(", ");
            console.log(dates); 
            if(todayselected == 1){
                if(dates.indexOf(currentdate) == -1){
                    todayselected = 0;
                    $("#timepicker").timepicker("destroy");
                    normaltimepicker();
                }
            }
            if(todayselected == 0){
                console.log(dates.indexOf(currentdate));
                if(dates.indexOf(currentdate) != -1){
                    todayselected = 1;
                    $("#timepicker").timepicker("destroy");
                    modifiedtimepicker();
                } 
            }
		}
	});
	});
	function modifiedtimepicker(){
    alert("hi");
		var d = new Date();
		$('#timepicker').timepicker({
			minTime: {                    // Set the minimum time selectable by the user, disable hours and minutes
    		hour: d.getHours(),            // previous to min time
    		minute: d.getMinutes(),
		},
		});
}
function normaltimepicker(){
    $('#timepicker').timepicker();
}
$(function() {
    $('#timepicker').timepicker();
});