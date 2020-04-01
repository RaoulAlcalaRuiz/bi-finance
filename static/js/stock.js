Highcharts.chart('stock_chart', {
    data: {
        table: 'stock-data'
    },
    chart: {
        zoomType: 'xy'
    },
    title: {
        text: 'Objectif mensuel'
    },
    yAxis: {
        labels: {
            formatter: function () {
                return this.value/1000 + 'k';
            }
        },
    },
    xAxis: {
        tickInterval: 1,
    },
    tooltip: {
        pointFormat: '{series.name} \: <b>{point.y:,.0f} </b>'
    },
    series: [{
            name: 'stock - actuel',
            type: 'column',
            color: '#fc8d1e'
        },
        {
            name: 'stock - objectif',
            type: 'spline',
            color: '#2450ff'
        }]
});

Highcharts.chart('stock_per_cat', {
    chart: {
        type: 'area'
    },
    title: {
        text: 'Valeur du stock par marque'
    },
    yAxis: {
        labels: {
            formatter: function () {
                return this.value / 1000 + 'k';
            }
        }
    },
    tooltip: {
        pointFormat: '{series.name} \: <b>{point.y:,.0f}</b>'
    },
    plotOptions: {
        area: {
            pointStart: 1,
            marker: {
                enabled: false,
                symbol: 'circle',
                radius: 2,
                states: {
                    hover: {
                        enabled: true
                    }
                }
            }
        }
    },
    xAxis: {
        categories: ["1","2","3","4","5","6","7","8","9","10","11","12"]
    },
    series:
    JSON.parse($("#stock_per_cat_data").html())
});