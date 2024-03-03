create database SmartGaze;
use SmartGaze;
create table Users (
	UID INT(7) Primary Key,
    user_name Varchar(30) NOT NULL,
    face_pattern Varchar(1000) NOT NULL,
    api_key Varchar(255)
);

create table Mirrors (
	MID INT(7) Primary Key
);

create Table User_mirror_bridge(
	UID INT(7),
    MID INT(7),
    Layout Varchar(255),
    alarm_time time,
    alarm_date date,
    Foreign key (UID) references Users(UID),
    Foreign key (MID) references Mirrors(MID)
);

create table To_do_list(
	title Varchar(255) NOT NULL,
    item_description Varchar(500) NOT NULL,
    UID int(7) NOT NULL,
    due_date datetime,
    Foreign key (UID) references Users(UID)
);

create table News_pref(
	PID INT(11) Primary Key,
    topic Varchar(255)
);

create table News_pref_bridge(
	PID INT(11),
    UID INT(7),
    Foreign key (UID) references Users(UID),
    Foreign key (PID) references News_pref(PID)
);
