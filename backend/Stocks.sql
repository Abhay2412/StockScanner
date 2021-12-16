CREATE DATABASE STOCKS;
USE STOCKS;

DROP TABLE IF EXISTS Prediction;
CREATE TABLE Prediction (
P_ID VARCHAR(4) NOT NULL,
PRIMARY KEY(P_ID)
);

DROP TABLE IF EXISTS Business;
CREATE TABLE Business (
Business_ID VARCHAR(4) NOT NULL,
Address VARCHAR(45) NOT NULL, 
Founding_Date VARCHAR(25) NOT NULL,
Business_Name VARCHAR(25) NOT NULL,
PRIMARY KEY(Business_ID)
);

DROP TABLE IF EXISTS User;
CREATE TABLE User (
Username VARCHAR(16) NOT NULL,
Password VARCHAR(25) NOT NULL,
Permissions VARCHAR(255) NOT NULL, 
PRIMARY KEY(Username)
);

DROP TABLE IF EXISTS Exchanges;
CREATE TABLE Exchanges (
Name VARCHAR(25) NOT NULL,
Location VARCHAR(25) NOT NULL, 
Number_of_Tickers INT NOT NULL, 
PRIMARY KEY(Name)
);

DROP TABLE IF EXISTS Stock;
CREATE TABLE Stock(
ID VARCHAR(12) NOT NULL,
Company_ID VARCHAR(4) NOT NULL,
Prediction_ID VARCHAR(4) NOT NULL,
Predict_Stock_Price INT NOT NULL, 
Strong_Buy INT NOT NULL, 
Rating_Buy INT NOT NULL, 
Rating_Sell INT NOT NULL, 
Strong_Sell INT NOT NULL,
Rating_Hold INT NOT NULL, 
Stock_Price INT NOT NULL, 
Sector VARCHAR(255) NOT NULL,
PRIMARY KEY (ID),
CONSTRAINT BusinessID FOREIGN KEY (Company_ID) REFERENCES Business(Business_ID),
CONSTRAINT PredictionID FOREIGN KEY (Prediction_ID) REFERENCES Prediction(P_ID)
);

DROP TABLE IF EXISTS BelongsTo;
CREATE TABLE BelongsTo (
ID VARCHAR(12) NOT NULL,
Name VARCHAR(25) NOT NULL,
PRIMARY KEY(ID),
CONSTRAINT ID10 FOREIGN KEY (ID) REFERENCES Stock(ID),
CONSTRAINT Name FOREIGN KEY (Name) REFERENCES Exchanges(Name)
);

DROP TABLE IF EXISTS Analyst;
CREATE TABLE Analyst (
Analyst_ID_Number VARCHAR(4) NOT NULL,
ID VARCHAR(12) NOT NULL,
Name VARCHAR(25) NOT NULL,
Company VARCHAR(25) NOT NULL,
PRIMARY KEY(Analyst_ID_Number),
CONSTRAINT ID1 FOREIGN KEY (ID) REFERENCES Stock(ID)
);

DROP TABLE IF EXISTS Admin;
CREATE TABLE Admin (
Username VARCHAR(16) NOT NULL,
PRIMARY KEY(Username),
CONSTRAINT Username1 FOREIGN KEY (Username) REFERENCES User(Username)
);

DROP TABLE IF EXISTS Watchlist;
CREATE TABLE Watchlist (
List_Number INT NOT NULL,
PRIMARY KEY(List_Number)
);

DROP TABLE IF EXISTS Contain;
CREATE TABLE Contain (
Watchlist_ID INT NOT NULL,
Stock_ID VARCHAR(12) NOT NULL,
CONSTRAINT WID FOREIGN KEY (Watchlist_ID) REFERENCES Watchlist(List_Number),
CONSTRAINT SID FOREIGN KEY (Stock_ID) REFERENCES Stock(ID)
);

DROP TABLE IF EXISTS Private;
CREATE TABLE Private (
Username VARCHAR(16) NOT NULL,
List_Number INT NOT NULL, 
Role_Type VARCHAR(13) NOT NULL, 
PRIMARY KEY(Username),
CONSTRAINT Username2 FOREIGN KEY (Username) REFERENCES User(Username),
CONSTRAINT ListNumber FOREIGN KEY (List_Number) REFERENCES Watchlist(List_Number)
);

