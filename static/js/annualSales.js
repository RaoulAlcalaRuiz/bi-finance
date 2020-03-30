Highcharts.chart('area-annual-sales', {
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
        ,
        column: {
            stacking: 'normal',
        },
        area: {
            stacking: 'normal',
        }
    },
    xAxis: {
        categories: ["1","2","3","4","5","6","7","8","9","10","11","12"]
    },
    series:
    JSON.parse($("#ca_annuals").html())
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
        name: 'Résultats',
        color: '#2748ab'},
        {
        name: 'Objectifs',
        color: '#5e8fbd'
        }]
});

Highcharts.chart('bar-employee-annual-sales', {
    data: {
        table: 'employe-annual-sales'
    },
    chart: {
        type: 'column'
    },
    title: {
        text: 'Objectif mensuel des employés'
    },
    plotOptions: {
        column: {
            stacking: 'percent'
        }
    },
    tooltip: {
        pointFormat: '{series.name} \: <b>{point.y:,.0f}</b>'
    },
});