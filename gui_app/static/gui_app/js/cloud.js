$("[name=type]").change(function (){

	$("#tenant").show();
	if($(this).val() == 'aws' || $(this).val() == 'wakamevdc'){
		$("[name=tenant_name]").val("");
		$("#tenant").hide();
	}
});
