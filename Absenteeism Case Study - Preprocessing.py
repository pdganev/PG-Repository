#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


raw_csv_data = pd.read_csv('C:\\Users\\Petar\\Desktop\\Absenteeism-data.csv')


# In[3]:


raw_csv_data


# In[4]:


df = raw_csv_data.copy()
df


# In[5]:


df = df.drop(['ID'], axis = 1)
df


# In[6]:


df['Reason for Absence'].min()


# In[7]:


df['Reason for Absence'].max()


# In[8]:


df['Reason for Absence'].unique()


# In[9]:


reason_columns = pd.get_dummies(df['Reason for Absence'])


# In[10]:


reason_columns


# In[11]:


reason_columns['check'] = reason_columns.sum(axis=1)
reason_columns


# In[12]:


reason_columns['check'].unique()


# In[13]:


reason_columns = reason_columns.drop(['check'], axis = 1)


# In[14]:


reason_columns = pd.get_dummies(df['Reason for Absence'], drop_first = True)


# ## Group the Reasons for Absence:

# In[15]:


df.columns.values


# In[16]:


reason_columns.columns.values


# In[17]:


df = df.drop(['Reason for Absence'], axis = 1)


# In[18]:


reason_type_1 = reason_columns.loc[:, 1:14].max(axis=1)
reason_type_2 = reason_columns.loc[:, 15:17].max(axis=1)
reason_type_3 = reason_columns.loc[:, 18:21].max(axis=1)
reason_type_4 = reason_columns.loc[:, 22:].max(axis=1)


# ## Concatenate Column Values

# In[19]:


df


# In[20]:


df = pd.concat([df, reason_type_1, reason_type_2, reason_type_3, reason_type_4], axis = 1)
df


# In[21]:


df.columns.values


# In[22]:


column_names = ['Date', 'Transportation Expense', 'Distance to Work', 'Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours', 'Reason_1', 'Reason_2', 'Reason_3', 'Reason_4']


# In[23]:


df.columns = column_names


# In[24]:


df.head()


# ## Reorder Columns

# In[25]:


column_names_reordered = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 
                          'Date', 'Transportation Expense', 'Distance to Work', 'Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours']


# In[26]:


df = df[column_names_reordered]
df.head()


# ## Create a Checkpoint

# In[27]:


df_reason_mod = df.copy()


# In[28]:


df_reason_mod.head()


# ## 'Date':

# In[29]:


type(df_reason_mod['Date'][0])


# In[30]:


df_reason_mod['Date'] = pd.to_datetime(df_reason_mod['Date'], format = '%d/%m/%Y')


# In[31]:


type(df_reason_mod['Date'])


# ## Extracting the Month value

# In[32]:


df_reason_mod['Date'][0]


# In[33]:


df_reason_mod['Date'][0].month


# In[34]:


list_months = []
list_months


# In[35]:


df_reason_mod.shape


# In[36]:


for i in range(df_reason_mod.shape[0]):
    list_months.append(df_reason_mod['Date'][i].month)


# In[37]:


list_months


# In[38]:


len(list_months)


# In[39]:


df_reason_mod['Month Value'] = list_months


# In[40]:


df_reason_mod.head()


# ## Extracting the Day of the week

# In[41]:


def date_to_weekday(date_value):
    return date_value.weekday()


# In[42]:


df_reason_mod['Day of the Week'] = df_reason_mod['Date'].apply(date_to_weekday)


# In[43]:


df_reason_mod.head()


# In[44]:


#Dropping the 'Date' column
df_reason_mod = df_reason_mod.drop(['Date'], axis = 1)
df_reason_mod.head()


# In[45]:


#Reordering the columns
column_names_upd = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Month Value', 'Day of the Week',
       'Transportation Expense', 'Distance to Work', 'Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education', 'Children',
       'Pets', 'Absenteeism Time in Hours']


# In[46]:


df_reason_mod = df_reason_mod[column_names_upd]
df_reason_mod.head()


# In[47]:


#Creating another checkpoint
df_reason_date_mod = df_reason_mod.copy()
df_reason_date_mod.head()


# ## 'Education'

# In[48]:


df_reason_date_mod['Education'].unique()


# In[49]:


df_reason_date_mod['Education'].value_counts()


# In[50]:


df_reason_date_mod['Education'] = df_reason_date_mod['Education'].map({1:0, 2:1, 3:1, 4:1})


# In[51]:


df_reason_date_mod['Education'].unique()


# In[52]:


df_reason_date_mod['Education'].value_counts()


# ## Final Checkpoint

# In[53]:


df_preprocessed = df_reason_date_mod.copy()
df_preprocessed.head(10)


# In[54]:


df_preprocessed.to_csv('C:\\Users\\Petar\\Desktop\\df-preprocessed.csv', index=False)

