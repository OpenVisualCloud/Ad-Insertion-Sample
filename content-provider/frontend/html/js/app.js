
function spec(key) {
    var kvs=window.location.search.substring(1).split('&');
    for (var i = 0; i < kvs.length; i++) {
        var kv=kvs[i].split('=');
        if (kv[0] === key) return kv[1] === undefined ? true : decodeURIComponent(kv[1]);
    }
    return false;
}

$(document).foundation();
$(window).bind("load", function () {
    if (spec("header")=="off") $("[ui-header]").hide();
    if (spec("playlist")=="off") $("[playlist-section]").hide();
    if (spec("videourl")=="off") $("#player [video-section] .input-group").hide();
    if (spec("seq")) settings.user("u"+spec("seq"));
    if (spec("benchmark")) apiHost.usecase(settings.user(), spec("benchmark"), 1);

    $(".top-bar").trigger(":initpage");
    $("#player").trigger(":update");

    $("[debug-console]").trigger(":initpage");
    $("[adstats-console]").trigger(":initpage");
    $("[workloads-console]").trigger(":initpage");
    $("[analytics-console]").trigger(":initpage");
    $("[analyticPerf-console]").trigger(":initpage");

});
