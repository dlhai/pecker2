﻿function isInArray(arr, value) {
    for (var i = 0; i < arr.length; i++) {
        if (value === arr[i]) {
            return true;
        }
    }
    return false;
}

// 取url中的参数
function GetParam(name) {
    var url = decodeURI(window.location.search);
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = url.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

function GetSub(ar, attr, val) {
    for (var i in ar) {
        if (ar[i][attr] == val)
            return ar[i];
    }
    return null;
}

function GetIdx(ar, attr, val) {
    for (var i in ar) {
        if (ar[i][attr] == val)
            return i;
    }
    return null;
}

function Clone(obj) {
    var r = new Object();
    for (var k in obj) {
        var val = obj[k];
        r[k] = typeof val === 'object' ? cloneObj(val) : val;
    }
    return r;
}

function Create(fields) {
    var r = new Object();
    for (var k in fields)
        r[fields[k].name] = "";
    return r;
}
