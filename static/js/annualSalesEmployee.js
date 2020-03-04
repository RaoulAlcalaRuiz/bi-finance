Highcharts.chart('area-annual-sales', {
    data: {
        table: 'cumulative-annual-sales'
    },
    chart: {
        type: 'area'
    },
    title: {
        text: 'Objectif mensuel'
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
    series: [{
        name: 'Réalité',
        color: '#2748ab'},
        {
        name: 'Objectif',
        color: '#5e8fbd'
        }]
});

Highcharts.chart('bar-annual-sales', {
    data: {
        table: 'annual-sales'
    },
    chart: {
        type: 'column'
    },
    title: {
        text: 'Objectif mensuel'
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
    series: [{
        name: 'Réalité',
        color: '#2748ab'},
        {
        name: 'Objectif',
        color: '#5e8fbd'
        }]
});

Highcharts.chart('bar-annual-sales-forecast', {
    data: {
        table: 'annual-sales-forecast'
    },
    chart: {
        type: 'column'
    },
    title: {
        text: 'Objectif mensuel'
    },
    yAxis: {
        labels: {
            formatter: function () {
                return this.value / 1000 + 'k';
            }
        }
    },
    plotOptions: {
        column: {
            grouping: false,
            shadow: false,
            borderWidth: 0
        }
    },
    tooltip: {
        shared: true,
        pointFormat: '{series.name} \: <b>{point.y:,.0f}</b>'
    },
    series: [{
        name: 'Réalité',
        color: '#2748ab',
        pointPadding: 0,
        pointPlacement: 0
        },
        {
        name: 'Objectif',
        color: '#fc9803',
        pointPadding: 0.2,
        pointPlacement: 0
        }]
});
