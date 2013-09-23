$(document).ready(function() {
	
	// hide all forms
	$("form.number").hide();
	$("form.new_debitor").hide();
	
	// display form for the specified debitor
	$("span.edit").live('click', function() {
		var id = $(this).attr('id');
		$("span.number[id="+id+"]").hide();
		$("form.number[id="+id+"]").show();
		$("form.number[id="+id+"]").focus();
		var amount = $("input.amount[id="+id+"]").val();
		var i = 1;
		numbers = 0;
		while(amount >= i) {
			i = i * 10;
			numbers++;
		}
		if(numbers == 0) {numbers = 1};
		var width = numbers*15 + 5;
		$("input.amount[id="+id+"]").width(width);
	});
	
	// save new data for specified debitor
	$("form.number").live('submit', function() {
		var id = $(this).attr('id');
		var data = {debitorID: id, 
					creditorID: $("span.owner").attr('id'),
					amount: $("input.amount[id="+id+"]").val()};
		$.ajax({
	       url: '/editDebitor',
	       type: 'POST',
	       data: data,
	       dataType: 'text',
	       error: function() { 
	           alert('An error occured. Please notify it by mail to jeremy@youowemeone.info. Thanks.');
	           $("form.number[id="+id+"]").hide();
	           $("span.number[id="+id+"]").show();
	           },
	       success: function(res) {
	           if(res != 'ok') {
	               alert('An error occured. Please notify it by mail to jeremy@youowemeone.info. Thanks.');
	               $("form.number[id="+id+"]").hide();
	               $("span.number[id="+id+"]").show();
	           } else {
	               $("form.number[id="+id+"]").hide();
			       $("span.number[id="+id+"]").text(data.amount);	   	
	   		       $("span.number[id="+id+"]").show();
	           }
	       }
	   	});
	   	return false;
	});
	
	// delete specified debitor
	$("span.delete").live('click', function() {
		var id = $(this).attr('id');
		var data = {debitorID: id, 
					creditorID: $("span.owner").attr('id')};
		$.ajax({
	       url: '/deleteDebitor',
	       type: 'POST',
	       data: data,
	       dataType: 'text',
	       error: function() { alert('An error occured. Please notify it by mail to jeremy@youowemeone.info. Thanks.'); },
	       success: function(res) {
	           if(res != 'ok') {
	               alert('An error occured. Please notify it by mail to jeremy@youowemeone.info. Thanks.');
	           }
	       }
	   	});
		$(this).parent().parent().remove();	   	
	   	if($("li").length == 0) {
	   		$("p.noone").show();
	   	}
	});
	
	// add new debitor
	$("span.add_owned").click(function(){
		$("form.new_debitor").show();
	});
	
	
	$("form.new_debitor").live('submit', function() {
		var data = {creditorID: $("span.owner").attr('id'),
					debitorName: $(this).children("input#debitorName").val(),
					amount: $(this).children("input#amount").val()};
		$.ajax({
	       url: '/addDebitor',
	       type: 'POST',
	       data: data,
	       dataType: 'text',
	       error: function() { alert('An error occured. Please notify it by mail to jeremy@youowemeone.info. Thanks.'); },
	       success: function(id) {
	           if(id == 'no') {
		           //$("form.new_debitor").hide();
		           alert('Oops!\nLooks like you used non authorized characters in the name (you can only use A-Za-z0-9 along with . - and _) or you tried to put things other than number in the number of beers field.\nTry again!');
	           } else {
		           $("form.new_debitor").hide();
		           $("form.new_debitor").children("input#debitorName").val('');
		           $("form.new_debitor").children("input#amount").val('');
		           $("ul.owned_list").append('<li id="'+id+'"> <span class="owned">'+data.debitorName+'</span>, you owe me <span class="number" id="'+id+'">'+data.amount+'</span> <form class="number" id="'+id+'"> <input type="text" class="amount" name="n" id="'+id+'" value="'+data.amount+'"/> </form> beer'+ (data.amount > 1 ? 's' : '') +'! <div class="actions"> <span class="edit" id="'+id+'">edit</span><br/> <span class="delete" id="'+id+'">delete</span> </div> </li>');
		           $("ul.owned_list > li:last").children("form").hide();
	           }
	       }
	   	});
	   	if($("p.noone").length > 0) {
	   		$("p.noone").hide();
	   	}
		
	   	return false;
	});
	
	// HOME PAGE
	
	// hide messages
	$("p.nick_taken").hide();
	$("p.success").hide();
	$("p.bad_chars").hide();
	
	//add new creditor
	$("form.subscribe").submit(function() {
	
		$("p.nick_taken").hide();
		$("p.success").hide();
		$("p.bad_chars").hide();
	
		data = {creditorName: $(this).children("input#creditorName").val()};
		$.ajax({
	       url: '/addCreditor',
	       type: 'POST',
	       data: data,
	       dataType: 'text',
	       error: function() { alert('An error occured. Please notify it by mail to jeremy@youowemeone.info. Thanks.'); },
	       success: function(res) {
	           if(res=='1') {
	           		$("p.nick_taken").show();
	           } else if(res=='2') {
	           		$("p.bad_chars").show();
	           } else {
		           $("p.success").children("a.account_link").attr("href", "http://youowemeone.info/"+data.creditorName);
		           $("p.success").children("a.account_link").text("youowemeone.info/"+data.creditorName);
	    	       $("p.success").show();
	    	   }
	       }
	   	});
		return false;
	});
	
	// PERSO
	$("table.conversion").hide();
	$("span.hide_table").hide();
	$("span.toggle_conversion_table#show").click(function() {
		$("table.conversion").fadeIn('fast');
		$("span.show_table").hide();
		$("span.hide_table").show();
	});
	$("span.toggle_conversion_table#hide").click(function() {
		$("table.conversion").fadeOut('fast');
		$("span.show_table").show();
		$("span.hide_table").hide();
	});

});