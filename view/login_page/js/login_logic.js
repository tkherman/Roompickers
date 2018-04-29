var ADDR = "http://dsg1.crc.nd.edu";
var PORT = 5005;

function login_btn_clicked(){
    var netid = document.getElementById("netid_login").value;

    // set global variable DORM_NAME
    get_data(ADDR + ":" + PORT + "/signin/"+netid, gotoMainScreen);
}

function gotoMainScreen(data){
    var jsonData = JSON.parse(data);
    localStorage.dorm_name = jsonData["dorm_name"];

    var netid = document.getElementById("netid_login").value;
    localStorage.netid = netid;

    location.href = '../html/test.html';
}

var get_data = function(url, callback)
{
    var request = new XMLHttpRequest();
    request.onreadystatechange = function()
    {
        if (request.readyState === 4 && request.status == 200){
        	if(request.responseText == "{}"){
        		alert("NetID not in database");
        	}else{
        		callback(request.responseText);
        	}
        }
    }; 
    request.open('GET', url);
    request.send(null);
}