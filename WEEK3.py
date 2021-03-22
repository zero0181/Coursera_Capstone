#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation


get_ipython().system('pip install geopy')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize


get_ipython().system(' pip install folium==0.5.0')
import folium # plotting library


# ## Gather Table form wiki

# In[78]:


from bs4 import BeautifulSoup as bs
url = 'https://en.wikipedia.org/w/index.php?title=List_of_postal_codes_of_Canada:_M&oldid=1011037969'
source = requests.get(url).text
soup = BeautifulSoup(source,'html.parser')
table= soup.find('table')
toronto_df = pd.read_html(str(table))[0]
toronto_df


# ## Remove Non assigned Value

# In[83]:


#Remove Borough not assigned value
df.drop(df[df['Borough'] == 'Not assigned' ].index, inplace=True)
#Remove Neighbourhood not assigned value
df.drop(df[df['Neighbourhood'] == 'Not assigned' ].index, inplace=True)
#show Data Frame
df


# ## Import coordinates data

# In[100]:


Codi = pd.read_csv('https://cocl.us/Geospatial_data')
Codi.rename(columns={'Postal Code':'PostalCode'},inplace=True)
Codi.head()


# ## Merge Table

# In[102]:


data_Table = pd.merge(df, Codi)
data_Table 


# In[ ]:





# In[132]:


Toronto_Table = data_Table[data_Table ['Borough'].str.contains('Toronto',regex=False)]
Toronto_Table.head()


# In[ ]:





# In[115]:


map_toronto = folium.Map(location=[43.651070,-79.347015],zoom_start=10)

for lat,lng,borough,neighbourhood in zip(Toronto_Table['Latitude'],Toronto_Table['Longitude'],Toronto_Table['Borough'],Toronto_Table['Neighbourhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
    [lat,lng],
    radius=5,
    popup=label,
    color='red',
    fill=True,
    fill_color='#3186cc',
    fill_opacity=0.7,
    parse_html=False).add_to(map_toronto)
map_toronto


# In[133]:


from sklearn.cluster import KMeans
k=5
toronto_clustering = Toronto_Table.drop(['PostalCode','Borough','Neighbourhood'],1)
kmeans = KMeans(n_clusters = k,random_state=0).fit(toronto_clustering)
kmeans.labels_
Toronto_Table.insert(0,'CLabels', kmeans.labels_)


# In[128]:


Toronto_Table


# In[ ]:





# In[ ]:




