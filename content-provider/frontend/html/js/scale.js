
function spec(key) {
    var kvs=window.location.search.substring(1).split('&');
    for (var i = 0; i < kvs.length; i++) {
        var kv=kvs[i].split('=');
        if (kv[0] === key) return kv[1] === undefined ? true : decodeURIComponent(kv[1]);
    }
    return false;
}

function mklayout() {
    var body=$("#scale");
    var body_width=body.width();
    var body_height=body.height();
    body.find("[screen]").empty();

    var card=$("#scale [vcac-a-icon]");
    var divide_width=card.width()*0.45+20;

    var ncolumns=spec("ncols")?Math.floor((parseInt(spec("ncols"),10)+1)/2)*2:2;
    var nrows=spec("nrows")?parseInt(spec("nrows"),10):3;
    var userid=spec("userid")?parseInt(spec("userid"),10):100;
    $("#scale [info-block] [channel]").text(nrows*ncolumns);

    var header_height=144;
    var margin=5;
    var view_port_height_adjust=0.8148;
    var screen_width=Math.floor((body_width-divide_width)/ncolumns-margin*2);
    var screen_height=Math.floor((body_height-header_height)/nrows-margin*2);
    var aspect_ratio=screen_width/(screen_height*view_port_height_adjust);
    var screen_width1=aspect_ratio>16/9?screen_height*view_port_height_adjust*16/9:screen_width;

    var lines=body.find("[lines] svg");
    lines.attr("width",body_width).attr("height",body_height);
    lines.empty();
    
    var signals=body.find("[signals]");
    signals.empty();

    for (var r=0;r<nrows;r++) {
        var y=(screen_height+margin*2)*r+header_height;
        for (var c=0;c<ncolumns;c++) {
            var x=(screen_width+margin*2)*c;
            if (c>=ncolumns/2) x=x+divide_width;
            var args={ 
                seq: userid+r*ncolumns+c, 
                benchmark: spec("benchmark")?spec("benchmark"):"object",
                header: "off",
                playlist: "off",
                videourl: "off",
                window: spec("window")?spec("window"):20,
            };
            var tmp=$('<div screen><iframe src="/?'+$.param(args)+'" scrolling="no" /><img src="image/screen.png"/></div>');
            var view_port_width=screen_width1-margin*2;
            var view_port_height=screen_height*0.8-margin*2;
            tmp.find("iframe").attr("width",view_port_width).attr("height",view_port_height).css({width:view_port_width+"px",height:view_port_height+"px"});
            tmp.find("img").attr("width",screen_width1).attr("height",screen_height);

            var view_port_x=(screen_width-screen_width1)/2;
            tmp.css({width:screen_width1+"px",height:screen_height+"px",left:x+view_port_x+"px",top:y+"px"});
            body.append(tmp);

            var line=$(document.createElementNS(lines.attr('xmlns'),"line"));
            line.attr({
              x1: body_width/2,
              x2: x+view_port_x+screen_width1/2,
              y1: body_height/2,
              y2: y+screen_height/2,
              stroke: "white",
              "stroke-width": 3,
            });
            lines.append(line);

            var signal=$("#template [signal]").clone();
            signal.css({
              "--signalx": x+view_port_x+screen_width1/2-body_width/2,
              "--signaly": y+screen_height/2-body_height/2,
            });
            signals.append(signal);
        }
    }
}

$(window).bind("load", function () {
    setTimeout(mklayout, 15000);
    setTimeout(function () { 
        window.location.reload(true); 
    }, (spec("duration")?parseFloat(spec("duration")):30)*60*1000);
}).resize(mklayout);
