import pandas as pd
import mysql.connector
conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Sahil@050',
    database='ecommerce_db',
)
query="""SELECT c.customer_id,c.name,c.region,
       COUNT(o.order_id) AS Total_Orders,
       COALESCE(SUM(o.price),0) AS Total_Spent
       FROM customers c
       LEFT JOIN orders o 
       ON c.customer_id=o.customer_id
       GROUP BY c.customer_id,c.name,c.region"""
df=pd.read_sql(query,conn)
conn.close()
print(df)
import numpy as np
df["Customer_Tier"]=np.where(df["Total_Spent"]>10000,"VIP","Standard")

Spending_array=df["Total_Spent"].to_numpy()
mean_val=np.mean(Spending_array)
std_val=np.std(Spending_array)

# handle where the standard deviation is zero
if std_val>0:
    df["Spending_Z_score"]=(Spending_array-mean_val)/std_val
else:
    df["Spending_Z_score"]=0
print("--Final Processed Pipeline Data--")
print(df)
