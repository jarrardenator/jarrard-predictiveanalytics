# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 23:47:43 2017

@author: Jeff
"""
import os
import pandas as pd
import numpy as np
import pandas_profiling


# 1 Create a single summary data set of ratings data using the data from all three years. 
# Import three files
    
sfo_2014 = pd.read_csv("SFO_2015.csv",parse_dates=True)
sfo_2015 = pd.read_csv("SFO_2015.csv", parse_dates=True)
sfo_2016 = pd.read_csv("SFO_2016.csv", parse_dates=True)

#Fix column names that need adjusting
sfo_2016 = sfo_2016.rename(index=str,columns={"*RESPNUM": "RESPNUM"})

#Add a Year column to each
sfo_2016['Year'] = 2016
sfo_2015['Year'] = 2015
sfo_2014['Year'] = 2014


#Append the files together with the common fields needed for Parts 2-4 into a Pandas dataframe
sfo_all = pd.concat([sfo_2014,sfo_2015,sfo_2016],ignore_index=True)

cols_part1 = ('RESPNUM','Year','CCGID','RUNID','INTDATE',
              'Q7ART','Q7FOOD','Q7STORE','Q7SIGN',
              'Q7WALKWAYS','Q7SCREENS','Q7INFODOWN',
              'Q7INFOUP','Q7WIFI','Q7ROADS','Q7PARK',
              'Q7AIRTRAIN','Q7LTPARKING','Q7RENTAL','Q7ALL',
              'Q9BOARDING','Q9AIRTRAIN','Q9RENTAL','Q9FOOD',
              'Q9RESTROOM','Q9ALL','Q10SAFE','Q12PRECHEKCRATE',
              'Q13GETRATE','Q14PASSTHRU','Q16LIVE')

sfo_part1 = pd.DataFrame(data=sfo_all,columns=cols_part1)

#c. profile new dataframe
#run the profiling and discuss

#d write to a new .csv file with initial header; reimport and check values
sfo_part1.to_csv("SFO_PART1.csv",header=True,index=True)

#test 
sfo_part1_test = pd.read_csv("SFO_PART1.csv",parse_dates=True)


# Part 2: Identify the top three comments made in 2015 and 2016
# Create a Comments dataset based on the information from the Data Dictionary for the comment codes
# 
sfo_part2 = sfo_all['Year'] >= 2015
sfo_part2 = sfo_all[sfo_part2]
cols_part2 = ('Q8COM1','Q8COM2','Q8COM3','Q8COM4','Q8COM5')
sfo_part2 = pd.DataFrame(data=sfo_part2,columns=cols_part2)

comments = []
for col in cols_part2:
    s = pd.Series(sfo_part2[col])
    s = s.dropna()
    comments.append(s)

comments = pd.concat(comments)
comments = pd.DataFrame(comments)
comments = comments.rename(columns={0:'CommentCode'})
comments['Count'] = 1
comments['CommentCode'] = comments.loc[:,('CommentCode')].astype('category')
comments = comments.pivot_table(values='Count',index='CommentCode',aggfunc=sum)
comments['TotalComments']=comments.Count.sum()
comments['Prop']=comments.Count/comments.TotalComments

top5comments = comments.sort_values(by='Count', ascending=False).head(5)

print(top5comments)


#Part 3:  Analyze the Q7ALL "SFO Rating as a whole" question by residence Home location

#set the columns
cols_part3 = ('RESPNUM','Year','RUNID','HOME','Q7ALL')
sfo_part3 = pd.DataFrame(data=sfo_all,columns=cols_part3)

sfo_part3 = sfo_part3[(sfo_part3.Q7ALL > 0) & (sfo_part3.Q7ALL < 6)]

sfo_part3_summary = sfo_part3.groupby(['Year','HOME'])
part3_stats = sfo_part3_summary['Q7ALL'].describe()
print(part3_stats)

#Part 4:  Create a targeting dataset
#Import the targeting data


select_resps_2017 = pd.read_csv("select_resps_2017.csv",parse_dates=True)
cols_part4_resps = ('RESPNUM','year')
select_resps_2017 = pd.DataFrame(data=select_resps_2017,columns=cols_part4_resps)
select_resps_2017 = select_resps_2017.rename(columns={"year" : "Year"})

cols_part4_demos = ('RESPNUM','Year','DESTGEO','DESTMARK','Q3PARK','Q4BAGS',
                    'Q4STORE','Q4FOOD','Q4WIFI','Q5TIMESFLOWN','Q5FIRSTTIME',
                    'Q6LONGUSE','Q18AGE','Q19GENDER','Q20INCOME','Q21FLY',
                    'Q22SJC','Q22OAK','LANG')

part4_demos = sfo_all[(sfo_all.Year >=2015)]
part4_demos=pd.DataFrame(data=part4_demos,columns=cols_part4_demos)


part4_targeting = pd.merge(select_resps_2017, part4_demos, how='inner', on=['RESPNUM', 'Year'])
print(part4_targeting.head(5))

