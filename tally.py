
import pre
import pandas as pd 

# import csv file
dfa=pd.read_csv(r"./athlete_events.csv")
dfr=pd.read_csv(r"./noc_regions.csv")

data1= pre.preprocess(dfa, dfr)
data1.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal","region"],inplace=True)


def yas(data1):
    # data1.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal","region"],inplace=True)
    year=data1["Year"].unique().tolist()
    year.sort()
    year.insert(0,"Overall")


    country=data1["region"].dropna().unique().tolist()
    country.sort()
    country.insert(0,"Overall")


    return year,country
   

# make another function for see the Analysis as user interest
def medal_tally(year,country):
    pr=data1
    flg=0
    if year=="Overall" and country=="Overall":
        pr=data1
    elif year=="Overall" and country !="Overall":
        flg=1
        pr=data1[data1["region"]==country]
    elif year !="Overall" and country =="Overall":
        pr=data1[data1["Year"]==year]
    elif year!="Overall" and country != "Overall":
        pr=data1[(data1["Year"]==year) & (data1["region"]==country)]

        
    if flg==1:
        x=pr.groupby("Year").sum()[["Gold","Silver","Bronze"]].sort_values("Year").reset_index()
    else:
        
        x=pr.groupby("region").sum()[["Gold","Silver","Bronze"]].sort_values("Gold",ascending=False)
        
    x["Total"]=x["Gold"]+x["Silver"]+x["Bronze"]
        
    return(x)    

# for graphical represantation
def graph(data,col):
    z=data.drop_duplicates(["Year",col])["Year"].value_counts().reset_index()
    x=z.sort_values("Year")
    return x


#  top 10 Athelets for particular sport
def top(data,sport):
    df=data.dropna(subset=["Medal"])
    
    if sport!="Overall":
        df=df[df["Sport"]==sport]
        
    x= df["Name"].value_counts().reset_index().merge(data,on="Name",how="left")[["Name","Sport","count","region"]].drop_duplicates("Name")
    x=x.head(10)
    return x 




def country(data,country):
    data.dropna(subset=["Medal"],inplace=True)
    data1=data[data["region"]==country]
    df=data1["Year"].value_counts().reset_index().sort_values("Year")
    return df



def top10(data,country):
    df=data.dropna(subset=["Medal"])
    
    
    df=df[df["region"]==country]
        
    x= df["Name"].value_counts().reset_index().merge(data,on="Name",how="left")[["Name","Sport","count"]].drop_duplicates("Name")
    x=x.head(10)
    return x 

def g(data,sport):
    df1=data.drop_duplicates(subset=["Name","region"])
    df1["Medal"].fillna("No Medal",inplace=True)

    if sport!="Overall":
        df=df1[df1["Sport"]==sport]
        return df
    else:
        return df1

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final




