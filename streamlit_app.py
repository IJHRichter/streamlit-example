import streamlit as st
import pandas as pd
import numpy as np
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
st.write("As I introduce myself to Streamlit, I've created this page to share a bit about me.")

st.subheader("Outside of work and school, I love hiking with my dog, Oliva.")
image = Image.open('Puppy.jpg')
st.image(image, caption='This is Olivia.')

#Display a video with a set start time 
st.subheader("But don't get me wrong, I also love cats. Press play to jump to a video of a kitten sneeze.")
video_url= "https://www.youtube.com/watch?v=ftgcwsBqS0U"
#start time in seconds 
st.video(video_url,start_time=13*60+48)

#Data Display
st.subheader("I love to travel. Here are the locations of some of my favorite trips from the last few years.")
#make a dataframe with the location name, long./lat., and month/year of trip. 
travel= pd.DataFrame({'location':['San Ignacio, Belize','Madrid','Glacier National Park','Atanta','San Fransisco','Bogota'],
'latitude':[17.1523,40.4168,48.7596,33.749,37.7749,4.711],
'longitude':[-89.0800,-3.7038,-113.787,-84.388,-122.4194,-74.07],
'date':[dt.datetime(2019,1,1),dt.datetime(2020,1,1),dt.datetime(2021,7,1),dt.datetime(2021,4,1),dt.datetime(2022,1,1),dt.datetime(2019,7,1)]
})

Ithtravel= pd.DataFrame({'location':['Ithaca','Buffalo','New York'],
'latitude':[42.444,42.8864,40.7128],
'longitude':[-76.5019,-78.8784,-74.006],
'date':[dt.datetime(2020,2,1),dt.datetime(2019,4,1),dt.datetime(2021,3,1)]
})
#use magic to print table
myTable= st.table(travel)

with st.expander("Expand to see the list of locations near Ithaca:"):
    st.experimental_show(Ithtravel)

checkIth= st.checkbox("Click to add locations near Ithaca to the above table.")
if checkIth:
    #modify the above table without printing out a new table
    myTable.add_rows(Ithtravel)
    travel= pd.concat([travel,Ithtravel],ignore_index=True)

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
    st.subheader(f"Here's a map of all trips in the last {month_filter} months.")
    st.map(filtered_data)

#When check mark is checked, switch the map to volcano data
showVolcanoes= st.checkbox("But enough about me, check to switch the map to show volcanoes around the world.")
if showVolcanoes:
    #hide the map without volcanoes 
    maps.empty()

    travelLoc= pd.DataFrame({'latitude':travel.loc[:,'latitude'],'longitude':travel.loc[:,'longitude']})
    
    #Use cache to store the volcano data 
    volcData= get_data('volcanoes.csv')
    volcLoc= pd.DataFrame({'latitude':volcData.loc[:,'latitude'],'longitude':volcData.loc[:,'longitude']})
    
    with maps.container():
        st.map(volcData)
    
    #practice combining data and display data as a dataframe
    st.write("Here is the full list of volcano locations along with my trip locations.")
    AllLoc= st.dataframe(travelLoc) 
    AllLoc.add_rows(volcLoc)
    

@st.experimental_memo
def set_fav_foods(fruit,veg):
    st.session_state["Fruit"]= fruit
    st.session_state["Veggie"]= veg

#Call function first with one set of inputs 
set_fav_foods("Banana","Peas")

#Use a form to have the user guess favorite foods 
st.write("Now that you have this detailed info about me, fill out this form to try guessing my favorite foods.")
with st.form("favFood_form"):
    fruit_val = st.selectbox("Favorite Fruit:",('Strawberry','Banana','Kiwi','Watermelon'))
    veg_val = st.selectbox("Favorite Vegetable:",('Brocolli','Carrot','Mushroom','Peas'))

    #include submit button 
    submitted = st.form_submit_button("Submit")
    if submitted:
        #by using experimental memo, function won't rerun if inputs haven't changed
        set_fav_foods(fruit_val,veg_val)
        st.write("Favorite Fruit:", fruit_val, "Favorite Vegetable:", veg_val)

#Pretend this check takes a long time by reading volcano data again
with st.spinner("Checking guess..."):
    datarepeat= pd.read_csv('volcanoes.csv')
    
st.success("Check Complete.")
if "Kiwi" in st.session_state["Fruit"]:
    if "Carrot" in st.session_state["Veggie"]:
        st.write("You're correct!")
        #show some baloons
        st.balloons()
else:
    st.write("Sorry try again.")
