/*
 * This code handles the tinymce textareas marked "editor". 
 * If markup == 'H' (for HTML), the textarea is made into a tinymce editor, else
 * it is just a plain textarea.
 *  
 * It also counts words and characters for textareas marked "editor" 
 */

function CustomFileBrowser(field_name, url, type, win) {

    var cmsURL = "/admin/filebrowser/browse/?pop=2";
    cmsURL = cmsURL + "&type=" + type;
    
    tinyMCE.activeEditor.windowManager.open({
        file: cmsURL,
        width: 820,  
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "no",  
        close_previous: "no"
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId
    });
    return false;
}


tinyMCE.init({
	mode : "none",
	theme : "advanced",
	language: "en",
    skin: 'grappelli',	
	theme_advanced_toolbar_location : "top",
	theme_advanced_toolbar_align : "left",
    theme_advanced_statusbar_location : "bottom",
    theme_advanced_resizing : true,	
	theme_advanced_buttons1 : "fullscreen,separator,preview,separator,bold,italic,underline,strikethrough,separator,bullist,numlist,outdent,indent,separator,undo,redo,separator,link,unlink,anchor,separator,image,media,spellchecker,help,separator,code",
	theme_advanced_buttons2 : "",
	theme_advanced_buttons3 : "",
    skin : "o2k7",
    skin_variant : "silver",	
    file_browser_callback: "CustomFileBrowser",
	auto_cleanup_word : true,
	plugins : "spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
	plugin_insertdate_dateFormat : "%m/%d/%Y",
	plugin_insertdate_timeFormat : "%H:%M:%S",
	extended_valid_elements : "a[name|href|title|onclick],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]",
	fullscreen_settings : {
		theme_advanced_path_location : "top",
		theme_advanced_buttons1 : "fullscreen,separator,preview,separator,media,spellchecker,cut,copy,paste,separator,undo,redo,separator,search,replace,separator,code,separator,cleanup,separator,bold,italic,underline,strikethrough,separator,forecolor,backcolor,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,help",
		theme_advanced_buttons2 : "removeformat,styleselect,formatselect,fontselect,fontsizeselect,separator,bullist,numlist,outdent,indent,separator,link,unlink,anchor",
		theme_advanced_buttons3 : "sub,sup,separator,image,insertdate,inserttime,separator,tablecontrols,separator,hr,advhr,visualaid,separator,charmap,emotions,iespell,flash,separator,print"
	},

	// ##NOT DRY## 
	setup: function(ed) {
    	ed.onKeyUp.add(function(ed, e) {
    		countWordsAndChars($('#'+this.id)[0], ed.getContent());    				
    	});
	}
});



function switchOffEditor(selector, editor) {
	switch(editor) {
	case 'H':
		tinyMCE.execCommand('mceRemoveControl', false, selector.id);
		break;
	case 'M':
		$('#'+selector.id).markItUpRemove();		
		break;
	}
}

function switchOnEditor(selector, editor) {
	switch (editor) {
	case 'H':
		tinyMCE.execCommand('mceAddControl', false, selector.id);
		break;
	case 'M':
		$('#'+selector.id).markItUp(mySettings);
		break;
	}
};

var editor='T'; // Default editor to plain text

function checkTextFormat() {

	current_editor = $('#id_text_format option:selected').val();

	switch (current_editor) {
	case 'H': //HTML editor (tinymce)
		if (editor!='H') {
			$(".editor textarea").each(function(intIndex) {
				switchOffEditor($(this)[0], editor);
			});
			editor = 'H';
			$(".editor textarea").each(function(intIndex) {
				switchOnEditor($(this)[0], editor);
			});
		}			
		break;
	case 'M': //Markdown editor
		if (editor!='M') {
			$(".editor textarea").each(function(intIndex) {
				switchOffEditor($(this)[0], editor);
			});
			editor = 'M';
			$(".editor textarea").each(function(intIndex) {
				switchOnEditor($(this)[0], editor);
			});				
		}			
		break;
	case 'R': //reStructuredText
		if (editor!='R') {
			$(".editor textarea").each(function(intIndex) {
				switchOffEditor($(this)[0], editor);
			});
			editor = 'R';			
		}					
		break;
	case 'T': //Plain text
		if (editor!='T') {
			$(".editor textarea").each(function(intIndex) {
				switchOffEditor($(this)[0], editor);
			});
			editor = 'T';			
		}					
	}
};

// This function works on non TinyMCE fields. 
// Ideally it should work on TinyMCE as well.

function countWordsAndChars(selector, txt) {
	text = txt.replace(/(<([^>]+)>)/g,"").replace(/&nbsp;/g," ");
    text = $.trim(text);
    if (text.length==0) {
    	wordcount = 0;
    	charcount = 0;
    } else {
    	wordcount = text.split(' ').length;
    	charcount = text.length;
    }
	$('#' + $(selector)[0].id + '_wordcount').html("<span>" + wordcount + 
			"</span> words, <span>" + charcount + "</span> characters");
}

jQuery(document).ready(function($){
	//Handle switching to and from TinyMCE Editor for textareas in editor class
	checkTextFormat();
	$('#id_text_format').change(function(){
		checkTextFormat();
	});
	
	// Word and character counting of textareas in editor class 
	$(".editor textarea").each(function(intIndex) {
		var count_string = '<div id="' + $(this)[0].id + '_wordcount" class="wordcount"> 0 words, 0 characters</div>'; 
		$(this).after(count_string);
		countWordsAndChars(this, $(this).val());		
		// Recount every time there is a key up on the textarea
		$(this).keyup(function(){
			countWordsAndChars(this, $(this).val());
		});	
	});
});

