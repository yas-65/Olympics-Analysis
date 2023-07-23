import streamlit as st 
import pre
import pandas as pd
# import medal
import tally
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns


#import CSV file
dfa=pd.read_csv(r"./athlete_events.csv")
dfr=pd.read_csv(r"./noc_regions.csv")

data= pre.preprocess(dfa,dfr)
data.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal","region"],inplace=True)

#make UI
st.sidebar.title("Olympics Analysis")

# here 4 option user can select anyone and see Analysis
user_menu=st.sidebar.radio(
     "Select An Option",
    ("Medal Tally","Overall Analysis","Country Wise Analysis","Athlete Wise Analysis ")
)


# if user selected Medal Tally
if user_menu=="Medal Tally":
    st.sidebar.header("Medal Tally")
   
# for select year and country (yas) function called from tally.py
    year,country=tally.yas(data)
    

    select_year=st.sidebar.selectbox("Select year", year)
    select_country=st.sidebar.selectbox("Select country",country)


# function (Medal_Tally) called from tally.py to see the Analysis as per user interest.
    w=tally.medal_tally(select_year, select_country)

    if select_year=="Overall" and select_country=="Overall":
        st.title("Overall Analysis ")
    
    elif select_year !="Overall" and select_country=="Overall":
        st.title("All country performance in "+ str(select_year))

    elif select_year=="Overall" and select_country !="Overall":
        st.title( select_country + " Performance in all Olympics")

    elif select_year!="Overall" and select_country!="Overall":
        st.title(str(select_year) + " Medal Tally of " + select_country) 

    st.table(w)

# if user select Overall Analysis
data5=pre.preprocess(dfa, dfr)

if user_menu=="Overall Analysis":


    y=data5["Year"].unique().shape[0]
    c=data5["City"].unique().shape[0]
    e=data5["Event"].unique().shape[0]
    a=data5["Name"].unique().shape[0]
    r=data5["region"].unique().shape[0]
    s=data5["Sport"].unique().shape[0]

    st.title("Top Statistics")
    c1,c2,c3=st.columns(3)
    with c1:
        st.header("Editions")
        st.title(y)
    with c2:
        st.header("Hosts")
        st.title(c)
    with c3:
        st.header("Events")
        st.title(e)
    c4,c5,c6=st.columns(3)
    with c4:
        st.header("Athletes")
        st.title(a)
    with c5:
        st.header("Nations")
        st.title(r)
    with c6:
        st.header("Sports")
        st.title(s)


    # graphical represantation of Participating Nation Over The Years 
        
    st.header("Participating Nation Over The Years ")
    z=tally.graph(data5,"region").rename(columns={"count":"No of Nation"})
    fig = px.line(z,x="Year",y="No of Nation")
    st.plotly_chart(fig)
    # x=plt.plot(z["Year"],z["count"])
    # st.pyplot(x)


    # graphical represantation of Total Event Over The Year

    st.header("Total Event Over The Year")
    z=tally.graph(data5,"Event").rename(columns={"count":"No of event"})
    fig=px.line(z,x="Year",y="No of event")
    st.plotly_chart(fig)


    # graphical represantation of Athelets Over The Year
    st.header("Athelets Over The Year")
    z=tally.graph(data5,"Name").rename(columns={"count":"No of Athelets"})
    fig=px.line(z,x="Year",y="No of Athelets")
    st.plotly_chart(fig)


    # Top 10 Athelets for particular sport
    st.header("Top Athelets")

    sport=data5["Sport"]
   
    sport_list=sport.unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")
    selected_sport=st.selectbox("Select Sport",sport_list)
   
    # for see the top 10 Athelets from particular sport (top)function call from tally.py
    x=tally.top(data5,selected_sport).reset_index()
    x=x.drop(["index"],axis=1)
    
    st.table(x)

# if user select Country wise Analysis
if user_menu=="Country Wise Analysis":
    st.sidebar.title("Country Wise Analysis")
    country=data["region"].dropna().unique().tolist()
    country.sort()
    selected_country=st.sidebar.selectbox("select country",country)
    df=tally.country(data,selected_country).rename(columns={"count":"Medal"})
    fig=px.line(df,x="Year",y="Medal")
    st.title(selected_country+ " Medal Tally Overthe Year")
    st.plotly_chart(fig)


    x=tally.top10(data5,selected_country).reset_index()
    x=x.drop(["index"],axis=1)
    st.title( " Top  Athelethecis of " + selected_country )
    
    st.table(x)

if user_menu=="Athlete Wise Analysis ":
    df1=data5.drop_duplicates(subset=["Name","region"])
    
    x1=df1["Age"].dropna()
    x2=df1[df1["Medal"]=="Gold"]["Age"].dropna()
    x3=df1[df1["Medal"]=="Silver"]["Age"].dropna()
    x4=df1[df1["Medal"]=="Bronze"]["Age"].dropna()

   
    fig=ff.create_distplot([x1,x2,x3,x4],["Overall Age","Gold Medalist","Silver Medalist","Bronze Medalist"],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=800)
    st.title("Distribution of Age")

    st.plotly_chart(fig)
    x=[]
    name=[]
    fsport=['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton']

    for sport in fsport:
        df=data5[data5["Sport"]==sport]
        x.append(data5[data5["Medal"]=="Gold"]["Age"].dropna())
        name.append(sport)

    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,height=1000,width=800)
    st.title("Distribution Of Age for Gold Medalist")
    st.plotly_chart(fig)
    st.title("weight vs Height") 
    selectc=data5["Sport"].unique().tolist()
    selectc.sort()
    selectc.insert(0,"Overall")

    s=st.selectbox("Select Sport",selectc)
    z=tally.g(data5,s)

    
    fig,ax=plt.subplots()
    ax = sns.scatterplot(x="Weight",y="Height",data=z,hue=z["Medal"],style=z["Sex"])
    st.pyplot(fig)


    st.title("Man vs Women Participation Over The Year")
    dat=tally.men_vs_women(data5)    
    fig=px.line(dat,x="Year",y=["Male","Female"])
    st.plotly_chart(fig)
