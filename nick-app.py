from os import ctermid
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn  as sns
from PIL import Image


st.set_option('deprecation.showPyplotGlobalUse', False)
sns.set_style('darkgrid')
st.set_page_config(layout="wide")

st.header("Dashboard for Examining Earthquake Trends in the Contiguous US")
st.write("#### By Nicholas Bronson")

expander_a = st.expander("Click here to expand and contract the introduction to this app", expanded = True)
expander_a.write('''Welcome to this Earthquake dashboard. All data used in this app was aquired from the
    United States Geological Survey's earthquake database linked [here](https://www.usgs.gov/programs/earthquake-hazards/earthquakes).''')
    
expander_a.write('''This dashboard provides insight on frequency, location, and magnitude of earthquakes
    in the contiguous United States (all states excluding Hawaii and Alaska).''')
    
expander_a.write('''The genesis of my idea to create this dashboard came from [this CNN article.](https://www.google.com/search?q=cnn+earthquakes+oregon&oq=cnn+earthquakes+oregon&aqs=chrome..69i57j69i60.2443j0j7&sourceid=chrome&ie=UTF-8)
    This dashboard will allow users to look into the earthquake data, and filter it in several different manners.
    Perhaps you can answer the question:''')

expander_a.write('''##### Have earthquakes been increasing in number or severity in the US, particularly on the West Coast?''')

def upload_data():
    #Function to load csv data into streamlit  
    data = pd.read_csv('https://raw.githubusercontent.com/bronsonnh/streamlit_repo/main/earthquake_updated_2fin.csv')
    return data

data = upload_data()

## Calculations for Earthquake Facts
n_eqs = len(data[data["year"] == 2021])
av_mag = round((data["mag"].mean()),2)
n_eqs_two_point_five_or_more = len(data[data["year"] == 2021])
avg_error = round((data["magError"].mean()),2)


expander_b = st.expander("Click here to see basic facts about earthquakes", expanded=False)

## Earthquake Facts 
expander_b.write("""## Basic Earthquake Facts & Graphs:
###### Note the data considered is only for earthquakes with a magnitude of 2 or greater. 
### Number of Earthquakes in the US in 2021:
""")
expander_b.header(n_eqs)
expander_b.write("""
### Average magnitude of earthquakes over the last 10 years:
""")
expander_b.header(av_mag)
expander_b.write(
"""
### Average error in magnitude of reported earthquakes:
""")
expander_b.header(avg_error)
expander_b.write("The number above is the estimated standard error for the magnitude of all earthquakes examined.") 

expander_b.write(
"""
To provide a bit of context, please see the table below provided by Michigan Tech's [website](https://www.mtu.edu/geo/community/seismology/learn/earthquake-measure/magnitude/).
""")
expander_b.image("https://raw.githubusercontent.com/bronsonnh/streamlit_repo/main/eq_table_mr.png")


expander_b.write(
"""
To understand the distribution of earthquake strength, please see the following histogram:
""")
fig = plt.figure(figsize=(10,4))
plt.hist(data["mag"], bins=30)
plt.xlabel("Earthquake Magnitude", fontsize=20)
plt.ylabel("Number of Earthquakes", fontsize=20)
plt.title("Distribution of Earthquake Strength 2010-2021", fontsize=20)
expander_b.pyplot(fig)


expander_b.write("""
The graph below shows the number of earthquakes per year in the US, as you can see 2019-2021 it appears the number of earthquakes has increased.
While this graph does clearly demonstrate this, it is worth considering that perhaps measurement has become more precise, more locations
that track earthquakes have come online, or some other confounding factor could be present.
""")
year_groups = data.groupby([data['year']])['year'].count()
year_value_counts = data['year'].value_counts(sort=False, ascending = False)
year_value_counts = year_value_counts.reindex(index=year_value_counts.index[::-1])
year_value_dict = dict(year_value_counts) 

fig = plt.figure(figsize=(10,4))
plt.bar(year_value_dict.keys(), year_value_dict.values())
plt.xlabel("Number of Earthquakes", fontsize=20)
plt.ylabel("Year", fontsize=20)
plt.title("Earthquakes per Year", fontsize=20)
expander_b.pyplot(fig)



#Number to Month Dictionary:
month_num_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5 , 'June': 6, 'July': 7, 'August': 8, 
                  'September': 9, 'October': 10, 'November': 11,'December': 12}

