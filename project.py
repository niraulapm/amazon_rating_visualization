
#%%
import pandas as pd
import datetime

data=pd.read_csv('./ratings_Electronics.csv',header=None)
data.columns=['User','Item','Rating','Time']

#%%
# choosing data for year 2013
data=data.sort_values(by='Time',ascending=True)
data=data[data['Time']>1357016400]
data=data[data['Time']<1388552400]
data['Time']=data['Time'].apply(lambda x: datetime.datetime.fromtimestamp(x))
#%%
# Lets include only regular customers for the analysis who give ratings to products
# at least 20 times
#%%
selected_users=data['User'].value_counts()
selected_users=selected_users[selected_users>20]
top_users=data[data['User'].isin(selected_users.index)]
#%%
# Lets include items with more than 50 number of ratings
items=top_users['Item'].value_counts()
items=items[items>50]
top_items=top_users[top_users['Item'].isin(items.index)]
#%%
# Lets choose items having average rating more than 4.0 for the 
avg_4=top_items.groupby('Item').mean()
avg_4=avg_4[avg_4['Rating']>4.0]
top_items=top_items[top_items['Item'].isin(avg_4.index)]

#%%
# boxplot of the ratings of items for 12 months
box_data=pd.pivot_table(top_items,index='Month',values='Rating',columns='Item')
#%%
# ploting a boxplot using plotly
import plotly.offline as pyo
import plotly.graph_objs as go



data = [
    go.Box(
        y=box_data['B000QUUFRW'],
        name='B000QUUFRW'
    ),
    go.Box(
        y=box_data['B000VX6XL6'],
        name='B000VX6XL6'
    ),
    go.Box(
        y=box_data['B001TH7GUU'],
        name='B001TH7GUU'
    ),
    go.Box(
        y=box_data['B002V88HFE'],
        name='B002V88HFE'
    ),
    go.Box(
        y=box_data['B002WE6D44'],
        name='B002WE6D44'
    ),
    go.Box(
        y=box_data['B0034CL2ZI'],
        name='B0034CL2ZI'
    ),
    go.Box(
        y=box_data['B003ES5ZUU'],
        name='B003ES5ZUU'
    ),
    go.Box(
        y=box_data['B0041Q38NU'],
        name='B0041Q38NU'
    ),
    go.Box(
        y=box_data['B005CT56F8'],
        name='B005CT56F8'
    ),
    go.Box(
        y=box_data['B005FYNSPK'],
        name='B005FYNSPK'
    ),
    go.Box(
        y=box_data['B009SYZ8OC'],
        name='B009SYZ8OC'
    )
]
layout = go.Layout(
    title = 'Comparison of amazon ratings of Electronic Items'
)
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='box.html')

# doing a barplot of average rating and number of ratings for a particular item
item_rating_count=top_items[top_items['Item']=='B005CT56F8']
bar_data=item_rating_count.groupby('Month').mean()
bar_data['Counts']=item_rating_count.groupby('Month').size()
bar_data=bar_data.reset_index()

# ploting bar plot using plotly
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


trace1 = go.Bar(
    x=months,  
    y=bar_data['Rating'],
    name = 'Rating',
    marker=dict(color='#FFD700') 
)
trace2 = go.Bar(
    x=months,
    y=bar_data['Counts'],
    name='Counts',
    marker=dict(color='#9EA0A1') 
)

data = [trace1, trace2]
layout = go.Layout(
    title='Bar diagram- average rating and no_of_counts per each month -2013'
)
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='bar.html')