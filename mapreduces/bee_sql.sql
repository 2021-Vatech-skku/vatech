
!sh pwd
create database IF NOT EXISTS test;
use test;
show tables;
create or replace TABLE treatments
  USING DELTA
  LOCATION '/Users/leejunseok/work/vtshare/mapreduces/treatments';
create or replace TABLE patients
  USING DELTA
  LOCATION '/Users/leejunseok/work/vtshare/mapreduces/patients';
create or replace TABLE receipt
  USING DELTA
  LOCATION '/Users/leejunseok/work/vtshare/mapreduces/receipts';



show tables;
