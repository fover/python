<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf8" />
<title>摩卡托坐标转经纬度坐标</title>
<meta name="description" content="" />
<script type="text/javascript" src="http://api.map.baidu.com/api?v=1.2"></script>
</head>
<body>
<div style="display:none;" id="container"></div>
<div style="width:500px;height:270px;float:left;margin:0 0 0 10px;">
    <p>摩卡托坐标x:<input type="text" value="12128773.43" id="mctX" /></p>
    <p>摩卡托坐标y:<input type="text" value="4040249.00" id="mctY" /></p>
    <p id="pointX"></p>
    <p id="pointY"></p>
    <p id="entertaiment"></p>
    <p><input style="width:400px;height:80px;font-size:30px;" type="button" value="摩卡托坐标转经纬度坐标" onclick="mctGeo();" /></p>
    <textarea id="content" rows="200" cols="200"></textarea>
</div>
</body>
</html>
<script type="text/javascript">
//以下两句话为创建地图
var map = new BMap.Map("container");

function mctGeo(){
    var mctXX = document.getElementById("mctX").value;
    var mctYY = document.getElementById("mctY").value;    
    var mctXY = new BMap.Pixel(mctXX,mctYY);    
    
    var projection2 = map.getMapType().getProjection();
    var LngLat = projection2.pointToLngLat(mctXY);    
    
    document.getElementById("pointX").innerHTML = "经纬度lng: " + LngLat.lng;
    document.getElementById("pointY").innerHTML = "经纬度lat: " + LngLat.lat;
}
</script>
