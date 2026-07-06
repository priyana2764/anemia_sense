from flask import Flask, render_template, request
import numpy as np
import pickle
import pandas as pd

app = Flask(__name__, static_url_path='/Flask/static')
model = pickle.load(open('model.pkl','rb'))  # Make sure your model.pkl is in same folder

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        gender = float(request.form['Gender'])
        hemoglobin = float(request.form['Hemoglobin'])
        mch = float(request.form['MCH'])
        mchc = float(request.form['MCHC'])
        mcv = float(request.form['MCV'])

        data = np.array([[gender, hemoglobin, mch, mchc, mcv]])
        df=pd.DataFrame(data, columns=['Gender', 'Hemoglobin', 'MCH', 'MCHC', 'MCV'])
        print(df)

        prediction = model.predict(df)
        print(prediction[0])
        result=prediction[0]

        if result == 0:
            message = "You don't have any Anemic Disease"
        else:
            message = "You have anemic disease"

        text="Hence, based on calculation: "
        return render_template('predict.html', prediction_text=text+str(message),data=data)
    
    return render_template('predict.html')
    
if __name__=="__main__":
    app.run(debug=False, port=5000)
