'use strict';

const WebSocket = require('ws');
const uuid = require('uuid');
const express = require('express');

const colors = require('./colors.json');
/*
 ************************** WEB SOCKET **************************
 */

const wss = new WebSocket.Server({
    port: 5555
});

function broadcast() {
    const jsonld = {
        '@context': {
            'color': 'http://www.streamreasoning.org/ontologies/2018/9/colors#',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
        },
        '@id': uuid.v4(),
        '@type': 'color:' + randomItem(['Red', 'Yellow', 'Blue'])
    }

    const jsonldString = JSON.stringify(jsonld, null, 4);

    wss.clients.forEach(function each(client) {
        if (client.readyState === WebSocket.OPEN) {
            client.send(jsonldString);
        }
    });
}

console.log('Web Socket on port 5555!');

(function loop() {
    var rand = Math.round(Math.random() * 1000);
    setTimeout(function() {
        broadcast();
        loop();
    }, rand);
}());

function randomItem(items) {
    return items[Math.floor(Math.random() * items.length)];
}

/*
 ************************** HTTP SERVER **************************
 */

const app = express();

app.get('/colors', function(req,res) {
    res.header("Content-Type",'application/json');
    res.send(JSON.stringify(colors, null, 4));
});

app.listen(8080, function () {
    console.log('Http server listening at http://localhost:8080');
});