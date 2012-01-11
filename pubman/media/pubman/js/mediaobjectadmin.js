function showSelectedFields() {
	switch($('#id_media_type option:selected').val()) {
	case 'I':
		$(".images-on-site").show();
		$(".video-on-site").hide();
		$(".embedded").hide();
		break;
	case 'V':
		$(".images-on-site").hide();
		$(".video-on-site").show();
		$(".embedded").hide();			
		break;
	case 'E':
		$(".images-on-site").hide();
		$(".video-on-site").hide();
		$(".embedded").show();			
		break;
	}	
}

jQuery(document).ready(function($){
	showSelectedFields();
	$('#id_media_type').change(function(){
		showSelectedFields();
	});	
});
