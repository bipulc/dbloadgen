-- Create MERCHANTS TABLE

DROP TABLE MERCHANTS;

CREATE TABLE MERCHANTS
( merchant_id INT GENERATED AS IDENTITY PRIMARY KEY ,
  merchant_name VARCHAR2(30)
) 
TABLESPACE dbloadgen_ts;

-- CREATE BUYER TABLE

DROP TABLE BUYER;

CREATE TABLE BUYER
(
  BUYER_ID  INT GENERATED AS IDENTITY PRIMARY KEY,
  first_name  VARCHAR2(30),
  last_name   VARCHAR2(30),
  company_name  VARCHAR2(50),
  address       VARCHAR2(50),
  city  VARCHAR2(30),
  county  VARCHAR2(30),
  postal  VARCHAR2(30),
  phone1  VARCHAR2(30),
  phone2  VARCHAR2(30),
  email   VARCHAR2(50),
  web     VARCHAR2(50)
)
TABLESPACE dbloadgen_ts;

-- Create TRANSACTION Table

CREATE TABLE TRANSACTION_NO_COMP 
( tran_id VARCHAR2(30),
  merchant_name VARCHAR2(30),
  buyer_first_name  VARCHAR2(30),
  buyer_last_name   VARCHAR2(30),
  buyer_company_name  VARCHAR2(50),
  buyer_address       VARCHAR2(50),
  buyer_city  VARCHAR2(30),
  buyer_county  VARCHAR2(30),
  buyer_postal  VARCHAR2(30),
  buyer_phone1  VARCHAR2(30),
  buyer_phone2  VARCHAR2(30),
  buyer_email   VARCHAR2(50),
  buyer_web     VARCHAR2(50),
  prd_id        NUMBER,
  qty           NUMBER,
  unit_price          NUMBER
)
TABLESPACE NO_ACO_TS;

