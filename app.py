from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline #get from predict_pipeline

application=Flask(__name__)

app=application

#home page route 
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST']) #both methohs allowed get to return the value and post to post(push) the values 
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    
    else: #create a object of the CustomData and then get the dataframe - get the values from the user over the web and then create df and then predict it 
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction") #then uusinf the dataframe predict the values

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df) 
        print("after Prediction")
        return render_template('home.html',results=results[0]) #rerurn in {{result}} jinja syntax
    

if __name__=="__main__":
    app.run(host="0.0.0.0")        


