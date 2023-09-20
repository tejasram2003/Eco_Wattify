import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error

dataframe = pd.read_csv('augmented_electricity_consumption.csv')

def train_price(dataframe):
    model = DecisionTreeRegressor()
    # dropping price and efficiency score columns
    x = dataframe.iloc[:,:-2].drop('House_Number',axis='columns')
    # using only the Cost_INR column
    y = dataframe.iloc[:,-1]

    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3,shuffle=True,random_state=42)

    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    print("Price Metrics")
    print(f"R2 Score: {r2_score(y_pred,y_test)}")
    print(f"Mean Squared Error: {mean_squared_error(y_pred,y_test)}")
    print(f"Mean absolute Error: {mean_absolute_error(y_test,y_pred)}")

    return model

def train_score(dataframe):
    model = DecisionTreeRegressor()
    # dropping price and efficiency score columns
    x = dataframe.iloc[:,:-2].drop('House_Number',axis='columns')
    # using only the is_efficient_score column
    y = dataframe.iloc[:,-2]

    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3,shuffle=True,random_state=42)

    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    print("Efficiency Score Metrics")
    print(f"R2 Score: {r2_score(y_pred,y_test)}")
    print(f"Mean Squared Error: {mean_squared_error(y_pred,y_test)}")
    print(f"Mean absolute Error: {mean_absolute_error(y_test,y_pred)}")

    return model

price_model = train_price(dataframe)
score_model = train_score(dataframe)

with open('decision_tree_model_price.pth','wb') as model_file:
    pickle.dump(price_model,model_file)

with open('decision_tree_model_score.pth','wb') as model_file:
    pickle.dump(score_model,model_file)