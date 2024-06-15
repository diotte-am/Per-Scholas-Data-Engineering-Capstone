pattern_dict = {
    "CDW_SAPP_CUSTOMER" : "SELECT SSN,\
        FIRST_NAME,\
        MIDDLE_NAME,\
        LAST_NAME,\
        CREDIT_CARD_NO,\
        CONCAT(STREET_NAME, ', ', APT_NO) AS FULL_STREET_ADDRESS,\
            CUST_CITY,\
        CUST_STATE,\
        CUST_COUNTRY,\
        CUST_ZIP,\
        CONCAT('(123)',\
            SUBSTRING(CUST_PHONE, 0, 3), '-',\
            SUBSTRING(CUST_PHONE, 3, 3))\
        AS CUST_PHONE,\
        CUST_EMAIL,\
        LAST_UPDATED FROM CDW_SAPP_CUSTOMER",
    "CDW_SAPP_BRANCH" : "SELECT BRANCH_CODE,\
        BRANCH_NAME,\
        BRANCH_STREET,\
        BRANCH_CITY,\
        BRANCH_STATE,\
        BRANCH_ZIP,\
        CONCAT('(',\
            SUBSTRING(BRANCH_PHONE, 0, 3), ')',\
            SUBSTRING(BRANCH_PHONE, 4, 3), '-',\
            SUBSTRING(BRANCH_PHONE, 7))\
        AS BRANCH_PHONE,\
        LAST_UPDATED FROM CDW_SAPP_BRANCH",
    "CDW_SAPP_CREDIT" : "SELECT CREDIT_CARD_NO,\
        CUST_SSN,\
        10000 * Year + 100 * Month + Day AS TIMEID,\
        BRANCH_CODE,\
        TRANSACTION_TYPE,\
        TRANSACTION_VALUE,\
        TRANSACTION_ID FROM CDW_SAPP_CREDIT"
}

