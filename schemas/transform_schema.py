transform_schema = {
    # table 1
    "CDW_SAPP_CUSTOMER" : "SELECT SSN,\
        FIRST_NAME,\
        MIDDLE_NAME,\
        LAST_NAME,\
        CAST(CREDIT_CARD_NO AS BIGINT),\
        CONCAT(APT_NO, ',', STREET_NAME) AS FULL_STREET_ADDRESS,\
            CUST_CITY,\
        CUST_STATE,\
        CUST_COUNTRY,\
        CUST_ZIP,\
        CONCAT('(123)',\
            SUBSTRING(CUST_PHONE, 0, 3), '-',\
            SUBSTRING(CUST_PHONE, 4))\
        AS CUST_PHONE,\
        CUST_EMAIL,\
        CAST(LAST_UPDATED AS DATE) FROM CDW_SAPP_CUSTOMER",
    # table 2
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
        CAST(LAST_UPDATED AS DATE) FROM CDW_SAPP_BRANCH",
    # table 3
    "CDW_SAPP_CREDIT" : "SELECT CAST(CREDIT_CARD_NO AS BIGINT),\
        10000 * Year + 100 * Month + Day AS TIMEID,\
        BRANCH_CODE,\
        CUST_SSN,\
        TRANSACTION_TYPE,\
        TRANSACTION_VALUE,\
        TRANSACTION_ID FROM CDW_SAPP_CREDIT",
    # table 4
    "CDW_SAPP_LOAN_DATA" : "SELECT Application_ID,\
        CAST(SUBSTRING(Application_ID, 3, 6) AS int) AS A_ID,\
        IF(Application_Status = 'Y', 1, 0) AS APPLICATION_STATUS,\
        CAST(Credit_History AS int) AS CREDIT_HISTORY,\
        Dependents AS DEPENDENTS,\
        Education AS EDUCATION,\
        Gender AS GENDER,\
        Income AS INCOME,\
        IF(Married = 'Yes', 1, 0) AS MARRIED,\
        Property_Area AS PROPERTY_AREA,\
        IF(Self_Employed = 'Yes', 1, 0) AS SELF_EMPLOYED\
        FROM CDW_SAPP_LOAN_DATA"
}
