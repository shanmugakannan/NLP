const express = require('express')
const app = express()

function runNlp(){
    return new Promise(function(resolve, reject) {

        const { spawn } = require('child_process');
        const pyprog = spawn('python',['nlp.py']);

        pyprog.stdout.on('data', function(data) {
            resolve(data);

        });
        pyprog.stderr.on('data', (data) => {
            reject(data);
        });
    });
}

app.get('/', (req, res) => {
    runNlp()
    .then(function(fromRunpy) {
        console.log(fromRunpy.toString());
        res.end(fromRunpy);
    })
    .catch(function(err){
       console.log(err);
       res.status(500).send({error : 'request failed'})
    })

})

app.listen(4000, () => console.log('app listening on port 4000!'))