$(".top-bar").on(":initpage", function(e) {
    $("#setting").find("[ui-header-setting-user] input").val(settings.user());
    $("#setting").find("[ui-header-setting-analytics-window] input").val(settings.analytics_window());
    $(this).find("[user-name-menu]").text(settings.user());

    /* disable all switches */
    $("#playListSwitch").prop("checked",true);
    $("#objDetectionSwitch").prop("checked",settings.algorithms().search("object")>=0);
    $("#emotionRecognitionSwitch").prop("checked",settings.algorithms().search("emotion")>=0);
    $("#faceRecognitionSwitch").prop("checked",settings.algorithms().search("face")>=0);
    $.each(["debug","analytics","adstats","workloads"],function(i,x) {
        $("#"+x+"ConsoleSwitch").prop("checked",false);
    });
});

$("#setting").find("form").submit(function() {
    var page=$(this);

    var user=page.find("[ui-header-setting-user] input").val().toLowerCase();
    settings.user(user);
    $(".top-bar").find("[user-name-menu]").text(user);
    
    settings.analytics_window(page.find("[ui-header-setting-analytics-window] input").val());

    $.each(["debug","analytics","adstats","workloads"],function(i,x) {
        if ($("#"+x+"ConsoleSwitch").is(":checked"))
            $("["+x+"-console]").show();
        else
            $("["+x+"-console]").hide();
    });

    if ($("#playListSwitch").is(":checked")) {
        $("#player [playlist-section]").show();
        $("#player [video-section]").width("70%");
    } else {
        $("#player [playlist-section]").hide();
        $("#player [video-section]").width("100%");
    }

    if ($("#objDetectionSwitch").is(":checked")) {
       settings.algorithms(settings.algorithms().replace("object ","")+"object ");
    } else {
       settings.algorithms(settings.algorithms().replace("object ",""));
    }

    if ($("#emotionRecognitionSwitch").is(":checked")) {
       settings.algorithms(settings.algorithms().replace("emotion ","")+"emotion ");
    } else {
       settings.algorithms(settings.algorithms().replace("emotion ",""));
    }

    if ($("#faceRecognitionSwitch").is(":checked")) {
       settings.algorithms(settings.algorithms().replace("face ","")+"face ");
    } else {
       settings.algorithms(settings.algorithms().replace("face ",""));
    }

    $("#player").trigger(":update");
    return false;
});

var settings={
    localStorage: {},
    user: function (name) {
        if (typeof name != "undefined") settings.localStorage.user=name;
        return typeof settings.localStorage.user!="undefined"?settings.localStorage.user:"guest";
    },
    analytics_window: function (size) {
        if (typeof size != "undefined") settings.localStorage.analytics_window=size;
        return typeof settings.localStorage.analytics_window!="undefined"?parseFloat(settings.localStorage.analytics_window):10;
    },
    algorithms: function (value) {
        if (typeof value != "undefined") settings.localStorage.algorithms=value;
        return typeof settings.localStorage.algorithms!="undefined"?settings.localStorage.algorithms:"object face emotion ";
    },
}
