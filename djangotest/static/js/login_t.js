$(function(){
     $('.flex-c-c').submit(function(){
        var $teacherid = $('#js-field__id');
        var $teacherpaw = $('#js-field__pass');
        var teacherid = $teacherid.val().trim();
        var teacherpaw = $teacherpaw.val();
    	if(teacherid.length>0 && teacherpaw.length>0){
    	    $.getJSON('/zxy/checklogint/', {'teacherid':teacherid, 'teacherpaw':teacherpaw }, function(data){
                    console.log(data);
                    var error_info = $('#id_error');
                    if(data['status']===200){

                    }else if(data['status']===902){
                        error_info.text("*职工号或密码错误！");
                    }
                })
    	}
    })
})