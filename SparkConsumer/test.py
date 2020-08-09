#Imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sb
from scipy.io import loadmat,savemat
from scipy import sparse
import pickle
import os

# FUNCTIONS 

@st.cache
def dataLoader(exp,cond,tbase):
    rasterfile = "Data/E{0}_C{1}_T{2}".format(exp,cond,tbase)
    raster = sparse.load_npz(rasterfile+".npz")
    raster = raster.toarray()
    return raster,raster.shape[0]

@st.cache
def MutualInformation(exp,cond,tbase):
    mifile="Data/E{0}_C{1}_T{2}".format(exp,cond,tbase)
    print ("Returning PreComputed MIMatrix "+mifile.split("/")[-1])
    return np.load(mifile+".npy")

@st.cache
def cargarDataset(TP):
    with open("Data/Datasets/N{0}.json".format(TP)) as DD:
        dataset = loads(DD.readline())
    return dataset

@st.cache
def cargarMedidas(TP):
    f = open('Data/Measures/N{0}.pkl'.format(TP), 'rb')   # 'rb' for reading binary file
    medidas = pickle.load(f)     
    f.close()
    return medidas

def rankingMedidas(TP):
    p,pp =0,0
    medidas = cargarMedidas(TP)
    ranks = ["AvgRand","AvgIncRand","MI","RF","Corr"]
    NsR = [10,20,50,100,120,N-1]
    Ns = [4,5,6,7,8,9,10,20,50,100,120,N-1]
    norms = [np.linalg.norm(sum([np.array([medidas[(r,p,f,s,pp)][1][1] for f in M]) for s in range(ss)])/ss) for r,ss,M in [(0,5,NsR),(1,5,NsR),(2,1,Ns),(3,1,Ns),(4,1,Ns)]]
    norms = list(zip(ranks,norms))
    return list(zip(*sorted(norms,key=lambda x:x[1],reverse=True)))[0]

@st.cache
def stats(TP): #Avg SpRate, Sum(MI),Sum(D),Sum(C) & Ranks
    Dindex,Dsums = list(zip(*sorted(enumerate(np.sum(D,axis=1)),key=lambda x:x[1])))
    Cindex,Csums = list(zip(*sorted(enumerate(np.sum(CC,axis=1)),reverse=True,key=lambda x:x[1])))
    MIindex,MIsums = list(zip(*sorted(enumerate(np.sum(MI,axis=1)),reverse=True,key=lambda x:x[1])))
    SPindex,SPsums = list(zip(*sorted(enumerate(np.sum(RASTER,axis=1)),reverse=True,key=lambda x:x[1])))
    #for neuron in neurons:
    #    print("RF:{} - Cor:{} - MI:{} - SP:{}".format(MIindex.index(neuron),Cindex.index(neuron),Dindex.index(neuron),SPindex.index(neuron)))
    return [MIindex.index(TP),Cindex.index(TP),Dindex.index(TP),SPindex.index(TP)]
    #print("RF Distance:\n{0}\t#{1}\nSumMI:\n{2}\t#{3}\nSumCC\n{4}\t{5}".format(ds,Dsums.index(ds),ms,MIsums.index(ms),cs,Csums.index(cs)))


# CONSTANTS & LOADS

EXP = 0 # 0 1 2 3
COND = 3 # 0.issa 1.ifsa 2.wn 3.nm 4.ffsa 5. fssa
TBASE = 0.02 #0.001 = 1ms
RASTER = dataLoader(EXP,COND,TBASE)[0]
INTERVAL = 50 # para SpRate
N,T = RASTER.shape

D = loadmat("Data/rfOverlap.mat")["rfDist"][0][0]
MI = MutualInformation(EXP,COND,TBASE)
CC = np.corrcoef(RASTER[:50],RASTER[50:])**2-np.diag(np.ones(N))



# STREAMLIT UI
st.title("Retina Streamlit")
MS = st.sidebar.multiselect("Neuronas a observar",[2,10,20,31,49,72,119,120,127,147])

st.sidebar.markdown("""
**Abreviaciones**\n
**MI**: Información Mutua\n
**Cor**: Correlación\n
**RF**: Distancia campo receptivo\n
**SR**: Spike Rate\n
**Avg**: Promedio\n
**Inc**: Incremental\n
**Rand**: Aleatorio\n
""")

NsR = [10,20,50,100,120,N-1]
Ns = [4,5,6,7,8,9,10,20,50,100,120,N-1]


st.write("### Criterios de mejor predicción\n","|N|1er Criterio|2do Criterio|3er Criterio|4to Criterio|5to Criterio|\n|---|---|---|---|---|---|\n",
            "".join(["|{}".format(n)+"|{}|{}|{}|{}|{}|\n".format(*rankingMedidas(n)) for n in MS]))



