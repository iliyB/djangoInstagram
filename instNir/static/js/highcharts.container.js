var data = {{ objects|safe }}
var title = {{ title|safe }}
Highcharts.chart('container', {
    chart: {
        type: 'column'
    },
    title: {
        text: title
    },
    xAxis: {
        type: 'category',
        labels: {
            rotation: -45,
            style: {
                fontSize: '13px',
                fontFamily: 'Verdana, sans-serif'
            }
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: 'количество'
        }
    },
    legend: {
        enabled: false
    },
    series: [{
        data: data,
    }]
});
}