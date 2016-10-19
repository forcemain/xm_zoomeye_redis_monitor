// 添加REDIS
function redis_add(rds_host, rds_port, rds_pass, usermail) {
    var add_time = moment().format()
    $.ajax({
        type: 'POST',
        async: true,
        dataType: 'json',
        url: '/api/redis/add',
        data: {
            'rds_host': rds_host,
            'rds_port': rds_port,
            'rds_pass': rds_pass,
            'add_time': add_time,
            'usermail': usermail},
        success: function (data) {
            if(data.success == 1){
                location.reload()
            }else{
                alert('errors: add redis host with error!')
            }
        },
        error: function (req, rsp, err) {
            alert('errors: add redis host with error!')
        }
    })
}

// PINGREDIS
function redis_ping(rds_host, rds_port, rds_pass, usermail) {
    $('form input').attr('disabled', 'disabled')
    $.ajax({
        type: 'POST',
        async: true,
        dataType: 'json',
        url: '/api/redis/ping',
        data: {'rds_host': rds_host, 'rds_port': rds_port, 'rds_pass': rds_pass},
        success: function (data) {
            if(data.success == 1){
                $('form input').removeAttr('disabled')
                redis_add(rds_host, rds_port, rds_pass, usermail)
            }else{
                $('form input').removeAttr('disabled')
                alert('errors: redis host can not be ping!')
            }
        },
        error: function(req, rsp, err) {
            $('form input').removeAttr('disabled')
            alert('errors: redis host can not be ping!')
        }
    })
}

// 添加REDIS按钮
function redis_add_btn_click() {
    var rds_host = $('#rds_host').val() || ''
    var rds_pass = $('#rds_pass').val() || ''
    var usermail = $('#usermail').val() || ''
    var rds_port = $('#rds_port').val() || 5123

    if(rds_host == ''){
        alert('notice: redis host can not be empty!')
        return false
    }
    redis_ping(rds_host, rds_port, rds_pass, usermail)
}

// 删除REDIS
function redis_delete(identify) {
    $.ajax({
        type: 'POST',
        async: true,
        dataType: 'json',
        url: '/api/redis/delete',
        data: {'identify': identify},
        success: function (data) {
            if(data.success == 1){
                location.reload()
            }else{
                alert('errors: delete redis with errors!')
            }
        },
        error: function (req, rsp, err) {
            alert('errors: delete redis with errors!')
        }
    })
}

// 删除REDIS按钮
function redis_del_lnk_click(identify) {
    redis_delete(identify)
}

// 编辑REDIS
function redis_edit(identify) {
    
}

// 编辑REDIS按钮
function redis_edt_lnk_click(identify) {
    redis_edit(identify)
}


// 增加表格搜索功能
$(document).ready(function(){
    $('.redis_table').dataTable({
        "searching": true,
        "paging": false,
        "lengthChange": false,
        "info": false,
        "columnDefs": [{
            "targets": 'nosort',
            "orderable": false
        }],
        "order": [1]
    });
})
