var express =require('express')
var fs=require('fs')
const multer = require("multer");
const bodyParser = require('body-parser'); 
var urlEncodeParser = bodyParser.urlencoded({extended: false});
var app=express();
app.use(multer({ dest: '/tmp/'}).array('model'));
app.use('/staticResource',express.static('staticResource'))

app.get('/',function(req,res){
	console.log(__dirname)
	res.sendFile(__dirname+"/staticResource/html/currentPicture.html")
})

app.get('/getPatternName',function(req,res){
	var readDir = fs.readdirSync("./staticResource/model/");
	res.send(readDir)
})

app.post('/upload',function(req,res){
	var fileName=new Array();
	if (req.files.length==0)
	{
		res.send("无文件");
	}
	else{
		fileName=req.files[0].originalname.split(".")
		if (fileName[fileName.length-1]!="yml")
		{
			res.send("格式有误");
		}
		else{
			var des_file = __dirname + "/staticResource/model/" + req.files[0].originalname;
			console.log(des_file);
			fs.readFile( req.files[0].path, function (err, data) {
				fs.writeFile(des_file, data, function (err) {
				if( err ){
					console.log( err );
				}else{
					res.send("上传成功");
				}
				});
			});
		}
	}
})

app.post('/delModel',urlEncodeParser,function(req,res){
	console.log(req.body.patternName);
	res.send("删除成功");
})

app.get('/getPatterns',function(req,res){
	var html=""
	var readDir = fs.readdirSync("./staticResource/model/");
	html+="<table align='center'>";
	for(var i=0;i<readDir.length;i++){
		html+="<tr>"
		html+="<td>"+readDir[i]+"</td>";
		html+="<td><button type= '"+"button"+"' onclick='"+ "delModel(this)"+"'value='"+ readDir[i]+"' >删除</button></td>"
		html+="</tr>"
	}
	html+="</table>"
	res.send(html)
})



var server=app.listen(8081,function(){
	var host = server.address().address
	var port = server.address().port

	console.log("the IP and Port http://%s:%s",host,port)
})
