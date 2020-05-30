import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#setting up title of the page
st.title('Sentiment analysis of US airlines by tweets')
#streamlit supports markdown formatting it is similiar to how we write README
st.markdown('Uses streamlit to display dashboard and user dataset obtained from Kaggle')

#can easily make sidebar in streamlit
st.sidebar.title('Sentiment analysis of US airlines by tweets')
st.sidebar.markdown('Uses streamlit to display dashboard and user dataset obtained from Kaggle')

#loading the data everytime we run the app takes a toll on CPU memory #so we cache the data if it remains the same so it runs only when the #data is different
st.cache(persist = True)

#data url is defined seperately so that later if the data is on cloud, #can directly past the link here. It is stored as a tupple here
DATA_URL = ("C:/Users/Saumya/Desktop/Saumya/WebDev/Python/Streamlit/Tweets.csv")
def load_data():
    data = pd.read_csv(DATA_URL)
        #loading the data of column tweet_created onto a pandas format datetime
    data['tweet_created'] =pd.to_datetime(data['tweet_created'])
    return data
data = load_data()

st.sidebar.subheader("Show random Tweets")
#this creates a radio element with first argument giving explanation of what the radio element is for
#the next argument is a tupple of what radio points there would be
random_tweet = st.sidebar.radio('sentiment',('positive','neutral','negative'))

#displaying the random tweet by running a query in pandas and displaying it as a markdown
#query(a==b) => a is the column in the CSV file, b is the argument with which we are comparing
#[['text']] => We don't want the whole frame, just the text(tweet) associated with it
#sample(n=1) => Just gets 1 sample from the query
#iat[0,0] => to only get the required text and not anything else
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown('### Number of tweets by sentiments')
#since we will be using many selectboxs later, key=1 makes sure that this selectbox is unique
select = st.sidebar.selectbox('Visualization type',['Histogram','Pie Chart'], key=1)
#gets the total number of data in the column airline_sentiment
sentiment_count = data['airline_sentiment'].value_counts()
#making the data frame for above
sentiment_count_df = pd.DataFrame({
    'Sentiment' : sentiment_count.index,
    'Tweets' : sentiment_count.values
})

#Checkbox is originally true(so hide) if unchecked, show graph
if not st.sidebar.checkbox('Hide',True):
    st.markdown('### Number of Tweets by Sentiment')
    #choosing which graph to show
    if select == 'Histogram':
        fig = px.bar(sentiment_count_df,x='Sentiment',y='Tweets',color='Tweets',height=500) #height=500px
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count_df,values='Tweets',names='Sentiment')
        st.plotly_chart(fig)

#can easily show map by st.map(data) but looks too messy so would be breaking it down by time of the day
st.sidebar.markdown('### When and where are users Tweeting from?')

#slider(<Title>,<min value>,<max value>)
hour = st.sidebar.slider('Hour of day',0,24)
#hour = st.sidebar.number_input('Hour of day',min_value=1,max_value=24) #min_value always starts from 1

#modifying data to get by hour
modify_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('Close',True):
    st.markdown('### Tweets location based on the time of day')
    st.markdown('%i tweets between %i:00 and %i:00' % (len(modify_data),hour,(hour+1)%24)) #%24 so as to not get out-of-bounds data
    st.map(modify_data)
if st.sidebar.checkbox('Show raw data',False):
    st.write(modify_data)

st.sidebar.subheader('Breakdown of airline tweets by sentiment')
choice = st.sidebar.multiselect('Pick Airline',('US Airways','United','American','Southwest','Delta','Virgin America'))

if len(choice) > 0:

    #data.airline gets the airlines in the airline column in csv
    choice_data = data[data.airline.isin(choice)]

    #histfunc='count' counts all the data of the y-axis to get a number
    #facet_col because we can select multiple airlines so to genreate a new column for each 
    #labels just changed the name form airline_sentiment to tweets
    fig_choice = px.histogram(choice_data,x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment', facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'})
    st.plotly_chart(fig_choice)