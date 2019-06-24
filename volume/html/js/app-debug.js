
$("[debug-console]").on(":initpage",function () {
    var page=$(this);

    var prev;
    page.find("[console-title]").mousedown(function(e) {
        prev={x:e.clientX,y:e.clientY};
        var move=function(e) {
            var tmp={x:prev.x-e.clientX,y:prev.y-e.clientY};
            prev={x:e.clientX,y:e.clientY};
            var offset=page.offset();
            page.offset({left:offset.left-tmp.x,top:offset.top-tmp.y});
        };
        var up=function (e) {
            $(document).off('mouseup',up);
            $(document).off('mousemove',move);
        };
        $(document).mouseup(up).mousemove(move);
    });

    page.find("button").click(function() {
        page.hide();
        $("#debugConsoleSwitch").prop("checked",false);
    });

    apiHost.debug(function (e) {
        var doc;
        try {
            doc=JSON.parse(e.data);
        } catch (e) {
            return;
        }

        if (page.is(":visible") && doc.topic!="workloads") {
            page.append("<pre>"+doc.topic+": "+doc.value+"<br></pre>");
            if (page.children().length>50)
                page.children().slice(2,3).remove();
        }

        try {
            doc.value=JSON.parse(doc.value);
        } catch (e) {
            return;
        }

        var panel=$("[workloads-console]");
        if (doc.topic=="workloads") {
            if (panel.is(":visible")) {
                try {
                    panel.trigger(":update-workloads",[moment(doc.value.time),doc.value.machine,doc.value.workload]);
                } catch (e) {
                }
            }
            return;
        }

        panel=$("[adstats-console]");
        if (doc.topic=="adstats") {
            if (panel.is(":visible")) {
                try {
                    panel.trigger(":update-adstats",[doc.value]);
                } catch (e) {
                }
            }
            return;
        }
    });
});

$("[analytics-console]").on(":initpage", function () {
    var page=$(this);

    $("#player video").unbind('timeupdate').on('timeupdate',function () {
        var stream=$("#player input").val();
        if ((stream.indexOf("dash/")>=0 && stream.indexOf(".mpd")>=0) || (stream.indexOf("hls/")>=0 && stream.indexOf(".m3u8")>=0)) {
            var current_time=$("#player video")[0].currentTime;
            apiHost.analytics(stream,current_time-0.150,current_time+0.150).then(function (data) {
                var objects={}
                $.each(data, function (x,v1) {
                    var time=Math.floor(v1.time);
                    if (!(time in objects)) objects[time]={}
                    $.each(v1.objects, function (x, v2) {
                        if ("detection" in v2) objects[time].d=v2.detection;
                        if ("emotion" in v2) objects[time].e=v2.emotion;
                        if ("face_id" in v2) objects[time].f=v2.face_id;
                    });
                });
                page.children().remove();
                $.each(objects, function (time,v2) {
                    var div1=page.parent().find("[analytics-template]").clone(false).removeAttr("analytics-template");
                    var ts1=parseInt(time,10);
                    div1.find("[timestring]").text([Math.floor(ts1/3600)%24,Math.floor(ts1/60)%60,ts1%60].map(v=>v<10?'0'+v:v).join(':'));
                    if ("d" in v2) {
                        div1.find("[labelstring]").text(v2.d.label);
                        div1.find("[baseimage]").attr("src","image/object_"+v2.d.label_id+"_"+v2.d.label+".png").width(40).height(40);
                    }
                    if ("e" in v2) {
                        div1.find("[overlayimage]").attr("src","image/"+v2.e.label+".png").width(24).height(24);
                    }
                    if ("f" in v2) {
                        if (v2.f.label!="Unknown")
                            div1.find("[labelstring]").text(v2.f.label);
                    }
                    page.append(div1.show());
                });
            });
        }
    });
}).on(":mouseclick",function (e) {
    $(this).next().trigger(e);
}).on(":mousemove",function (e) {
    $(this).next().trigger(e);
});

$("[adstats-console]").on(":initpage",function (e) {
    var page=$(this);

    page.data("chart",new Chart(page.find("[adstats-chart]"),{
        type: 'horizontalBar',
        data: {
            labels: [],
            datasets: [{
                data: [],
            }],
        },
        options: {
            elements: {
                rectangle: {
                    borderWidth: 2,
                },
            },
            reponsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'AD Report',
            },
            plugins: {
                colorschemes: {
                    scheme: 'tableau.Tableau20'
                },
            },
        }
    }));
}).on(":update-adstats",function (e, data) {
    var page=$(this);
    var chart=page.data("chart");

    $.each(data,function (k,v) {
        var i=chart.config.data.labels.indexOf(k);
        if (i>=0) {
            chart.config.data.datasets[0].data[i]=v;
            return;
        }
        chart.config.data.labels.push(k);
        chart.config.data.datasets[0].data.push(v);
    });
    chart.update();
});

$("[workloads-console]").on(":initpage",function (e) {
    var page=$(this);

    page.data("chart",new Chart(page.find("[workloads-chart]"),{
        type: 'line',
        data: {
            labels: [],
            datasets: [],
        },
        options: {
            reponsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Server Workloads',
            },
            scales: {
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: false
                    },
                    stacked: false, //true
                }],
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: false
                    },
                    type: 'time',
                    time: {
                        displayFormats: {
                            second: 'hh:mm:ss'
                        }
                    },
                    distribution: 'linear',
                }],
            },
            plugins: {
                colorschemes: {
                    scheme: 'tableau.Tableau20'
                },
            },
            elements: {
                line: {
                    tension:0,
                }
            },
            animation: {
                duration:0,
            },
            hover: {
                animationDuration:0,
            },
            responsiveAnimationDuration:0,
        }
    }));
}).on(":update-workloads",function (e, time, machine, workload) {
    var page=$(this);
    var chart=page.data("chart");

    var labels=chart.config.data.labels;
    labels.push(time);
    labels.sort();

    var datasets=chart.config.data.datasets;
    var m=-1;
    for (var i=0;i<datasets.length;i++)
        if (datasets[i].label==machine) { m=i; break; }
    if (m<0) {
        //if (datasets.length==0)
        //    datasets.push({label:machine,fill:'origin',data:[]});
        //else
        //    datasets.push({label:machine,fill:'-1',data:[]});
        datasets.push({label:machine,fill:false,data:[]});
        m=datasets.length-1;
    }

    datasets[m].data.push({t:time,y:workload});
    for (m=0;m<datasets.length;m++) {
        datasets[m].data.sort(function(a,b){
            return (a.t>b.t)-(a.t<b.t);
        });
    }

    /* remove excessive data points */
    if (labels.length>20) {
        var t=labels.shift();
        for (m=0;m<datasets.length;m++)
            for (var i=0;i<datasets[m].data.length;i++)
                datasets[m].data=datasets[m].data.filter(v=>v.t>t);
    }

    chart.update();
});
