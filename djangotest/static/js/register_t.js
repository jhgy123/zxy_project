$(function(){
	var $teacherid = $('#js-field__id');
	$teacherid.change(function(){
	    var teacherid = $teacherid.val().trim();
        if(teacherid.length){
            $.getJSON('/zxy/checktid/', {'teacherid':teacherid}, function(data){
                console.log(data);
                var error_info = $('#id_error');
                if(data['status']===200){

                }else if(data['status']===901){
                    error_info.text("*该职工号已被注册！");
                }
            })
	}
	})
})

