USE STOCK_MARKET;
SELECT * FROM TWO_MINUTE WHERE ID=15;
SELECT * FROM MINUTE;
SELECT * FROM STOCKS;

DELETE FROM TWO_MINUTE WHERE ID=2;
DELETE FROM MINUTE WHERE 5=5;

ALTER TABLE STOCKS DROP Full_Name;

CREATE TABLE MINUTE(
Id int not null,
Datetime datetime not null,
Open double not null,
High double not null,
Low double not null,
Close double not null,
Volume int not null,
constraint pk primary key(Id, Datetime),
foreign key(Id) references STOCKS(Id));

CREATE TABLE TWO_MINUTE(
Id int not null,
Datetime datetime not null,
Open double not null,
High double not null,
Low double not null,
Close double not null,
Volume int not null,
constraint pk primary key(Id, Datetime),
foreign key(Id) references STOCKS(Id));

DROP TABLE MINUTE;
DROP TABLE TWO_MINUTE;

DESCRIBE MINUTE;
DESCRIBE STOCKS;
