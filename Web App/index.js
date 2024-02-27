const express = require("express");
const path = require('path');
const app = express();
const session = require("express-session");
require('dotenv').config()


//express setup
app.set("view engine", "ejs");
app.use(express.static(__dirname + '/public'));
app.set('views', path.join(__dirname, '/views'));
app.use(session({
    secret: process.env.SECRET,
    resave: false,
    saveUninitialized: true,
  }));


//listening port
let port = process.env.PORT;
if (port == null || port == "") {
  port = 3069;
}

app.listen(port, function (){
    console.log("Mobile App started");
});

//routes

app.get("/home", function(req, res){
    if(req.session.user){
        res.render("home", {appTitle: "Home"});
    }else{
        res.redirect("/login");
    }
});

app.get("/login", function(req, res){
    if(!req.session.user){
        res.render("login", {appTitle: "Login"});
    }else{
        res.redirect("/home");
    }
})

app.get("/register", function(req, res){
    if(!req.session.user){
        res.render("register", {appTitle: "Register"});
    }else{
        res.redirect("/home");
    }
})