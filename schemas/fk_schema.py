fk_schema = {
    "ALTER TABLE CDW_SAPP_CREDIT ADD COLUMN CUST_ID INT",
    "UPDATE CDW_SAPP_CREDIT C JOIN CDW_SAPP_CUSTOMER CU ON C.CUST_SSN = CU.SSN SET C.CUST_ID = CU.CUST_ID",
    "ALTER TABLE CDW_SAPP_CREDIT ADD FOREIGN KEY (CUST_ID) REFERENCES CDW_SAPP_CUSTOMER(CUST_ID)",
    "ALTER TABLE CDW_SAPP_CREDIT ADD FOREIGN KEY (BRANCH_CODE) REFERENCES CDW_SAPP_BRANCH(BRANCH_CODE)",
    "ALTER TABLE CDW_SAPP_CREDIT DROP COLUMN CUST_SSN"
}