function openClass(evt, className) {
  var i, x, tablinks;
  x = document.getElementsByClassName("class");
  for (i = 0; i < x.length; i++) {
	 x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < x.length; i++) {
	 tablinks[i].classList.remove("red");
  }
  document.getElementById(className).style.display = "block";
  evt.currentTarget.classList.add("red");
}
var mybtn = document.getElementsByClassName("testbtn")[0];
mybtn.click();		

$(document).ready(function() {
	var socket_1 = io.connect();
	var x = '離線中';		
	var status = '1';
	var lat = '';
	var lon = '';
	
	socket_1.on('server_response', function(msg) {
		var temp = msg.data.split(',');
		var station_no = temp[0];
		status = temp[1];
		
		if (status == "0"){
			x = '連線狀態:連線中'
			lat = temp[2];
			lon = temp[3];
			document.getElementById("coordinate_"+station_no).innerHTML='<tr><td><div>目前位置:'+lon+','+lat+'</div></td></tr>';
		}
		else if (status == "1"){
			x = '連線狀態:離線中'
			lat = '';
			lon = '';
			document.getElementById("coordinate_"+station_no).innerHTML='<tr><td><div>目前位置:</div></td></tr>';
		}						
		document.getElementById("connect_"+station_no).innerHTML='<tr><td><div>'+x+'</div></td></tr>';	
	});
});    

var myVar=setInterval(function(){connect()},10000);
var socket_2 = io.connect();
function connect(){
	socket_2.emit('client_event', {data: 'connect'});	
}

var myTime=setInterval(function(){clock()},1000);
function clock(){
	var d=new Date();
	var t=d.toLocaleTimeString();
	for (i = 1; i <= 6; i++) {
		document.getElementById("clock_"+i).innerHTML=t;
	}
}

var socket_3 = io.connect();	
function shutdown(station_no){	
	var r=confirm("警告!!\n關機後無法透過網頁開機\n是否繼續執行?");
	if (r==true){				
		socket_3.emit('client_event', {data: 'shutdown,'+station_no});
	}				
}