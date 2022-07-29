function check_reset_s(){
    var $password_input = $('#js-field__pass');
    var password = $password_input.val().trim();
    $password_input.val(MD5(password));

    var is_submit=true;
    var errors = $('.error');
    for(var i=0; i<errors.length; ++i){
        if(errors[i].innerText!=""){
            console.log({'static':900});
            is_submit=false;
            break;
        }
    }
    if(is_submit){
        alert('点击【确认】后，密码重置链接将发至您的邮箱，请您稍后查看邮箱进行密码重置！\nTips:密码重置链接有效时间为24小时，请及时操作！');
    }
    return is_submit;
}