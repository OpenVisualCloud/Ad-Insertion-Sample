$(document).foundation();
$(window).bind("load", function () {
    $(".top-bar").trigger(":initpage");
    $("#player").trigger(":update");

    $("[debug-console]").trigger(":initpage");
    $("[adstats-console]").trigger(":initpage");
    $("[workloads-console]").trigger(":initpage");
    $("[analytics-console]").trigger(":initpage");
    $("[analyticPerf-console]").trigger(":initpage");
});
