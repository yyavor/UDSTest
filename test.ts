import * as net from "net"

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
        c.write("Enter your next message:\n");
    });

    c.on("error", (error)=>{
        console.log("--------error---------")
    });

    c.on("end", ()=>{
        c.write('hello\r\n');
        c.pipe(c);
    })
});
server.listen("/tmp/echo1.sock", function(){
    console.log("Listening ...");
})