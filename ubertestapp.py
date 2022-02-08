import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px
import time 
from PIL import Image

@st.cache
def get_data(csv_path):
    #read data from given csv path
    data= pd.read_csv(csv_path)
    #Code from Streamlit Uber Test App for writing column names to lowercase
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

st.set_page_config(page_title="Isabel's First Project",
page_icon=':star:')
st.title("Fun Facts about Isabel")
st.write("To introduce myself to Streamlit, I've added a few components to this page to share a bit about me.")

st.subheader("Outside of work and school, I love hiking with my dog, Oliva.")
image = Image.open('Puppy.jpg')
st.image(image, caption='This is Olivia.')

#Display a video with a set start time 
st.subheader("I also love cats. Press play to jump to a video of a kitten sneeze.")
video_url= "https://www.youtube.com/watch?v=ftgcwsBqS0U"
#start time in seconds 
st.video(video_url,start_time=13*60+48)

#Data Display
st.subheader("I love to travel. Here are the locations of some of my favorite trips.")
#make a dataframe with the location name, long./lat., and month/year of trip. 
travel= pd.DataFrame({'location':['San Ignacio','Madrid','Glacier National Park'],
'latitude':[17.1523,40.4168,48.7596],
'longitude':[-89.0800,-3.7038,-113.787],
'date':[dt.datetime(2019,1,1),dt.datetime(2020,1,1),dt.datetime(2021,7,1)]
})

Ithtravel= pd.DataFrame({'location':['Ithaca','Buffalo'],
'latitude':[42.444,42.8864],
'longitude':[-76.5019,-78.8784],
'date':[dt.datetime(2020,2,1),dt.datetime(2019,4,1)]
})
with st.expander("Expand to check list of locations near Ithaca:"):
    st.experimental_show(Ithtravel)

st.write("Locations List")
myTable= st.table(travel)
checkIth= st.checkbox("Click to add locations near Ithaca.")
if checkIth:
    #modify the above table without printing out a new table
    myTable.add_rows(Ithtravel)

#calculate how many months it's been since the date of trip 
monthdiff=[]
for i in range(len(travel)):
    today= dt.datetime.now()
    monthdiff.append(12*(today.year-travel.loc[i,'date'].year)+(today.month-travel.loc[i,'date'].month))
travel['MonthsSince']=monthdiff

#display locations on map
maps= st.empty()
with maps.container():
    #include a slider to filter out non-recent trips
    month_filter = st.slider('Slide to filter the map by most to least recent trips.', 0, 48, 24)  # min: 0mo, max: 48mo, default: 24mo
    filtered_data = travel[travel['MonthsSince'] <= month_filter]
    st.subheader(f'Map of all trips in the last {month_filter} months.')
    st.map(filtered_data)

#When check mark is checked, overlay volcano data
showVolcanoes= st.checkbox("Check to switch to a map of volcanoes around the world.")
if showVolcanoes:
    #hide the map without volcanoes 
    maps.empty()

    travelLoc= pd.DataFrame({'latitude':travel.loc[:,'latitude'],'longitude':travel.loc[:,'longitude']})
    AllLoc= st.dataframe(travelLoc)

    volcData= get_data('volcanoes.csv')
    volcLoc= pd.DataFrame({'latitude':volcData.loc[:,'latitude'],'longitude':volcData.loc[:,'longitude']})
    
    with maps.container():
        st.map(volcData)
    
    #display volcano data as a dataframe
    st.write("Here is the full list of volcano locations and trip locations.")
    AllLoc.add_rows(volcLoc)
    
    #Include bar graph of locations of volcanos
    #Code for displaying loading text from Uber Test App code
    volc_loading= st.text("Loading Volcanoes by Region...") 
    st.write(px.bar(volcData,x='region')) 
    volc_loading.text("Here is the Volcano Count by Region of the World.")


@st.experimental_memo
def set_fav_foods(fruit,veg):
    st.session_state["Fruit"]= fruit
    st.session_state["Veggie"]= veg


set_fav_foods("Banana","Peas")
st.session_state

#if length of dataframe is less than complete, 
#st.progress(value between 0 and 100)

#copied test code for form from Streamlit example
st.write("Fill out the following form to guess my favorite foods.")
with st.form("favFood_form"):
    fruit_val = st.selectbox("Favorite Fruit:",('Strawberry','Banana','Kiwi','Watermelon'))
    veg_val = st.selectbox("Favorite Vegetable:",('Brocolli','Carrot','Mushroom','Peas'))

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        #by using experimental memo, function won't rerun if inputs haven't changed
        set_fav_foods(fruit_val,veg_val)
        st.write("Favorite Fruit:", fruit_val, "Favorite Vegetable:", veg_val)

#Pretend this check takes a long time 
with st.spinner("Checking guess..."):
    time.sleep(3)
st.success("Check Complete.")
if "Kiwi" in st.session_state["Fruit"]:
    if "Carrot" in st.session_state["Veggie"]:
        st.write("You're correct!")
        #show some baloons
        st.balloons()
else:
    st.write("Sorry try again.")