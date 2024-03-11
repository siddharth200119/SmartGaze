const express = require("express");
const path = require('path');
const app = express();
var bodyparser = require('body-parser');
const session = require("express-session");
var mysql = require('mysql');
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
app.use(bodyparser.urlencoded({extended: true}));
app.use(bodyparser.json());


//mysql connection

var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "password",
    database: "SmartGaze"
});



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
    if(req.session.uid){
        const params = {
            siteTitle: "Home", 
            appTitle: req.session.userName,
            uid: req.session.uid,
            appHeaderBtn: {
                title: "Logout",
                route: "/logout"
            }
        }
        res.render("home", params);
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
            },
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

//apis

app.post("/api/login", function(req, res){
    const email = req.body.username;
    const password = req.body.password;
    con.connect(function(err) {
        if (err) throw err;
        console.log("SQL Connected");
        con.query("SELECT UID FROM Users WHERE email = '" + email + "' and password = '" + password + "'", function(err, result, fields){
            if(err) throw err;
            if(result[0].UID){
                req.session.uid = result[0].UID
                res.redirect("/home")
            }else{
                res.redirect("/login")
            }
            console.log(result[0].UID)
        })
    });
})