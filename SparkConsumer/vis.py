from cassandra.cluster import Cluster
from time import sleep
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

cluster = Cluster(["localhost"])
session = cluster.connect("reddit")




def cargarDataset(sr):
    rows = session.execute("SELECT * from word_counter WHERE count > 100 AND subreddit = '{0}' ALLOW FILTERING".format(sr))
    data = [[row.subreddit,row.word,row.count,row.score] for row in rows]
    datacount = sorted(data,key=lambda x: x[2],reverse=True)[:25]
    datascore = sorted(data,key=lambda x: x[3],reverse=True)[:25]
    return pd.DataFrame(datacount,columns=["SubReddit","Word","Count","Score"]) , pd.DataFrame(datascore,columns=["SubReddit","Word","Count","Score"])

while False:
    rows = session.execute("SELECT * from word_counter WHERE count > 100 ALLOW FILTERING")
    data = [[row.subreddit,row.word,row.count,row.score] for row in rows]
    data = sorted(data,key=lambda x: x[2])
    print (data)
    sleep(5)


st.title("Reddit Comments")
sr = st.selectbox("Subreddit",["AskReddit","politics","reddit.com"])
counts,scores = cargarDataset(sr)
plt.subplot(1,2,1)
plt.title("Word Counts")
sns.barplot(y="Word", x="Count", data=counts)
plt.subplot(1,2,2)
plt.title("Word Scores")
sns.barplot(y="Word", x="Score", data=scores)
plt.tight_layout()
st.pyplot()