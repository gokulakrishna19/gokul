from django.shortcuts import render
from .models import Realestate
from profiles.models import profiles

# Create your views here.
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
import pandas as pd
#from matplotlib import style
#import statistics
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#from collections import Counter
profile = profiles.objects.all()





saving = 0
inner= "minimum"
residential="avg_price"
commercial="max_price"

        
features = [
            
            
            
            'avg_growth',
            'minimum',
            'avg_price',
            'max_price'
            
            
            
            ]

def Status_Calc(minimum, avg_growth):
    
    #count=0
    price_1000sqft= minimum * 1000
    print(saving)
    if price_1000sqft<= saving:
        if avg_growth >= 5:
            #print( count+1)
           
            return 1
        
        else:
            return 0
    else:
        return 0
    

def Build_Data_Set(answer):
   


    if answer == "interior":
        types="minimum"
    elif answer == "residential":
        types="avg_price"
    elif answer == "commercial":
        types="max_price"


    data_df = pd.DataFrame.from_csv("real_estate.csv")
    
    
    data_df["Status2"] = list(map(Status_Calc, data_df[types], data_df["avg_growth"]))
    
    X = np.array(data_df[features].values)
    y = (data_df["Status2"].values)

    X = preprocessing.scale(X)
     
    return X,y
    

def Analysis(request):

    username = None
    if request.user.is_authenticated():
        username = request.user.username

    print(username)

    answer = "interior"
   
    if request.method == 'POST':
        answer = request.POST['type'] 
        print(answer)

    for p in profile:
        if p.username == username:
            csav = p.csaving



    global saving
    saving = csav

    X, y = Build_Data_Set(answer)
    #print (len(X))
   # print (y)
    
    clf = svm.SVC(kernel="linear", C= 1.0)
    clf.fit(X,y)
    
    #w = clf.coef_[0]
    #a = -w[0] / w[1]
    #xx = np.linspace(min(X[:, 0]), max(X[:, 0]))
    #yy = a * xx - clf.intercept_[0] / w[1]

    #plt.plot(xx,yy, "k-", label="non weighted")

    #plt.scatter(X[:, 0],X[:, 1],c=y)
    #plt.ylabel("Price")
    #plt.xlabel("growth")
    #plt.legend()

    #plt.show()
    
    
    data_df = pd.DataFrame.from_csv("real_estate.csv")
 
    #print( data_df[features])
   

    X = np.array(data_df[features].values)
    

    X = preprocessing.scale(X)

    Z = data_df["area"].values.tolist()
    

    invest_list = []

    for i in range(len(X)):
       
        p = clf.predict(X[i])[0]
        
       
        if p == 1:
            #print(Z[i])
            invest_list.append(Z[i])

    #print(len(invest_list))
    #print(invest_list)
    all_plans = Realestate.objects.all()
    #print(data_df.loc[data_df['area'].isin(invest_list)])
    
    #return invest_list
    return render(request, 'realestate/Real estate.html',{'plan':all_plans,'invest':invest_list, 'answer':answer })