c1,c2 = st.columns((1,1))



c1.write(
"""
### Map to display number of earthquakes, sliders to choose month, year, and strength of earthquakes displayed.
""")

##Filter Creation - Filters for Month, Year, and Magnitude
month_dd = c1.selectbox('Select the Month', (month_num_dict.keys()))
year_dd = c1.selectbox('Select the Year', range(int(data['year'].min()), int(data['year'].max() + 1)))

# month_input = c1.slider('Month Filter', int(data['month'].min()), int(data['month'].max()))
#year_input = c1.slider('Year Filter', int(data['year'].min()), int(data['year'].max()))
mag_input = c1.slider('Magnitude Filter (strengths greater than or equal to selected input)', int(data['mag'].min()), int(data['mag'].max()))

month_filter = data['month'] == month_num_dict[month_dd]
year_filter = data['year'] == year_dd
mag_filter = data['mag'] >= mag_input

c1.map(data.loc[month_filter & year_filter & mag_filter, ['latitude', 'longitude']])





c2.write('''### Map with filters, specifically for Oregon''')
c2.markdown('##')


or_boundary = data[data['latitude'].between(42,46.5) & data['longitude'].between(-135,-116.4)]

month_dd_o = c2.selectbox('Select the Month ', (month_num_dict.keys()))
year_dd_o = c2.selectbox('Select the Year ', range(int(or_boundary['year'].min()), int(or_boundary['year'].max() + 1)))

month_filter_o = data['month'] == month_num_dict[month_dd]

# month_input_o = c2.slider('Month Filter Oregon', int(or_boundary['month'].min()), int(or_boundary['month'].max()))
# year_input_o = c2.slider('Year Filter Oregon', int(or_boundary['year'].min()), int(or_boundary['year'].max()))
mag_input_o = c2.slider('Magnitude Filter Oregon (strengths greater than or equal to selected input)', int(or_boundary['mag'].min()), int(or_boundary['mag'].max()))

month_filter_o = or_boundary['month'] == month_num_dict[month_dd_o]
year_filter_o = or_boundary['year'] == year_dd_o
mag_filter_o = or_boundary['mag'] >= mag_input_o

c2.map(or_boundary.loc[month_filter_o & year_filter_o & mag_filter_o, ['latitude', 'longitude']])


"""
Looking at this map, the number of earthquakes in Oregon (including the areas off the coast) seem to have increased massively. I have graphed the number of earthquakes per year below as well, you can see that the number of earthquakes between 2020 and 2021 has increased by **over 350%.** 
"""

or_year_value_counts = or_boundary['year'].value_counts(sort=False, ascending = False)
or_year_value_counts = or_year_value_counts.reindex(index=year_value_counts.index[::-1])
or_year_value_dict = dict(or_year_value_counts) 

fig2 = plt.figure(figsize=(10,4))
plt.plot(or_year_value_dict.keys(), or_year_value_dict.values())
plt.xlabel("Year", fontsize=20)
plt.ylabel("Number of Earthquakes", fontsize=20)
plt.title("Number of Earthquakes per Year in Oregon", fontsize=20)
c2.pyplot(fig2)

"""
# Conclusions and Next Steps
"""

"""
My conclusion is that there **appears to be a significant uptick in earthquakes off the coast of Oregon in 2021** . Additionally, across the US, there has been a modest increase in earthquakes between 2019 and 2021 compared to 2011-2018, however, it looks  it looks like 2010 had higher number of earthquakes. It would not be fair to say there has been an increase in number of earthquakes across the US based on this analysis alone.
While I have come to this conclusion, there is certainly more work to be done. Please feel free to use the data below, or check out the [USGS website](https://www.usgs.gov/programs/earthquake-hazards/earthquakes) which has extensive information on earthquakes globally.
"""



"""
## Full dataframe for US earthquakes from 2010-2021 
"""
data

"## Full dataframe for Oregon earthquakes from 2010-2021"

or_boundary 

""" Thank you for visiting my streamlit app! I seek to update this page with additional features, please feel free to reach out at [bronsonnh@gmail](bronsonnh@gmail) or
we can chat on [LinkedIn](https://www.linkedin.com/in/nicholas-h-bronson-2b2b9774/) if you have any suggestions or thoughts on this app, or trends in earthquake prevalance."""
