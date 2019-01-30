import * as net from "net"
import * as msgpack from "msgpack"

var server = net.createServer( (c) => {
    console.log("Subscribe to all events");

    c.on("connect", ()=>{
        console.log("--------connect---------")
    });

    c.on("close", ()=>{
        console.log("--------close---------")
    });

    c.on("data", (data)=>{
        console.log(data.toString())
        var message = msgpack.pack([1, 2, 3, 34]);
        c.write(message);
    });

    c.on("error", (error)=>{
        console.log("--------error---------")
        console.log(error.message)
    });

    c.on("end", ()=>{
        c.write('hello\r\n');
        c.pipe(c);
    })
});
server.listen("/tmp/echo1.sock", function(){
    console.log("Listening ...");
})