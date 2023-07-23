import pandas as pd 

dfa=pd.read_csv(r"./athlete_events.csv")
dfr=pd.read_csv(r"./noc_regions.csv")

# data preprocessing 
def preprocess(dfa,dfr):
# select only summer data
 dfa=dfa[dfa["Season"]=="Summer"]


# for merge dataset
 data=dfa.merge(dfr,on="NOC",how="left")


# for  drop_duplicates in dataframe
 data.drop_duplicates(inplace=True)



# for  get dummy variable one hot encoding use
 dummy = pd.get_dummies(data["Medal"],dtype=int)


# dummy variable and data  joint 
 data = pd.concat([data,dummy],axis=1)

 return data





