create database IF NOT EXISTS test_minio;
use test_minio;
create or replace  TABLE treatments
  USING DELTA
  LOCATION 's3a://bigdata/treatments';
create or replace TABLE patients
  USING DELTA
  LOCATION 's3a://bigdata/patients';
show tables;
