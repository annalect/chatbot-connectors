#!/usr/local/bin/node
var net = require('net')
var util = require('util')
var os = require('os')

class ChatScriptConnector {
    constructor(options){
        this.port = options.port || 1024
        this.host = options.host || 'localhost'
        this.identity = options.identity || 'undefined' /* not to be confused with 'nobody' */
        this.botname = options.botname || 'harry'
    }

    chat(message, identity=this.identity, botname=this.botname){
        return new Promise((resolve, reject)=> {    
            var client = net.createConnection(this) /* this contains the host and port properties createConnection cares about */
            var buffers = []
            client.on('connect', () => client.write([this.identity,this.botname,message].join('\0') + '\0'))
            client.on('data', data => buffers.push(data))
            client.on('error', error => reject(error))
            client.on('end', () => resolve(Buffer.concat(buffers).toString().trim()))
        }).then(this.objectify)
    }

    objectify(stringOrJSON){
        return new Promise(resolve => {
            try {
                var output = JSON.parse(stringOrJSON)
                resolve(JSON.stringify(output))
            } catch(e) {
                var output = { stdout: stringOrJSON } 
                resolve(JSON.stringify(output))                
            }
        })
    }
}

module.exports = ChatScriptConnector

/* interpret.js can act as a standalone executable! pipe input to stdin and receive JSON on stdout */

if(process.argv[2]){
    (new ChatScriptConnector({
        port: process.env.CSPORT,
        host: process.env.CSHOST,
        identity: process.env.fullName,
        botname: process.env.BOT,
    }))
    .chat(process.argv[2])
    .then(response => {
        process.stdout.write(response)   
        process.exit()
    })
    .catch(error => {
        process.stderr.write(util.inspect(error))
        process.exit()
    })
}

// process.stdin.on('data', stdin => {
//     (new ChatScriptConnector({
//         port: process.env.CSPORT,
//         host: process.env.CSHOST,
//         identity: process.env.fullName,
//         botname: process.env.BOT,
//     }))
//     .chat(stdin.toString())
//     .then(response => {
//         process.stdout.write(response)   
//         process.exit()
//     })
//     .catch(error => {
//         process.stderr.write(util.inspect(error))
//         process.exit()
//     })
// })
