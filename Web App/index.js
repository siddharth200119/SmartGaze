const express = require("express");
const path = require('path');
const app = express()
app.set("view engine", "ejs");
app.use(express.static(__dirname + '/public'));
app.set('views', path.join(__dirname, '/views'));


let port = process.env.PORT;
if (port == null || port == "") {
  port = 3069;
}

app.listen(port, function (){
    console.log("Mobile App started");
})

app.get("/", function(req, res){
    res.render("home", {appTitle: "Home"});
});