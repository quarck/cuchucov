#!/usr/bin/python3

import cgi
import cgitb
import os
import datetime 
import csv 
import fcntl 

cgitb.enable()

storage="/home/www-data/cov_log"

own_path = os.environ['REQUEST_URI'] if 'REQUEST_URI' in os.environ else ''
method = os.environ['REQUEST_METHOD'].upper() if 'REQUEST_METHOD' in os.environ else ''

print("Content-Type: text/html\r\n")
print("\r\n")


template="""
<!doctype html>
<html>
<head>
<title>CuChulainn Archers attendance record system</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,user-scalable=0,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0">
<style>
html {{
   font-family: 'Lato', sans-serif;
}}

h1 {{
    margin: 0px;
    padding: 0px;
    margin-bottom: 10px;
    padding-top: 10px;
    color: #000;
    font-size: 25px;
    font-weight: bold;
 }}
h2 {{
    margin: 0px;
    padding: 0px;
    margin-bottom: 10px;
    padding-top: 0px;
    color: #000;
    font-size: 18px;
    font-weight: bold;
 }}

.GDPRPanel {{
    position: fixed;
    bottom: -1px;
    left: 0;
    z-index: 400;
    display: "flex";
    flex-flow: row nowrap;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 65px;
    padding: 0 9px 0 12px;
    color: #fff;
    background: #000;
	font-size: 15px;
}}

body {{
	background: #feeb00; 
}}

#allow_cookies_div {{
	display: none;
}}

.dirbutton {{
    font-size: 18px;
    height:70px; 
    width:80%
}}

input {{
    font-size: 16px;
	width: 100%;
}}

</style>
</head>
<body onload="onload()">

<script language="JavaScript">
	function set_cookie(cname, cvalue, exdays) 
	{{
 		var d = new Date();
  		d.setTime(d.getTime() + (exdays*24*60*60*1000));
  		var expires = "expires="+ d.toUTCString();
  		document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
	}}

	function get_cookie(cname) 
	{{
		var name = cname + "=";
  		var decodedCookie = decodeURIComponent(document.cookie);
  		var ca = decodedCookie.split(';');
  		for(var i = 0; i <ca.length; i++) 
		{{
    		var c = ca[i];
    		while (c.charAt(0) == ' ') 
			{{
      			c = c.substring(1);
    		}}
    		if (c.indexOf(name) == 0) 
			{{
      			return c.substring(name.length, c.length);
    		}}
  		}}
  		return "";
	}}


	function on_allow_cookies()
	{{
	    set_cookie('allow_cookies','1', 500);
		document.getElementById('allow_cookies_div').style.display = 'none'
	}}

	function submit(direction)
	{{
		var name = document.getElementById('name').value
		var phone = document.getElementById('phone').value
		var date = new Date()
		var datetime = date.toLocaleDateString() + " " + date.toLocaleTimeString()

		if (get_cookie('allow_cookies') == '1')
		{{
			set_cookie('name', window.escape(name), 500)
			set_cookie('phone', window.escape(phone), 500)
			set_cookie('last_change', direction + ' at ' + datetime, 500)
		}}

		document.getElementById('datetime').value = datetime
		document.getElementById('direction').value = direction

		document.getElementById('form').submit();
	}}

	function onload()
	{{

		if ( window.history.replaceState ) 
		{{
			window.history.replaceState( null, null, window.location.href );
		}}

		if (get_cookie('allow_cookies') != "1")
		{{
			document.getElementById('allow_cookies_div').style.display = 'flex'
		}}

		if (!document.getElementById('status'))
		{{
			var last_change = get_cookie("last_change")
			if (last_change != "")
			{{
				var el = document.getElementById('last_update_text')
				el.innerText = "Last status change: " + last_change
				el.style.display = "block"
			}}
		}}
		
		var name = document.getElementById('name')
		var ck_name = get_cookie('name')
		if (name.value == "" && ck_name != "")
		{{
			name.value = ck_name
		}}
		var phone = document.getElementById('phone')
		var ck_phone = get_cookie('phone')
		if (phone.value == "" && ck_phone != "")
		{{
			phone.value = ck_phone
		}}
	}}

</script>

<div id="allow_cookies_div" class="GDPRPanel">
<p>This website uses cookies to remember your name and phone number.
<button onclick="on_allow_cookies()">&nbsp;&nbsp;OK&nbsp;&nbsp;</button></p>
</div>

<h1 id="header">CuChulainn Archers </h1>
<h2 id="header2">Attendance Record Keeping System</h2>

{status}
<p id="last_update_text" style="display: none"></p>

<form action="{own_path}" method="post" id="form">
<input type="hidden" name="dir" id="direction" value="U"/> <!-- U - unknown, A - arrived, D - departing -->
<input type="hidden" name="dt" id="datetime" value=""/> <!-- client date time -->
<table width="100%" border="0px" cellspacing="10px">

<tr><td><label for="archer_name">Name:</label></td> <td><input type="text" id="name" name="name" placeholder="Your Real Name" value="{name}"/></td></tr>

<tr><td><label for="phone">Mobile:</label></td> <td><input type="tel" id="phone" name="phone" placeholder="Your Mobile Phone" value="{phone}"/></td></tr>
</table>
<p>By clicking either button below you are agreeing for your input being recorded for contract tracing purposes</p>
</form>
<p align="center">
<button id="btn_arrived" class="dirbutton" onclick="submit('Arrival')">Arrived</button>
</p>
<p align="center">
<button id="btn_departing" class="dirbutton" onclick="submit('Departure')">Departing</button>
</p>

<p align="center">
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   version="1.1"
   id="Layer_1"
   x="0px"
   y="0px"
   viewBox="0 0 3001 1601"
   enable-background="new 0 0 1072.551 1663.835"
   xml:space="preserve"
   sodipodi:docname="corona_shoot.svg"
   width="50%"
   inkscape:version="0.92.4 (5da689c313, 2019-01-14)"><metadata
   id="metadata4557"><rdf:RDF><cc:Work
       rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type
         rdf:resource="http://purl.org/dc/dcmitype/StillImage" /><dc:title></dc:title></cc:Work></rdf:RDF></metadata><defs
   id="defs4555" /><sodipodi:namedview
   pagecolor="#ffffff"
   bordercolor="#666666"
   borderopacity="1"
   objecttolerance="10"
   gridtolerance="10"
   guidetolerance="10"
   inkscape:pageopacity="0"
   inkscape:pageshadow="2"
   inkscape:window-width="1920"
   inkscape:window-height="1001"
   id="namedview4553"
   showgrid="false"
   inkscape:zoom="0.24792122"
   inkscape:cx="872.7869"
   inkscape:cy="672.50564"
   inkscape:window-x="-9"
   inkscape:window-y="-9"
   inkscape:window-maximized="1"
   inkscape:current-layer="Layer_1" />
<path
   d="m 780.26551,4.1196181 c 3.532,-6.139 7.055,-4.441 7.14,-1.197 0.115,5.085 -2.118,10.1159999 -1.049,15.1969999 0.611,0.632 1.163,1.324 1.681,2.046 5.752,1.388 7.543,9.738 3.4,13.703 2.29,3.266 -0.583,5.334 1.303,8.855 10.605,18.993 8.906,12.964 15.787,22.443 4.257,5.83 2.013,10.111 2.021,14.153 0.064,1.371 2.28,1.133 2.538,2.445 0.45,2.313 1.01,4.945 -0.743,6.873 0.28,0.475 0.573,0.951 0.879,1.426 -0.153,0.267 -0.463,0.802 -0.62,1.07 6.933,18.687002 10.849,15.191002 22.371,34.571002 3.365,5.708 8.794,7.221 13.698,17.26 4.669,9.565 5.753,8.656 13.664,14 8.058,5.372 7.486,10.02 11.321,14.552 4.779,5.728 9.251,6.192 14,13.979 6.022,9.936 38.716,48.969 44.818,109.965 3.308,42.538 0.188,56.585 0.501,65.72 3.635,0.297 5.42,6.159 -0.972,7.891 -0.047,3.12 0.068,6.393 -1.244,9.309 8.123,0.984 -2.703,19.289 -4.19,29.999 45.185,11.622 55.578,13.858 58.045,16.797 -5.388,1.729 -10.296,1.798 -55.995,3.46 8.461,4.934 16.538,8.3 13.427,15.808 -0.976,2.275 -3.337,3.536 -5.612,4.181 7.194,3.972 7.221,9.072 4.444,12.866 -3.201,4.24 -9.257,2.757 -10.723,2.598 7.158,4.863 4.157,14.753 -4.156,14.446 3.303,1.651 3.736,6.427 1.566,9.169 -3.447,5.003 -12.102,1.336 -14.144,0.807 -3.864,20.021 3.188,29.271 -5.939,34.278 0.013,2.454 -1.032,4.733 -1.384,7.106 6.02,7.831 -1.367,9.158 -2.415,9.857 -6.695,11.675 -6.901,77.896 -90.387,141.806 -3.54,2.526 -6.643,5.629 -10.311,7.985 -3.324,2.139 -7.327,2.717 -10.863,4.389 -5.841,2.579 -8.021,8.682 -16.037,10.782 -7.432,2.19 -6.904,-1.017 -16.152,7.985 -7.892,7.759 -12.399,7.226 -16.988,11.02 -17.457,14.348 -19.114,10.815 -28.458,22.464 -0.047,0.9 -0.348,1.757 -0.828,2.521 0.386,2.364 -1.015,4.453 -2.046,6.457 -0.539,1.218 -1.863,1.592 -2.92,2.199 -3.435,15.544 -6.132,7.631 -27.431,26.459 0.734,2.161 -0.301,4.5 -2.182,5.68 3.539,5.429 -1.252,13.158 -8.269,11.954 -2.122,4.402 -1.626,9.492 -3.362,14.008 -1.143,3.449 -6.336,3.379 -6.834,-5.136 0.17,-6.851 1.736,-13.826 5.51,-19.629 -1.412,-1.527 -236.532,-279.716 -236.532,-279.716 -35.695,85.915 -41.658,83.221 -54.144,130.544 11.746,9.124 10.459,9.496 11.962,11.733 -0.505,6.82 1.502,4.427 -2.369,8.885 -1.053,-0.318 -2.05,-0.785 -3.001,-1.329 0.467,1.83 1.316,3.621 1.112,5.561 -1.579,19.299 -6.759,36.303 0.849,102.787 6.05,51.831 10.832,73.211 11.444,89.577 0.57,7.324 -2.545,-3.977 15.426,32.389 19.821,40.39 60.118,144.16798 77.275,188.36898 31.913,90.472 48.763,112.839 68.004,147.719 47.784,84.957 54.563,87.542 53.626,97.634 0.144,0.216 0.433,0.654 0.577,0.874 -1.808,3.837 -13.752,11.204 -14.908,12.034 -2.551,1.8 -4.241,4.559 -6.86,6.278 -1.27,0.851 -13.729,8.843 -16.445,9.216 -0.31,-1.265 -0.756,-2.475 -1.184,-3.68 -6.373,3.06 -2.72,-6.452 -26.624,9.572 1.118,3.875 4.785,1.522 2.768,10.133 -0.794,2.734 0.238,5.518 0.463,8.269 0.004,1.557 6.002,5.948 2.793,9.25 0.076,2.027 0.982,9.35 2.488,10.515 5.28,4.503 2.218,5.698 2.611,7.513 0.2,1.108 0.17,2.254 -0.48,3.239 0.458,1.906 0.658,3.901 1.341,5.756 1.265,1.176 2.942,2.394 2.674,4.377 -0.331,2.335 1.63,4.394 0.781,6.72 0.391,1.227 0.828,2.449 1.286,3.676 1.129,0.777 2.475,1.511 2.954,2.904 0.458,1.35 1.656,2.564 1.252,4.096 -0.318,1.282 0.633,2.356 0.993,3.536 0.586,1.248 -0.14,2.785 0.683,3.973 0.688,0.874 1.605,1.605 1.982,2.713 0.556,1.558 2.39,2.428 2.441,4.219 0.489,5.135 3.222,6.378 1.061,9.224 0.484,2.296 2.628,3.74 3.056,6.036 0.14,0.522 0.357,1.032 0.582,1.562 2.413,0.355 4.711,4.747 2.432,7.08 22.819,60.505 7.871,29.522 55.316,86.949 5.898,6.979 5.866,11.396 6.669,14.327 1.753,6.315 0.642,9.209 -3.048,13.83 -6.849,8.347 -13.316,9.069 -25.236,9.543 -61.448,1.544 -55.909,-22.45 -57.57,-31.786 -8.764,1.684 -9.862,-2.116 -12.552,-4.177 -8.271,-6.608 -2.433,-11.535 -7.221,-24.302 0,-10e-4 -7.929,-28.093 -7.93,-28.093 -5.232,-15.351 -3.099,-19.202 -5.722,-29.146 -1.834,-7.208 -5.79,-13.601 -8.244,-20.579 -6.866,-18.585 -3.501,-14.458 -22.625,-59.849 -28.053,16.44 -26.706,11.251 -27.876,8.146 -4.471,-16.081 -24.751,-74.023 -27.159,-80.836 -15.485,-3.164 -30.251,-6.939 -36.562,-18.453 -32.201,-58.281 -52.75,-206.504 -140.219,-380.93198 -15.834,78.72098 -21.08,155.08598 -34.541,226.40798 -13.948,74.511 -15.103,116.079 -21.951,183.05 -7.388,74.486 -5.66,75.113 -8.893,76.239 -2.977,0.457 -16.232,-3.86 -22.889,-10.417 -1.286,-1.291 -2.679,-2.458 -4.135,-3.536 -2.229,-1.672 -3.171,-4.419 -5.035,-6.406 -2.182,-2.335 -4.41,-4.635 -6.898,-6.635 -19.276,108.406 -16.099,109.583 -20.516,143.886 -0.07,0.407 -2.992,20.749 -2.971,21.161 0.316,23.807 -2.896,15.883 -17.29,22.901 -4.608,2.129 -8.531,1.08 -19.2,-0.539 -2.598,3.222 -4.669,6.89 -7.751,9.712 -18.113,17.745 -75.059,17.401 -82.458,14.123 -4.66500005,-2.051 -4.45000005,-9.762 -3.27300005,-12.786 2.69500005,-13.402 5.39500005,-14.507 28.64100005,-35.118 1.392,-1.452 3.277,-2.381 4.423,-4.054 1.689,-2.403 4.219,-3.973 6.444,-5.811 14.886,-11.711 31.138,-35.907 34.371,-42.916 10.619,-23.06 3.058,-36.46 10.795,-74.97 0.654,-3.112 0.934,-6.278 1.18,-9.432 -2.748,-3.149 0.603,-6.073 0.649,-7.178 1.396,-18.521 1.249,-40.991 1.269,-41.991 -11.511,-4.516 -33.701,-16.476 -38.141,-18.228 -1.452,2.882 -2.335,5.994 -3.366,9.046 -6.572,-1.208 -31.887,-14.195 -31.85,-26.879 0.529,-26.823 9.986,-38.832 32.058,-122.713 12.622,-51.118 17.358,-91.427 22.418,-118.064 18.815,-110.46998 22.184,-102.50298 36.001,-163.58698 16.731,-66.744 4.428,-143.429 68.407,-245.684 3.937,-6.043 10.876,-15.456 10.876,-15.456 -0.904,0.505 -1.876,0.887 -2.904,1.049 -2.924,-5.666 -3.606,-20.697 2.33,-34.24 0.84,-1.974 3.188,-2.445 4.406,-4.101 0.645,-0.891 1.634,-1.38 2.738,-1.32 0.934,-1.112 1.914,-2.258 3.311,-2.789 4.399,-1.797 4.14,-4.207 6.223,0.25 19.904,-44.055 4.718,-41.485 10.239,-96.869 7.239,-60.295 18.816,-68.809 21.046,-79.86 0.754,-5.596 3.174,-6.149 1.931,-9.581 -3.408,-7.383 -3.14,-8.769 -7.339,-10.43 -7.541,-3.998 -8.4,-7.673 -31.251,-15.885 -53.421,-20.1 -116.632,-23.278 -132.663,-26.73 -27.788,-5.511 -66.671,-24.031 -50.396,-50.23 -3.349,-3.294 -6.1,-7.11 -9.144,-10.672 -1.583,-1.872 -2.64000005,-4.292 -2.50500005,-6.771 0.10500005,-2.26 4.08700005,-9.206 5.42100005,-10.319 3.691,-3.808 43.267,-1.522 50.201,-0.352 20.654,3.507 13.772,1.884 27.172,2.729 20.147,0.95 27.379,12.923 65.571,17.816 10.682,1.156 53.323,6.596 63.453,3.68 6.762,-1.899 10.555,-6.251 17.892,-3.515 -7.77,-4.722 -6.161,-2.464 -11.478,-9.301 0.408,-2.734 1.099,-5.501 2.649,-7.828 9.775,-15.52 -5.655,-10.563 -2.878,-60.414 0.574,-21.955 2.661,-20.565 4.207,-26.803 4.048,-22.594 4.738,-75.601 46.142,-103.453 9.576,-5.899 19.405,-11.336 28.585,-13.393 28.356,-7.517002 57.871,2.195 72.38,17.2 10.457,10.211 7.765,9.279 20.889,23.194 17.55,18.585 5.989,5.507 15.978,19.688 14.239,26.316 24.611,17.567 21.153,82.734 0.552,2.865 1.337,5.718 1.231,8.672 3.326,-2.274 345.671,-222.816002 347.872,-224.710002 -1.991,-10.952 0.219,-21.3549999 2.914,-26.0289999 m -9.458,34.2949999 c -10e-4,0 -340.596,219.806002 -340.597,219.807002 0,0 11.336,35.154 8.044,72.941 6.788,1.169 8.219,1.228 11.716,8.006 1.805,4.343 7.859,10.891 8.112,15.672 4.024,0.475 8.184,2.925 9.088,7.14 2,0.466 415.63,48.277 422.082,48.902 0.119,-0.259 0.348,-0.781 0.463,-1.04 0.692,0.136 1.422,0.289 2.135,0.454 1.923,-3.179 3.782,-6.401 5.85,-9.487 1.638,0.403 3.269,0.874 4.903,1.346 0.549,-15.02 -2.291,-24.422 4.355,-26.611 -0.034,-2.458 0.552,-4.856 1.24,-7.195 -5.387,-4.434 -2.503,-8.442 1.091,-9.05 3.296,-4.549 4.705,-28.592 5.302,-36.68 3.139,-35.961 2.292,-27.32 -2.623,-39.626 -6.241,-15.085 -15.174,-51.427 -15.176,-51.432 -16.584,-37.929 -48.873,-66.228 -57.54,-78.739 -10.997,-15.955 -25.098,-37.997 -52.306,-64.447002 0.233,-0.577 0.484,-1.155 0.739,-1.732 -0.768,-0.722 -1.732,-1.286 -2.245,-2.216 -0.558,-7.017 1.456,-7.525 2.483,-8.507 2.48,-2.525 2.761,1.479 5.625,-6.372 3.125,-9.723 -3.665,-9.122 -11.19,-24.875 -1.401,-2.628 -1.991,-5.608 -3.379,-8.231 -0.208,-1.006 -0.45,-2.008 -0.713,-2.997 -2.603,1.48 -4.904,3.424 -7.459,4.969 m -304.222,330.884002 c 6.225,4.665 15.114,0.374 17.583,11.758 69.966,27.141 121.487,33.003 195.602,31.561 3.595,-1.183 0.982,-2.957 10.918,-3.999 29.456,4.72 124.522,26.375 145.928,14.008 5.946,-3.378 11.679,-3.453 18.253,-1.541 5.227,-7.719 11.086,-2.853 13.694,-3.719 1.804,-0.475 3.659,-0.734 5.531,-0.777 -26.801,-3.078 -401.522,-46.776 -407.509,-47.291 m -8.88,88.299 c -23.348,9.811 -13.019,27.128 -23.492,40.573 -1.762,2.39 -0.892,-0.076 -3.303,9.441 0.713,1.077 231.337,273.798 237.063,280.28 11.674,-15.87 17.752,-17.965 21.925,-21.717 1.206,-2.318 0.666,-5.128 0.289,-7.603 -0.156,-1.517 -5.291,-4.002 -4.071,-7.301 0.565,-2.292 0.501,-5.128 2.636,-6.622 0.972,-0.756 1.401,-1.978 2.339,-2.763 0.434,-0.395 11.549,-7.163 15.91,-9.139 27.278,-12.493 43.373,-31.88 66.637,-42.87 1.519,-0.714 32.35,-18.146 50.595,-35.972 13.411,-13.545 6.723,-5.516 18.376,-22.817 33.557,-50.633 20.438,-15.32 31.93,-58.865 1.421,-5.293 8.072,-31.539 6.461,-36.57 0.068,-0.204 0.208,-0.611 0.28,-0.815 -2.921,-0.857 -5.662,-5.352 1.516,-9.22 0.072,-2.301 0.365,-4.589 1.031,-6.796 -6.888,-5.594 4.449,-18.521 5.548,-34.133 -5.404,-0.255 -10.842,-0.857 -15.986,-2.619 -1.758,-0.895 -6.303,3.693 -10.523,0.331 -1.804,-1.639 -4.287,-2.139 -6.58,-2.666 -1.19,0.381 -9.371,4.126 -14.225,3.192 -9.527,-1.209 -15.564,-8.661 -26.484,-9.976 -34.094,-4.301 -88.694,1.325 -96.793,4.75 -0.777,0.042 -1.549,0.081 -2.305,0.119 l 0.017,0.306 c -3.434,0.433 -6.66,1.863 -10.078,2.42 -13.09,2.11 -12.85,0.89 -15.333,-4.062 -59.101,1.826 -204.678,-31.363 -233.38,-18.886 m -268.832,196.103 c 0.246,0.976 0.548,1.944 0.887,2.904 0.492,-0.819 0.972,-1.634 1.456,-2.449 -0.365,0.026 -1.095,0.076 -1.46,0.098 -0.221,-0.137 -0.662,-0.412 -0.883,-0.553 z"
   id="path4550"
   inkscape:connector-curvature="0" />
<path
   inkscape:connector-curvature="0"
   d="m 2742.9429,433.12917 c -5.9119,0.83827 -10.0625,6.33101 -9.2242,12.24266 0.8372,5.91166 6.3316,10.06242 12.2434,9.22383 h 10.7333 v 22.13732 c -19.9574,1.04863 -39.3277,4.65393 -57.3563,11.06865 l -4.025,-10.73324 4.6958,-2.01248 c 5.0317,-2.13817 7.6732,-7.67255 6.1212,-12.91338 -1.551,-5.24083 -6.792,-8.51114 -12.1587,-7.54687 -0.923,0.2093 -1.845,0.54525 -2.6833,1.00571 l -29.1804,12.74572 c -5.4504,2.38987 -7.9663,8.8047 -5.5352,14.25515 2.3903,5.45045 8.8056,7.92414 14.2559,5.53427 l 4.6958,-2.01248 4.025,10.06242 c -17.7356,8.51114 -33.8355,19.53793 -48.2996,32.53514 l -15.4291,-15.76445 7.714,-7.71452 c 3.3542,-3.18638 4.3191,-8.17562 2.3485,-12.36835 -2.0125,-4.23458 -6.4572,-6.66631 -11.0692,-6.07941 -2.3893,0.25115 -4.654,1.34165 -6.3724,3.01872 l -31.194,31.19349 c -4.1505,4.27656 -4.1087,11.11063 0.1717,15.26139 4.2772,4.15076 11.1111,4.10879 15.2616,-0.16744 l 7.7151,-7.71452 15.7639,15.42904 c -12.9969,14.46476 -24.0242,30.56463 -32.5346,48.2996 l -10.0624,-4.02497 2.0125,-4.6958 c 1.7184,-3.52179 1.4253,-7.67255 -0.7943,-10.90089 -2.2636,-3.18649 -6.0374,-4.94738 -9.9358,-4.52814 -0.4615,0.0859 -0.923,0.20929 -1.3416,0.33487 -3.4808,0.71269 -6.3316,3.10266 -7.7151,6.37287 l -12.7457,29.181 c -2.1381,3.56387 -2.0125,8.00808 0.2576,11.44604 2.3055,3.43797 6.3723,5.2828 10.481,4.6958 4.0668,-0.58711 7.5047,-3.47994 8.7208,-7.42108 l 2.0125,-4.69579 10.7332,4.02497 c -6.4142,18.02852 -10.0206,37.3987 -11.0681,57.35577 h -22.1373 v -10.73324 c 0.1288,-3.10256 -1.1324,-6.07931 -3.3542,-8.17562 -2.2647,-2.13828 -5.3247,-3.18649 -8.3859,-2.89304 -0.4615,0.0859 -0.923,0.2093 -1.3416,0.33488 -4.9888,1.13203 -8.5115,5.6182 -8.3848,10.73324 v 42.93298 c 0,3.85731 1.9706,7.46303 5.3247,9.43355 3.3542,1.92866 7.4629,1.92866 10.817,0 3.3541,-1.97052 5.3666,-5.57624 5.3248,-9.43355 v -10.73325 h 22.1373 c 1.0518,19.95718 4.6539,39.32736 11.0681,57.35577 l -10.7332,4.02497 -2.0125,-4.69579 c -1.8869,-4.31842 -6.3724,-6.9179 -11.0681,-6.37287 -3.396,0.41967 -6.3316,2.47369 -8.0081,5.45056 -1.6358,2.97676 -1.8032,6.54052 -0.3757,9.64307 l 12.7457,29.181 c 2.3903,5.45056 8.8045,7.96611 14.2549,5.53439 5.4514,-2.38987 7.9243,-8.80459 5.5351,-14.25515 l -2.0125,-4.69579 10.0624,-4.02497 c 8.4686,17.65125 19.2437,33.8768 32.1998,48.2996 l -15.4291,15.42904 -7.715,-7.71452 c -2.3055,-2.47358 -5.6597,-3.73141 -9.0557,-3.35414 -4.1934,0.41967 -7.7569,3.22845 -9.0985,7.16949 -1.3836,3.9831 -0.2898,8.38534 2.7251,11.27827 l 31.1941,31.19349 c 4.2761,4.15076 11.1099,4.1089 15.2605,-0.16743 4.1516,-4.27645 4.1097,-11.11052 -0.1717,-15.26128 l -7.714,-7.71452 15.429,-15.42904 c 14.4223,12.95546 30.6477,23.73056 48.2996,32.19973 l -4.025,10.06242 -4.6958,-2.01248 c -1.552,-0.75455 -3.3122,-1.09007 -5.0317,-1.00571 -5.1992,0.0429 -9.6009,3.77349 -10.5239,8.84656 -0.8802,5.11514 1.9706,10.14635 6.8349,11.9491 l 29.1805,12.74573 c 3.5634,2.13828 8.008,2.01248 11.4459,-0.25116 3.4378,-2.30593 5.2829,-6.37286 4.6958,-10.48166 -0.5903,-4.06682 -3.4797,-7.5049 -7.421,-8.72076 l -4.6958,-2.01248 4.025,-10.73324 c 18.0286,6.41483 37.3989,10.02055 57.3563,11.06865 v 22.13732 h -10.7332 c -0.3328,0 -0.6655,0 -1.009,0 -0.3327,0 -0.6654,0 -1.0089,0 -5.9119,0.54525 -10.2728,5.82783 -9.7275,11.73948 0.5474,5.91177 5.8281,10.27215 11.74,9.72701 h 42.933 c 3.8564,0.0429 7.4628,-1.97052 9.4334,-5.32466 1.9288,-3.35414 1.9288,-7.46293 0,-10.81707 -1.9706,-3.35414 -5.577,-5.36662 -9.4334,-5.32476 h -10.7333 v -22.13732 c 19.9563,-1.04863 39.3266,-4.65382 57.3553,-11.06865 l 4.0249,10.73324 -4.6958,2.01248 c -3.9412,1.21597 -6.8338,4.65394 -7.4209,8.72076 -0.5904,4.1089 1.2579,8.17573 4.6958,10.48177 3.4378,2.26396 7.8825,2.38975 11.4459,0.25116 l 29.1815,-12.74573 c 5.2829,-1.7609 8.3848,-7.29528 7.0432,-12.70387 -1.2998,-5.45045 -6.5409,-8.97224 -12.0749,-8.09179 -1.2998,0.12558 -2.5159,0.46153 -3.689,1.0057 l -4.6958,2.01249 -4.025,-10.06242 c 17.7345,-8.51114 33.8344,-19.53783 48.2996,-32.53515 l 15.429,15.76446 -7.715,7.71452 c -4.2761,4.15076 -4.318,10.98483 -0.1717,15.26127 4.1505,4.27656 10.9844,4.31852 15.2616,0.16744 l 31.1929,-31.19349 c 3.4797,-3.22834 4.4028,-8.34338 2.3066,-12.57797 -2.0554,-4.27655 -6.7083,-6.62445 -11.3622,-5.86979 -2.4322,0.33488 -4.6958,1.55127 -6.3734,3.35414 l -7.714,7.71452 -15.765,-15.42904 c 12.998,-14.46477 24.0242,-30.56463 32.5357,-48.2996 l 10.0624,4.02497 -2.0125,4.69579 c -2.3903,5.45045 0.1074,11.86528 5.5341,14.25504 5.4503,2.43183 11.8656,-0.0859 14.2548,-5.53428 l 12.7457,-29.18101 c 1.551,-3.47993 1.1742,-7.50489 -1.0518,-10.60745 -2.2229,-3.10266 -5.87,-4.82158 -9.6857,-4.48617 -0.3327,0 -0.6655,0 -1.0089,0 -3.4808,0.71269 -6.3316,3.10255 -7.7151,6.37286 l -2.0125,4.6958 -10.7332,-4.02497 c 6.4152,-18.02852 10.0205,-37.3987 11.0692,-57.35577 h 22.1373 v 10.73324 c 0,3.85721 1.9706,7.46293 5.3248,9.43345 3.3541,1.92866 7.4628,1.92866 10.8169,0 3.3542,-1.97052 5.3666,-5.57624 5.3248,-9.43345 v -42.93297 c 0.1288,-3.10255 -1.1324,-6.07942 -3.3542,-8.17573 -2.2647,-2.13828 -5.3247,-3.18649 -8.3858,-2.89293 -0.4616,0.0859 -0.9231,0.2093 -1.3417,0.33488 -4.9888,1.13203 -8.5115,5.61821 -8.3848,10.73324 v 10.73324 h -22.1373 c -1.0519,-19.95718 -4.654,-39.32725 -11.0692,-57.35577 l 10.7332,-4.02497 2.0125,4.6958 c 1.2161,3.94114 4.6539,6.83407 8.7208,7.42096 4.1087,0.58711 8.1755,-1.25772 10.4821,-4.69579 2.2636,-3.43797 2.3892,-7.88217 0.2468,-11.44593 l -12.7457,-29.18101 c -1.9288,-4.44421 -6.5827,-7.08566 -11.4041,-6.37286 -3.396,0.41967 -6.3304,2.47369 -8.0081,5.45045 -1.6346,2.97675 -1.8021,6.54062 -0.3756,9.64317 l 2.0125,4.6958 -10.0624,4.02496 c -8.4697,-17.65114 -19.2448,-33.8768 -32.1998,-48.2996 l 15.4291,-15.42903 7.7139,7.71452 c 4.1506,4.27655 10.9855,4.31841 15.2616,0.16743 4.2762,-4.15076 4.318,-10.98483 0.1718,-15.26138 l -31.193,-31.19349 c -2.0125,-2.13828 -4.7795,-3.31228 -7.715,-3.35414 -0.6655,0.0429 -1.3417,0.16744 -2.0125,0.33488 -4.025,0.71268 -7.2535,3.64758 -8.3848,7.54676 -1.1324,3.94114 0,8.13386 3.0182,10.901 l 7.715,7.71452 -15.429,15.42904 c -14.4234,-12.95535 -30.6488,-23.73056 -48.2996,-32.19973 l 4.0249,-10.06242 4.6958,2.01248 c 5.4504,2.38976 11.8646,-0.0859 14.2549,-5.53438 2.4321,-5.45045 -0.1074,-11.86528 -5.5341,-14.25504 l -29.1815,-12.74572 c -1.8869,-0.92199 -3.9832,-1.25783 -6.0375,-1.00571 -4.7376,0.71269 -8.4267,4.48618 -9.0556,9.22383 -0.6333,4.73776 1.9706,9.30776 6.3723,11.23642 l 4.6958,2.01248 -4.025,10.73325 c -18.0286,-6.41484 -37.3989,-10.02056 -57.3552,-11.06866 v -22.13732 h 10.7332 c 3.8565,0.0429 7.4629,-1.97062 9.4335,-5.32476 1.9287,-3.35414 1.9287,-7.46293 0,-10.81707 -1.9706,-3.35414 -5.577,-5.36662 -9.4335,-5.32466 h -42.9329 c -0.3328,0 -0.6655,0 -1.009,0 -0.3327,0 -0.6654,0 -1.0089,0 -0.3327,0 -0.6655,0 -1.0089,0 z m 24.4857,64.39947 c 100.9172,0 182.4652,81.54754 182.4652,182.46515 0,100.91771 -81.548,182.46514 -182.4652,182.46514 -100.9182,0 -182.4651,-81.54743 -182.4651,-182.46514 0,-100.91761 81.5469,-182.46515 182.4651,-182.46515 z m 0,32.19973 c -17.6519,0 -32.1997,14.54859 -32.1997,32.19973 0,17.65125 14.5478,32.19973 32.1997,32.19973 17.6508,0 32.1997,-14.54848 32.1997,-32.19973 0,-17.65114 -14.5489,-32.19973 -32.1997,-32.19973 z m 0,21.46649 c 6.0375,0 10.7333,4.69579 10.7333,10.73324 0,6.03745 -4.6958,10.73325 -10.7333,10.73325 -6.0374,0 -10.7332,-4.6958 -10.7332,-10.73325 0,-6.03745 4.6958,-10.73324 10.7332,-10.73324 z m -76.1395,20.46024 c -17.6508,0 -32.1997,14.54859 -32.1997,32.19974 0,17.65124 14.5489,32.19973 32.1997,32.19973 17.6508,0 32.1998,-14.54849 32.1998,-32.19973 0,-17.65115 -14.549,-32.19974 -32.1998,-32.19974 z m 152.2779,0 c -17.6508,0 -32.1997,14.54859 -32.1997,32.19974 0,17.65124 14.5489,32.19973 32.1997,32.19973 17.6508,0 32.1998,-14.54849 32.1998,-32.19973 0,-17.65115 -14.549,-32.19974 -32.1998,-32.19974 z m -152.2779,21.46649 c 6.0375,0 10.7333,4.6958 10.7333,10.73325 0,6.03745 -4.6958,10.73324 -10.7333,10.73324 -6.0374,0 -10.7332,-4.69579 -10.7332,-10.73324 0,-6.03745 4.6958,-10.73325 10.7332,-10.73325 z m 152.2779,0 c 6.0375,0 10.7333,4.6958 10.7333,10.73325 0,6.03745 -4.6958,10.73324 -10.7333,10.73324 -6.0374,0 -10.7332,-4.69579 -10.7332,-10.73324 0,-6.03745 4.6958,-10.73325 10.7332,-10.73325 z m -194.2041,54.67246 c -17.6519,0 -32.1997,14.54859 -32.1997,32.19974 0,17.65124 14.5478,32.19973 32.1997,32.19973 17.6508,0 32.1998,-14.54849 32.1998,-32.19973 0,-17.65115 -14.549,-32.19974 -32.1998,-32.19974 z m 118.0657,0 c -17.6519,0 -32.1997,14.54859 -32.1997,32.19974 0,17.65124 14.5478,32.19973 32.1997,32.19973 17.6508,0 32.1997,-14.54849 32.1997,-32.19973 0,-17.65115 -14.5489,-32.19974 -32.1997,-32.19974 z m 118.0657,0 c -17.6519,0 -32.1997,14.54859 -32.1997,32.19974 0,17.65124 14.5478,32.19973 32.1997,32.19973 17.6508,0 32.1997,-14.54849 32.1997,-32.19973 0,-17.65115 -14.5489,-32.19974 -32.1997,-32.19974 z m -236.1314,21.46649 c 6.0375,0 10.7333,4.6958 10.7333,10.73325 0,6.03744 -4.6958,10.73324 -10.7333,10.73324 -6.0374,0 -10.7332,-4.6958 -10.7332,-10.73324 0,-6.03745 4.6958,-10.73325 10.7332,-10.73325 z m 118.0657,0 c 6.0375,0 10.7333,4.6958 10.7333,10.73325 0,6.03744 -4.6958,10.73324 -10.7333,10.73324 -6.0374,0 -10.7332,-4.6958 -10.7332,-10.73324 0,-6.03745 4.6958,-10.73325 10.7332,-10.73325 z m 118.0657,0 c 6.0374,0 10.7332,4.6958 10.7332,10.73325 0,6.03744 -4.6958,10.73324 -10.7332,10.73324 -6.0375,0 -10.7333,-4.6958 -10.7333,-10.73324 0,-6.03745 4.6958,-10.73325 10.7333,-10.73325 z M 2691.2891,723.933 c -17.6508,0 -32.1997,14.54859 -32.1997,32.19973 0,17.65125 14.5489,32.19974 32.1997,32.19974 17.6508,0 32.1998,-14.54849 32.1998,-32.19974 0,-17.65114 -14.549,-32.19973 -32.1998,-32.19973 z m 152.2779,0 c -17.6508,0 -32.1997,14.54859 -32.1997,32.19973 0,17.65125 14.5489,32.19974 32.1997,32.19974 17.6508,0 32.1998,-14.54849 32.1998,-32.19974 0,-17.65114 -14.549,-32.19973 -32.1998,-32.19973 z m -152.2779,21.46649 c 6.0375,0 10.7333,4.6958 10.7333,10.73324 0,6.03745 -4.6958,10.73325 -10.7333,10.73325 -6.0374,0 -10.7332,-4.6958 -10.7332,-10.73325 0,-6.03744 4.6958,-10.73324 10.7332,-10.73324 z m 152.2779,0 c 6.0375,0 10.7333,4.6958 10.7333,10.73324 0,6.03745 -4.6958,10.73325 -10.7333,10.73325 -6.0374,0 -10.7332,-4.6958 -10.7332,-10.73325 0,-6.03744 4.6958,-10.73324 10.7332,-10.73324 z m -76.1384,20.46025 c -17.6519,0 -32.1997,14.54859 -32.1997,32.19973 0,17.65125 14.5478,32.19973 32.1997,32.19973 17.6508,0 32.1997,-14.54848 32.1997,-32.19973 0,-17.65114 -14.5489,-32.19973 -32.1997,-32.19973 z m 0,21.46649 c 6.0375,0 10.7333,4.69579 10.7333,10.73324 0,6.03745 -4.6958,10.73324 -10.7333,10.73324 -6.0374,0 -10.7332,-4.69579 -10.7332,-10.73324 0,-6.03745 4.6958,-10.73324 10.7332,-10.73324 z"
   id="path5206"
   style="stroke-width:1" />
</svg>
</p>

</body>
</html>
"""

