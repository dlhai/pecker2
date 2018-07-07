function int(s) {
    if (s == "") return 0;
    else if (s == "None") return 0;
    else return parseInt(s);
}

//var str = '这是一个测试的字符串：{0} {1}'.format('Hello', 'world');
//var str = '这是一个测试的字符串：{str0} {str1}'.format({ str0: 'Hello', str1: 'world' });
String.prototype.format = function (args) {
    var result = this;
    if (arguments.length > 0) {
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                if (args[key] != undefined) {
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
            }
        }
        else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] != undefined) {
                    var reg = new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
    }
    return result;
}

//判断是否以某个字符串结尾
String.prototype.endWith=function(endStr){
      var d=this.length-endStr.length;
      return (d>=0&&this.lastIndexOf(endStr)==d)
}

// 对Date的扩展，将 Date 转化为指定格式的String   
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，   
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)   
// 例子：   
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423   
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18   
Date.prototype.format = function (fmt) { //author: meizz   
    var o = {
        "M+": this.getMonth() + 1,                 //月份   
        "d+": this.getDate(),                    //日   
        "h+": this.getHours(),                   //小时   
        "m+": this.getMinutes(),                 //分   
        "s+": this.getSeconds(),                 //秒   
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度   
        "S": this.getMilliseconds()             //毫秒   
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}  

// 对Array的扩展，相当于将Array的filter和map的功能合并
Array.prototype.fmap = function (cb) {
    return this.map(cb).filter(x => x != undefined);
}

// 对Array的扩展
Array.prototype.insertaftername = function (name, it ) {
	idx =GetIdx(this, "name", name);
	if ( idx != null)
		this.splice(idx,0,it);
}

function isInArray(arr, value) {
    for (var i = 0; i < arr.length; i++) {
        if (value === arr[i]) {
            return true;
        }
    }
    return false;
}

//生成一个随机字符串
function rndstr(len) {
    var chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    var maxPos = chars.length + 1;
    var pwd = '';
    for (i = 0; i < len; i++)
        pwd += chars.charAt(Math.floor(Math.random() * maxPos));
    return pwd;
}

// 取url中的参数
function GetParam(name) {
    var url = decodeURI(window.location.search);
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = url.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return "";
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
    if (typeof obj == typeof []) 
        var r = new Array();
    else
        var r = new Object();

    for (var k in obj) {
        var val = obj[k];
        r[k] = typeof val === 'object' ? Clone(val) : val;
    }

    return r;
}

function Create(fields) {
    var r = new Object();
	fields.forEach(x=>r[x.name]="");
    return r;
}

// 将a和b合并，新的对象有a和b的所有属性，若两个均有某一属性，则a的属性优先
function mix(a,b){
	var r = Clone(b);
    for (var k in a) {
        var val = a[k];
        r[k] = typeof val === 'object' ? Clone(val) : val;
    }
	return r;
}

