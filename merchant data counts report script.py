#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df=pd.read_csv('march_till_17th_daily_transactions.csv', low_memory=False)


# In[3]:


df.columns


# In[4]:


df.head()


# In[5]:


df.tail()


# In[6]:


merchant_products = [
    'capital provider account', 'usd-wallet','dealer', 'matatu', 'paybill-businessoption', 
    'paybill-customeroption', 'sandbox', 'till', 'till-customeroption', 
    'viewtech control', 'wallet as a service'
]

user_products = [
    'wallet-personal', 'personal sub wallet', 'limited personal wallet',
    'chama account', 'biashara wallet','escrow'
]

agency_products = [
    'agency aggregated shop', 'agency hq', 'agencyshop'
]


# In[7]:


merchant_products = [p.strip().lower() for p in merchant_products]
user_products = [p.strip().lower() for p in user_products]
agency_products = [p.strip().lower() for p in agency_products]


# In[8]:


df['product_type'] = (
    df['product_type']
    .astype(str)
    .str.lower()
    .str.strip()
    .str.replace(r'\s+', ' ', regex=True)
)


# In[9]:


def categorize_product(product):
    product = product.lower()
    if product in merchant_products:
        return "Merchant"
    elif product in user_products:
        return "User"
    elif product in agency_products:
        return "Agency"
    else:
        return "Other"
df['product_segment'] = df['product_type'].apply(categorize_product)


# In[10]:


merchant_df = df[df['product_type'] == 'Merchant']


# In[11]:


merchant_df = df[df['product_type'] == 'Merchant']


# In[12]:


merchant_df['transaction_date'] = pd.to_datetime(merchant_df['transaction_date'])
merchant_df['date_only'] = merchant_df['transaction_date'].dt.date

merchant_df['merchant'] = merchant_df['account_name'] + ' (' + merchant_df['account_number'].astype(str) + ')'


# In[13]:


pivot = merchant_df.pivot_table(
    index='merchant',
    columns='date_only',
    values='transaction_code', 
    aggfunc='count',
    fill_value=0
)


# In[14]:


print(merchant_df.columns)


# In[15]:


print(merchant_df[['merchant', 'date_only', 'transaction_code']].head(10))
print("Total rows:", len(merchant_df))


# In[16]:


print(df['product_type'].unique())


# In[17]:


merchant_df = df[df['product_segment'] == 'Merchant'].copy()


# In[18]:


merchant_df['transaction_date'] = pd.to_datetime(merchant_df['transaction_date'])
merchant_df['date_only'] = merchant_df['transaction_date'].dt.date

merchant_df['merchant'] = merchant_df['account_name'] + ' (' + merchant_df['account_number'].astype(str) + ')'


# In[19]:


pivot = merchant_df.pivot_table(
    index='merchant',         
    columns='date_only',       
    values='transaction_code',
    aggfunc='count',
    fill_value=0
)


# In[25]:


merchant_df = df[df['product_segment'] == 'Merchant']

num_merchants = merchant_df['account_name'].nunique()
print("Total Merchants who transacted:", num_merchants)


# In[28]:


pivot['Total_transaction'] = pivot.sum(axis=1)

pivot = pivot.sort_values(by='Total', ascending=False)


# In[29]:


pivot.to_excel('merchant_daily_transactions_with_total.xlsx')


# In[ ]:




