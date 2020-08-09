from cassandra.cluster import Cluster
from time import sleep
import streamlit as st
import seaborn as sns
import pandas as pd

cluster = Cluster(["localhost"])
session = cluster.connect("reddit")




def cargarDataset(sr):
    rows = session.execute("SELECT * from word_counter WHERE count > 100 AND subreddit = '{0}' ALLOW FILTERING".format(sr))
    data = [[row.subreddit,row.word,row.count,row.score] for row in rows]
    data = sorted(data,key=lambda x: x[2],reverse=True)[:25]
    return pd.DataFrame(data,columns=["SubReddit","Word","Count","Score"])

while False:
    rows = session.execute("SELECT * from word_counter WHERE count > 100 ALLOW FILTERING")
    data = [[row.subreddit,row.word,row.count,row.score] for row in rows]
    data = sorted(data,key=lambda x: x[2])
    print (data)
    sleep(5)


st.title("Reddit Comment")
sr = st.selectbox("Subreddit",["AskReddit","politics","reddit.com"])
pddf = cargarDataset(sr)
sns.barplot(y="Word", x="Count", data=pddf)
st.pyplot()