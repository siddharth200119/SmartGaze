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
        const params = {
            siteTitle: "Home", 
            appTitle: req.session.userName,
            appHeaderBtn: {
                title: "Logout",
                route: "/logout"
            }
        }
        res.render("home", );
    }else{
        res.redirect("/login");
    }
});

app.get("/login", function(req, res){
    if(!req.session.user){
        const params = {
            siteTitle: "Login", 
            appTitle: "Login",
            appHeaderBtn: {
                title: "Register",
                route: "/register"
            }
        }
        res.render("login", params);
    }else{
        res.redirect("/home");
    }
})

app.get("/register", function(req, res){
    if(!req.session.user){
        const params = {
            siteTitle: "Register", 
            appTitle: "Register",
            appHeaderBtn: {
                title: "Login",
                route: "/login"
            }
        }
        res.render("register", params);
    }else{
        res.redirect("/home");
    }
})