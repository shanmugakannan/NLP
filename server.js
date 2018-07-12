const express = require('express');
var http = require('http');
var bodyParser = require("body-parser");
//Config
var config = require('./config/api.config');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
  });
  
function runNlp(text){
    return new Promise(function(resolve, reject) {

        var spawn  = require('child_process').spawn;
        var py = spawn('python',['nlp.py',text]);
        
        //Read Output from NLP library
        py.stdout.on('data', function(data) {
            console.log(data.toString('ascii'));
            resolve(data);
        });
        //Catch Error
        py.stderr.on('data', (data) => {
            console.log(data.toString('ascii'));
            reject(data);
        });

        //Send input to Python library
        py.stdin.write(JSON.stringify(text));
        py.stdin.end();
    });
}

app.post('/nlp/parse',function(req,res){
    if (req.body) {
        runNlp(req.body.text)
        .then(function(fromRunpy) {
            res.end(fromRunpy);
        })
        .catch(function(err){
           res.status(500).send({error : err})
        })       
       }
     });

app.get('/DL/isDL/:dl/',function(req,clientresponse){
    var dl = req.params.dl;
    var executor = config.dlmgr.executor;
    var token = config.dlmgr.token;
    var apipath = "/api/DL/exist";

    var options = {
      host: config.dlmgr.host,
      rejectUnauthorized: false,
      path: [apipath,dl,executor,token].join("/")
    };
     http.get(options, function(res){
        //console.log(options.path);
        var body = "";
        res.on('data', function(data) {
            body += data;
        });
        res.on('end', function() {
            clientresponse.setHeader('Content-Type', 'application/json')
            clientresponse.send(body);
        })
        res.on('error', function(e) {
            clientresponse.status(404).send(e.message);
        });
    });
  });
  
  app.get('/user/properties/:username/',function(req,clientresponse){
    var user = req.params.username;
    var executor = config.dlmgr.executor;
    var token = config.dlmgr.token;
    var apipath = "/api/user/properties";

    var options = {
      host: config.dlmgr.host,
      rejectUnauthorized: false,
      path: [apipath,user,executor,token].join("/")
    };
     http.get(options, function(res){
        console.log(options.path);
        var body = "";
        res.on('data', function(data) {
            body += data;
        });
        res.on('end', function() {
            clientresponse.setHeader('Content-Type', 'application/json')
            clientresponse.send(body);
        })
        res.on('error', function(e) {
            clientresponse.status(404).send(e.message);
        });
    });
  });

 


app.listen(4000, () => console.log('app listening on port 4000!'))