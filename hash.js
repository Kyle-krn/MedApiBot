
<script src="js/hmac-md5.js"></script>                        
<script src="js/enc-base64-min.js"></script>
<script>
    var uri = "https://authservice.priaid.ch/login";
    var secret_key = "mysecretkey";
    var computedHash = CryptoJS.HmacMD5(uri, secret_key);
    var computedHashString = computedHash.toString(CryptoJS.enc.Base64);     
</script>