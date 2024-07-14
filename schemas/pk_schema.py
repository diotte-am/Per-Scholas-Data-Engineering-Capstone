pk_schema = {
    # table 1
    "CDW_SAPP_CUSTOMER" : "ALTER TABLE CDW_SAPP_CUSTOMER ADD COLUMN CUST_ID INT AUTO_INCREMENT PRIMARY KEY",
    # table 2
    "CDW_SAPP_BRANCH" : "ALTER TABLE CDW_SAPP_BRANCH ADD PRIMARY KEY (BRANCH_CODE)",
    # table 3
    "CDW_SAPP_CREDIT" : "ALTER TABLE CDW_SAPP_CREDIT ADD PRIMARY KEY (TRANSACTION_ID)",
    # table 4
    "CDW_SAPP_LOAN_DATA" : "ALTER TABLE CDW_SAPP_LOAN_DATA ADD PRIMARY KEY (A_ID)"
}