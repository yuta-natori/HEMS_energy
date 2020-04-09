<script type="text/javascript">
	$(function(){
		var from = $("#from").datepicker({
			onSelect: function(selectedDate) {
			$("#to").datepicker("option","minDate",selectegDate);
		}
	});
		var to =$("#to").datepicker({
			onSelect: function(selectedDate){
			$("#from").datepicker("option","maxDate",selectedDate);
		}
	});
	});
</script>