for S in MS:
    medidas = cargarMedidas(S)
    t,m,p,pp = 1,1,0,0
    if 0:
        fig = plt.figure(figsize=(20,10))
        plt.xlabel("N");plt.ylabel("$R^2$")
        plt.plot(NsR,[medidas[(0,p,f,4,pp)][t][m] for f in NsR],"k.",label="Random")
        plt.plot(NsR,[medidas[(1,p,f,4,pp)][t][m] for f in NsR],"b-",alpha=0.3,label="Random I")
        for s in range(4):
            plt.plot(NsR,[medidas[(0,p,f,s,pp)][t][m] for f in NsR],"k.")
            plt.plot(NsR,[medidas[(1,p,f,s,pp)][t][m] for f in NsR],"b-",alpha=0.3)
        plt.plot(Ns,[medidas[(2,p,f,0,pp)][t][m] for f in Ns],"r-",alpha=0.3,label="MI")
        plt.plot(Ns,[medidas[(3,p,f,0,pp)][t][m] for f in Ns],"g-",alpha=0.3,label="RF")
        plt.plot(Ns,[medidas[(4,p,f,0,pp)][t][m] for f in Ns],"k-",alpha=0.3,label="Correl")
        plt.legend()
        plt.title("Neuron {0} - {2} {1}".format(S,"$R^2$","Spike Rate"))
        st.write(fig)
    

    fig = plt.figure(figsize=(20,10))
    plt.xlabel("N");plt.ylabel("$R^2$")
    rand = [np.array([medidas[(0,p,f,s,pp)][t][m] for f in NsR]) for s in range(5)]
    irand = [np.array([medidas[(1,p,f,s,pp)][t][m] for f in NsR]) for s in range(5)]
    stdrand = np.std(rand,axis=0)
    stdirand = np.std(irand,axis=0)
    plt.plot(NsR,sum(rand)/5,"k-",alpha=0.3,label="AvgRandom")
    plt.fill_between(NsR, sum(rand)/5 - stdrand, sum(rand)/5 + stdrand, alpha=0.05,color="k")
    plt.plot(NsR,sum(irand)/5,"b-",alpha=0.3,label="AvgRandom I")
    plt.fill_between(NsR, sum(irand)/5 - stdirand, sum(irand)/5 + stdirand, alpha=0.05,color="b")
    plt.plot(Ns,[medidas[(2,p,f,0,pp)][t][m] for f in Ns],"r-",alpha=0.3,label="MI")
    plt.plot(Ns,[medidas[(3,p,f,0,pp)][t][m] for f in Ns],"g-",alpha=0.3,label="RF")
    plt.plot(Ns,[medidas[(4,p,f,0,pp)][t][m] for f in Ns],"k-",alpha=0.3,label="Correl")
    plt.legend()
    plt.title("Neuron {0} - {2} {1}".format(S,"$R^2$","Spike Rate"))
    #plt.tight_layout()
    st.write(fig)


st.write("### Posiciónes en ranking\n","|N|MI|Cor|RF|SR|\n|---|---|---|---|---|\n",
            "".join(["|{}|".format(n)+"{}|{}|{}|{}|\n".format(*stats(n)) for n in MS]))
st.write()

rank = plt.figure(figsize=(18,9))
plt.subplot(4,1,1)
plt.title("Total Mutial Information",fontsize=18)
mirank = sorted(np.sum(MI,axis=1)/MI.shape[1],reverse=1)
plt.plot(range(MI.shape[0]),mirank,".")
for neuron in MS:
    plt.plot([mirank.index(np.sum(MI,axis=1)[neuron]/MI.shape[1])]*2,[0.0,0.002],alpha=0.5,label="Target N={0}".format(neuron))
plt.legend()
plt.subplot(4,1,2)
plt.title("Total Correlation",fontsize=18)
ccrank = sorted(np.sum(CC,axis=1)/CC.shape[1],reverse=1)
plt.plot(range(CC.shape[0]),ccrank,".")
for neuron in MS:
    plt.plot([ccrank.index(np.sum(CC,axis=1)[neuron]/CC.shape[1])]*2,[0.0,0.006],alpha=0.5,label="Target N={0}".format(neuron))
plt.legend()
plt.subplot(4,1,3)
plt.title("Total Receptive Field Distance",fontsize=18)
rfrank = sorted(np.sum(D,axis=1)/D.shape[1])
plt.plot(range(D.shape[0]),rfrank,".")
for neuron in MS:
    plt.plot([rfrank.index(np.sum(D,axis=1)[neuron]/D.shape[1])]*2,[0.0,6],alpha=0.5,label="Target N={0}".format(neuron))
plt.legend()
plt.subplot(4,1,4)
plt.title("Average Neuron activation",fontsize=18)
plt.ylabel("$<\sigma_i>$")
plt.xlabel("Neuron Ranking")
sprank = sorted(np.sum(RASTER,axis=1)/RASTER.shape[1],reverse=1)
plt.plot(range(RASTER.shape[0]),sprank,".")
for neuron in MS:
    plt.plot([sprank.index(np.sum(RASTER,axis=1)[neuron]/RASTER.shape[1])]*2,[0.0,1.0],alpha=0.5,label="Target N={0}".format(neuron))
plt.legend()
plt.tight_layout()
st.write(rank)


