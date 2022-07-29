function check_reactivate(){
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
        alert('您即将激活成功！\n点击【确认】后，激活链接将发至您的邮箱，请您稍后查看邮箱进行激活！\nTips:激活链接有效时间为24小时，只有激活后的账号才能登录使用哦！');
    }
    return is_submit;
}