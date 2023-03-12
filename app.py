from flask import *
import json
import pandas as pd
from sklearn.linear_model import LinearRegression


app= Flask(__name__)

@app.route('/forecastAccidents/',methods=['GET'])
def home_page():
    
    user_query=str(request.args.get('month'))
    
    df = pd.read_csv('monatszahlen2209_verkehrsunfaelle.csv')
    df = df[df['JAHR'] <= 2020]
    df.drop(['VORJAHRESWERT','VERÄND_VORMONAT_PROZENT','VERÄND_VORJAHRESMONAT_PROZENT','ZWÖLF_MONATE_MITTELWERT'],axis=1,inplace=True)
    df=df[df['MONAT']!= 'Summe']
    filtered_df = df[(df['MONATSZAHL'] == 'Alkoholunfälle') & (df['AUSPRÄGUNG'] == 'insgesamt')]
    filtered_df['MONAT']=pd.to_datetime(filtered_df['MONAT'],format='%Y%m')
    train_df = filtered_df[(filtered_df['MONAT'].dt.month != 12)].reset_index(drop=True)
    test_df = filtered_df[(filtered_df['MONAT'].dt.month == 12)].reset_index(drop=True)
    train_df['MONAT']=train_df['MONAT'].dt.month.astype(int)
    test_df['MONAT']=test_df['MONAT'].dt.month.astype(int)
    model = LinearRegression()
    X_train = train_df[['JAHR','MONAT']]
    y_train = train_df['WERT']
    model.fit(X_train, y_train)
    X_test = test_df[['JAHR','MONAT']]
    y_pred = model.predict(X_test)
    print('Predicted number of accidents in 2021:', y_pred[0])
    data_set={'Page':'Home','Message':"Hello",'Number of Accidents':y_pred[int(user_query)]}
    json_dump=json.dumps(data_set)

    return json_dump



if __name__ =='__main__':
    app.run(port=8080)
