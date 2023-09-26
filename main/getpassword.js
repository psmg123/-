let CryptoJS = require("crypto-js");
var aesUtil = {
    encrypt: function(t, r) {
        t instanceof Object && (t = JSON.stringify(t));
        var p = CryptoJS.AES.encrypt(CryptoJS.enc.Utf8.parse(t), CryptoJS.enc.Utf8.parse(r), {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        return p.toString()
    },
    decrypt: function(t, r) {
        var p = CryptoJS.AES.decrypt(t, CryptoJS.enc.Utf8.parse(r), {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        })
          , e = CryptoJS.enc.Utf8.stringify(p).toString();
        return "{" !== e.charAt(0) && "[" !== e.charAt(0) || (e = JSON.parse(e)),
        e
    }
};

//
// console.log(aesUtil.encrypt(302517, "MWMqg2tPcDkxcm11"));


