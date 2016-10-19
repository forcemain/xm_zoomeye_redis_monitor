// 简单检查
function check_redis_exists() {
    var identify = $('#wrapper').attr('identify')
    return identify
}

// 获取数据
function get_redis_jsondata(identify) {
    function get_json(identify) {
        $.ajax({
            type: 'POST',
            async: true,
            dataType: 'json',
            url: '/api/redis/json',
            timeout: 5000,
            data: {'identify': identify},
            success: distributejsondata
        })
    }
    return function () {
        get_json(identify)
    }

}

// 填充表格
function fill_all_tabledata(data) {
    var info_keys = [
        'redis_version', 'os', 'process_id', 'uptime_in_seconds', 'connected_clients',
        'blocked_clients','total_connections_received', 'total_commands_processed',
        'instantaneous_ops_per_sec', 'rejected_connections', 'expired_keys', 'evicted_keys',
        'keyspace_hits', 'keyspace_misses']
    for(var _ in info_keys){
        var key = info_keys[_]
        var val = data[key]
        $('#'+key).text(val)
    }
    // 添加DB
    var html = ''
    for(var key in data){
        if(key.substring(0, 2)=='db'){
            var val = data[key]
            html += '<tr><td>'+
                    key +
                    '</td><td>'+
                    val.keys +
                    '</td><td>'+
                    val.expires +
                    '</td><td>'+
                    val.avg_ttl +'' +
                    '</td></tr>'
        }
    }

    $('.redis_database tbody tr').remove()
    $('.redis_database tbody').append(html)
}

// 处理数据
function distributejsondata(data) {
    if(data.success == 1){
        var x_date = (new Date()).toLocaleTimeString().replace(/^\D*/,'');
        fill_all_tabledata(data.data)
        tim_chart.addData([
            [
                0,
                data.data.get_time,
                false,
                false,
                x_date
            ]
        ]);
        ops_chart.addData([
		    [
                0,
                data.data.instantaneous_ops_per_sec,
                false,
                false,
                x_date
            ]
        ]);
        mem_chart.addData([
		    [
                0,
                (data.data.used_memory / 1024).toFixed(2),
                false,
                false,
                x_date
            ],
            [
                1,
                (data.data.used_memory_rss / 1024).toFixed(2),
                false,
                false,
                x_date
            ]
        ]);
        cpu_chart.addData([
		    [
                0,
                data.data.used_cpu_sys,
                false,
                false,
                x_date
            ],
            [
                1,
                data.data.used_cpu_user,
                false,
                false,
                x_date
            ],
            [
                2,
                data.data.used_cpu_user_children,
                false,
                false,
                x_date
            ],
            [
                3,
                data.data.used_cpu_sys_children,
                false,
                false,
                x_date
            ]
        ]);
    }else{
        tim_chart.addData([
            [0, 0, false, false, x_date]
        ])
        ops_chart.addData([
            [0, 0, false, false, x_date]
        ])
		mem_chart.addData([
		    [0, 0, false, false, x_date],
            [1, 0, false, false, x_date]
        ])
		cpu_chart.addData([
		    [0, 0, false, false, x_date],
            [1, 0, false, false, x_date],
            [2, 0, false, false, x_date],
            [3, 0, false, false, x_date]
        ])
    }
}

// 依赖配置
var echarts = null,
    tim_chart = null,
    ops_chart = null,
    mem_chart = null,
    cpu_chart = null

// 画监控图
function draw_chart(ecid, option) {
	var echart = echarts.init(document.getElementById(ecid));
	echart.setOption(option);
	return echart
}

// 生成选项
function echart_opt(text, subtext, legend, yAxis_name, y_format) {
    var option = {
        grid: {x2: 0},
        title : {
	        text: text,
	        subtext: subtext
	    },
        tooltip : {
	        trigger: 'axis'
	    },
	    legend: {
	        data:legend
	    },
	    toolbox: {
	        show : false,
	        // feature : {
	        //     mark : {show: true},
	        //     dataView : {show: true, readOnly: false},
	        //     magicType : {show: true, type: ['line', 'bar']},
	        //     restore : {show: true},
	        //     saveAsImage : {show: true}
	        // }
	    },
	    dataZoom : {
	        show : false,
	        start : 0,
	        end : 256
	    },
	    xAxis : [{
            type : 'category',
            boundaryGap : true,
            data : (function (){
                var now = new Date();
                var res = [];
                var len = 256;
                while (len--) {
                    res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
                    now = new Date(now - 2000);
                }
                return res;
            })()
	    }],
	    yAxis : [{
            type : 'value',
            scale: true,
            name : yAxis_name,
            axisLabel : {
                formatter: '{value} ' + y_format
            }
        }],
	    series : []
	};
	var tmp = null;
	var s = null;
	for (var i in legend) {
		tmp = legend[i];
		s = {
            name:tmp,
            type:'line',
            data:(function (){
                var res = [];
                var len = 256;
                while (len--) {
                    res.push(0.0);
                }
                return res;
            })()
        }
		option.series.push(s);
	}
	return option;
}

// 配置加载
require.config({
    paths: {
        echarts: '/static/js/echarts/'
    }
});
require([
    'echarts',
    'echarts/chart/bar',
    'echarts/chart/line',
],function (ec){
    echarts = ec
    // 实时折线
    tim_chart = draw_chart('tim_chart',
                           echart_opt('实时连通情况', '', ['连接时间'], '连接耗时', 'ms'))
    ops_chart = draw_chart('ops_chart',
                           echart_opt('每秒处理情况', '', ['处理频率'], '处理频率', '个'));
    mem_chart = draw_chart('mem_chart',
                           echart_opt('内存占用情况', '', ['RDS内存', '分配内存'], '内存占用', ' Kb'));
    cpu_chart = draw_chart('cpu_chart',
                           echart_opt('负载占用情况', '', ['cpu_user', 'cpu_sys', 'cpu_user_children', 'cpu_sys_children'], 'CPU消耗', ''));
    // 开启监控
    var identify = check_redis_exists()
    if(identify==''){
        alert('errors: redis identify not exists!')
        return false
    }
    setInterval(get_redis_jsondata(identify), 1000)
})