DROP TABLE IF EXISTS Professional;
CREATE TABLE Professional (
Username VARCHAR(16) NOT NULL,
List_Number INT NOT NULL, 
Role_Type VARCHAR(13) NOT NULL, 
PRIMARY KEY(Username),
CONSTRAINT Username3 FOREIGN KEY (Username) REFERENCES User(Username),
CONSTRAINT ListNumber1 FOREIGN KEY (List_Number) REFERENCES Watchlist(List_Number)
);

DROP TABLE IF EXISTS StockEvent;
CREATE TABLE StockEvent (
Event_ID VARCHAR(4) NOT NULL,
Stock_ID VARCHAR(12) NOT NULL, 
P_ID VARCHAR(4) NOT NULL,
Time VARCHAR(8) NOT NULL, 
Date VARCHAR(10) NOT NULL,
Bearish_sentiment VARCHAR(255) NOT NULL,
Neutral_sentiment VARCHAR(255) NOT NULL,
Bullish_sentiment VARCHAR(255) NOT NULL,
Price_Change INT NOT NULL, 
Predict_Stock_Events VARCHAR(255) NOT NULL, 
PRIMARY KEY(Event_ID),
CONSTRAINT ID3 FOREIGN KEY (Stock_ID) REFERENCES Stock(ID),
CONSTRAINT PredictionID1 FOREIGN KEY (P_ID) REFERENCES Prediction(P_ID)
);

DROP TABLE IF EXISTS SecFiling;
CREATE TABLE SecFiling (
Event_ID VARCHAR(4) NOT NULL,
P_ID VARCHAR(4) NOT NULL,
Type_of_Filing VARCHAR(255) NOT NULL, 
Predict_SEC_Filing VARCHAR(255) NOT NULL, 
CONSTRAINT EID FOREIGN KEY (Event_ID) REFERENCES StockEvent(Event_ID),
CONSTRAINT PredictionID2 FOREIGN KEY (P_ID) REFERENCES Prediction(P_ID)
);

DROP TABLE IF EXISTS PR;
CREATE TABLE PR (
Event_ID VARCHAR(4) NOT NULL,
P_ID VARCHAR(4) NOT NULL,
Headline VARCHAR(255) NOT NULL, 
Predict_PR VARCHAR(255) NOT NULL, 
PRIMARY KEY(Event_ID),
CONSTRAINT EID1 FOREIGN KEY (Event_ID) REFERENCES StockEvent(Event_ID),
CONSTRAINT PredictionID3 FOREIGN KEY (P_ID) REFERENCES Prediction(P_ID)
);

DROP TABLE IF EXISTS Week52;
CREATE TABLE Week52 (
Event_ID VARCHAR(4) NOT NULL,
P_ID VARCHAR(4) NOT NULL,
Value_1 VARCHAR(255) NOT NULL, 
Type_High VARCHAR(255) NOT NULL, 
Type_Low VARCHAR(255) NOT NULL, 
Predict_52Week VARCHAR(255) NOT NULL, 
CONSTRAINT EID2 FOREIGN KEY (Event_ID) REFERENCES StockEvent(Event_ID),
CONSTRAINT PredictionID4 FOREIGN KEY (P_ID) REFERENCES Prediction(P_ID)
);

DROP TABLE IF EXISTS Offering;
CREATE TABLE Offering (
Offering_ID VARCHAR(4) NOT NULL,
ID VARCHAR(12) NOT NULL,
Quantity_of_stock INT NOT NULL, 
Price_offered_at DOUBLE NOT NULL, 
Status_Complete VARCHAR(255) NOT NULL, 
Status_Incomplete VARCHAR(255) NOT NULL, 
PRIMARY KEY(Offering_ID),
CONSTRAINT ID4 FOREIGN KEY (ID) REFERENCES Stock(ID)
);

INSERT INTO BUSINESS (Business_ID, Address, Founding_Date, Business_Name)
VALUES ('AAPL', '1234 California Road', '1976-1-04', 'Apple');

INSERT INTO PREDICTION (P_ID)
VALUES ('1001');

INSERT INTO PREDICTION (P_ID)
VALUES ('1002');

INSERT INTO PREDICTION (P_ID)
VALUES ('1003');

INSERT INTO PREDICTION (P_ID)
VALUES ('1004');

INSERT INTO STOCK (ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector)
VALUES ('AAPL.NASDAQ', 'AAPL', '1001', 160, 1, 1, 0, 0, 1, 151, 'Tech');