form = cgi.FieldStorage()

def print_response(status="", name="", phone=""):
	html = template.format(
			status=status,
			own_path=own_path,
			name = name, 
			phone = phone
		)
	print(html)


if method == "GET": 
	print_response(status="")
	exit(0)

if method != "POST":
	print_response(status="<p id='status' color='red'>Invalid request method</p>")
	exit(0)
	

name = form["name"].value if "name" in form else ""
phone = form["phone"].value if "phone" in form else ""
client_time = form["dt"].value if "dt" in form else ""
direction = form["dir"].value if "dir" in form else ""

server_time = datetime.datetime.now()


if name == "" or phone == "" or client_time == "" or direction == "": 
	print_response(status="<p id='status' style=\"color: #ff0000;\">Name and Phone are mandatory</p>", name=name, phone=phone)
	exit(0)

todays_file = storage + "/log_" + server_time.strftime("%Y%m%d") + ".csv"

new_file = not os.path.exists(todays_file)

def c(s):
	return s.replace('\r', ' ').replace('\n', ' ')

with open(todays_file, 'a') as f:
	writer = csv.writer(f)

	fcntl.flock(f, fcntl.LOCK_EX)

	if new_file: 
		writer.writerow(["name","phone","direction","time","server_time"])
	writer.writerow([c(name),c(phone),c(direction),c(client_time),str(server_time)])

	fcntl.flock(f, fcntl.LOCK_UN)

print_response(
	status="<p id='status' style=\"color: #009f00;\">Recorded successfully: " + direction +  " at " + client_time + "</p>", 
	)

