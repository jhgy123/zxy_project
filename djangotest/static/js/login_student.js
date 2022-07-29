$(function(){
    $('#js-field__id').val("")
	$('#js-field__name').blur(function(){
		var content = this.value;
		var name = $.trim(content);
		var reg = /^[\u4e00-\u9fa5]+$/;
		if(name === ""){
			$('#name_error').text("*真实姓名不能为空！");
		}
		else if(!reg.test(name)){
			$('#name_error').text("*请输入真实姓名！");
		}
		else{
			$('#name_error').text("");
		}
	});
		
	$('#js-field__id').blur(function(){
		var content = this.value;
		var id = $.trim(content);
		var reg = /^\d{11}$/;
		if(id === ""){
			$('#id_error').text("*学号不能为空！");
		}
		else if(!reg.test(id)){
			$('#id_error').text("*请输入正确的学号！");
		}
		else{
			$('#id_error').text("");
		}
	});
	
	$('#js-field__email').blur(function(){
		var content = this.value;
		var email = $.trim(content);
		var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
		if(email === ""){
			$('#email_error').text("*邮箱不能为空！");
		}
		else if(!reg.test(email)){
			$('#email_error').text("*请输入正确的邮箱！");
		}
		else{
			$('#email_error').text("");
		}
	});
	
	$('#js-field__pass').blur(function(){
		var content = this.value;
		var paw = $.trim(content);
		var reg = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/;
		if(paw === ""){
			$('#pass_error').text("*密码不能为空！");
		}
		else if(!reg.test(paw)){
			$('#pass_error').text("*输入密码格式错误！(至少8个字符，至少1个字母，1个数字和1个特殊字符[$,@,$,!,%,*,#,?,&])");
		}
		else{
			$('#pass_error').text("");
		}
	});
	
	$('#js-field__pass').focus(function(){
		$('#js-field__pass').val("");
		$('#js-field__r-pass').val("");
		$('#r-pass_error').text("");
	});
})