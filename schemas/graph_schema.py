GRAPH = {
    "3.1" : ["SELECT COUNT(TRANSACTION_ID) AS TOTAL,\
            TRANSACTION_TYPE FROM CDW_SAPP_CREDIT\
            GROUP BY TRANSACTION_TYPE\
            ORDER BY TOTAL DESC",
            "Transaction type with the highest transaction count"],
    "3.2" : ["SELECT CUST_STATE,\
            COUNT(CUST_ID) AS TOTAL FROM CDW_SAPP_CUSTOMER\
            GROUP BY CUST_STATE\
            ORDER BY TOTAL DESC LIMIT 10",
            "Top 10 states with the highest number of customers"],
    "3.3" : ["SELECT CDW_SAPP_CUSTOMER.CUST_ID,\
            CONCAT(CDW_SAPP_CUSTOMER.FIRST_NAME, ' ', CDW_SAPP_CUSTOMER.LAST_NAME) AS NAME,\
            COUNT(CDW_SAPP_CREDIT.TRANSACTION_ID) AS TOTAL,\
            SUM(TRANSACTION_VALUE) AS SUM\
            FROM CDW_SAPP_CUSTOMER JOIN CDW_SAPP_CREDIT ON CDW_SAPP_CUSTOMER.CUST_ID = CDW_SAPP_CREDIT.CUST_ID\
            GROUP BY CDW_SAPP_CUSTOMER.CUST_ID\
            ORDER BY SUM DESC LIMIT 10",
            "Top 10 customers with the highest transaction amounts"],
    "5.1" : ["SELECT COUNT(A_ID)/(SELECT COUNT(A_ID) FROM CDW_SAPP_LOAN_DATA WHERE Married = 0 AND Gender = 'Male')*100 AS Percent,\
            (CASE Application_Status WHEN 1 THEN 'Approved' ELSE 'Declined' END) as Result,\
            COUNT(A_ID) AS Total\
            FROM CDW_SAPP_LOAN_DATA WHERE Married = 0 AND Gender = 'Male' GROUP BY Application_Status",
            "Percentage of rejection for married male applicants"],
    "5.2" : ["SELECT COUNT(A_ID) AS Total, Application_Status, Self_Employed FROM CDW_SAPP_LOAN_DATA GROUP BY Application_Status, Self_Employed", 
             "Percentage of applications approved for self-employed applicants"],
    "5.3" : ["SELECT SUBSTRING(CAST(TIMEID AS CHAR), 1, 6) AS YEAR,\
            COUNT(TRANSACTION_ID) AS TOTAL FROM CDW_SAPP_CREDIT\
            GROUP BY YEAR\
            ORDER BY TOTAL DESC\
            LIMIT 3",
            "plot the top three months with the largest volume of transaction data"],
    "5.4" : ["SELECT SUM(c.TRANSACTION_VALUE) AS TOTAL,\
            c.BRANCH_CODE, b.BRANCH_CITY FROM CDW_SAPP_CREDIT AS c\
            JOIN CDW_SAPP_BRANCH AS b ON b.BRANCH_CODE = c.BRANCH_CODE\
            WHERE TRANSACTION_TYPE = 'Healthcare'\
            GROUP BY BRANCH_CODE ORDER BY TOTAL DESC LIMIT 5",
            "Branches with the highest total healthcare transaction cost"]
}
