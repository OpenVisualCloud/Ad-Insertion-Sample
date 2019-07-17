
var apiHost={
    playList: function (name) {
        var url="api/playlist";
        var args= { name: name };
        console.log("GET "+url+"?"+JSON.stringify(args));
        return $.get(url, args);
    },
    click: function (name, x, y, t, stream) {
        var url="api/click";
        var args= { x: x, y:y, name: name, t:t, stream:stream }
        console.log("POST "+url+"?"+JSON.stringify(args));
        return $.post(url, args);
    },
    debug: function (ondata) {
        if (!!window.Worker) {
            var worker=new Worker('js/app-worker.js');
            worker.onmessage=ondata;
            worker.postMessage(window.location.protocol.replace("http","ws")+window.location.host+window.location.pathname+"api/debug");
        }
    },
    analytics: function (stream, start, end) {
        var url="api/debug/analytics";
        var args= { stream: stream, start: start, end:end }
        //console.log("GET "+url+"?"+JSON.stringify(args));
        return $.get(url, args);
    },
    usecase: function (casename,enable) {
        var url="api/usecase";
        var args= { casename: casename, enable: enable };
        console.log("POST "+url+"?"+JSON.stringify(args));
        return $.post(url, args);
    },
};
