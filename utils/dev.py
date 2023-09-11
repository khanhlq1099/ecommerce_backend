import pandas as pd
import numpy as np
# from config.db_config import engine


# ['user', 'user_detail', 'product_category', 'product_sub_category', 'product', 'payment_method'] 

# df = pd.read_excel('ecommerce_db_create.xlsx',sheet_name='product')

# print(df)
# df.to_sql('user_detail',engine,index=False, if_exists='append')

def handle(num):
    if num < '2': return 'a'
    elif num < '3':return 'b'
    else: return 'c'

df1 = pd.DataFrame({'Bin':['(-inf,2)','[2,3)','(3,inf)'],
                    'WoE':['a','b','c']})


df2 = pd.DataFrame({
    'Value':['1','2.5','3.5']
})

df2['WoE'] = df2['Value'].apply(handle)

print(df2)