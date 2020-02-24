
Highcharts.chart('area-annual-sales', {
    data: {
        table: 'annual-sales-cumulative'
    },
    chart: {
        type: 'area'
    },
    title: {
        text: 'Chiffre d\'affaires Réalité/Objectif'
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