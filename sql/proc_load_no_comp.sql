CREATE OR REPLACE PROCEDURE load_no_comp(pi_num_rows IN NUMBER)
AS
    lv_merchant_name merchants.merchant_name%TYPE;
    lv_first_name     buyer.first_name%type;
    lv_last_name      buyer.last_name%type;
    lv_company_name    buyer.company_name%type;
    lv_address    buyer.address%type; 
    lv_city   buyer.city%type; 
    lv_county buyer.county%type; 
    lv_postal buyer.postal%type; 
    lv_phone1 buyer.phone1%type; 
    lv_phone2 buyer.phone2%type;
    lv_email  buyer.email%type; 
    lv_web    buyer.web%type;

BEGIN

For rec in 1 .. pi_num_rows loop
  -- Get a merchant id (random number between 1 and 100) and get merchant row
  
  SELECT MERCHANT_NAME INTO lv_merchant_name FROM MERCHANTS 
  WHERE MERCHANT_ID = floor(dbms_random.value(1, 100));
  
  -- Get a buyer id ( random number between 1 and 500) and get buyer row
  SELECT first_name,last_name,company_name,address ,city,county,postal,phone1,phone2,email,web
  INTO lv_first_name, lv_last_name, lv_company_name, lv_address, lv_city, lv_county, lv_postal, lv_phone1, lv_phone2,
       lv_email, lv_web
  FROM BUYER WHERE buyer_id = floor(dbms_random.value(1,500));
  
  -- insert into transaction table
  
  INSERT INTO TRANSACTION_NO_COMP 
( tran_id , merchant_name ,buyer_first_name ,buyer_last_name  ,buyer_company_name ,
  buyer_address ,buyer_city,buyer_county,buyer_postal,buyer_phone1,buyer_phone2,
  buyer_email,buyer_web,prd_id ,qty ,unit_price )
Select DBMS_RANDOM.STRING('X',30), lv_merchant_name,
       lv_first_name, lv_last_name, lv_company_name, lv_address, lv_city, lv_county, lv_postal, lv_phone1, lv_phone2,
       lv_email, lv_web,
        floor(dbms_random.value(1,10000)),
        floor(dbms_random.value(1,1000)),
        floor(dbms_random.value(1,100))
FROM DUAL;

END loop;

COMMIT;

END load_no_comp;
/
