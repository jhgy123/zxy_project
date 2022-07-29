    function check_login_t(){
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
        return is_submit
    }
