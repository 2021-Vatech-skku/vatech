
!sh pwd
create database IF NOT EXISTS test;
use test;
show tables;
create or replace TABLE treatments
  USING DELTA
  LOCATION '/Users/leejunseok/work/vtshare/mapreduces/treatments';

show tables;
