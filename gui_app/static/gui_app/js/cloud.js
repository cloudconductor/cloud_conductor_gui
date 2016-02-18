$("[name=type]").change(function (){

	$("#tenant").show();
	if($(this).val() == 'aws'){
		$("[name=tenant_name]").val("");
		$("#tenant").hide();
	}
});