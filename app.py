from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET'])
@cross_origin()

def homepage():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
@cross_origin()

def index():
    if request.method == 'POST':
        try:

            women_occupation = request.form.get('women_occupation')
            women_occ_list = ['occ_2', 'occ_3', 'occ_4', 'occ_5', 'occ_6']
            women_list = []
            for i in women_occ_list:
                if i == women_occupation:
                    i = 1.0
                    women_list.append(i)
                else:
                    i = 0.0
                    women_list.append(i)

            husband_occupation = request.form.get('husband_occupation')
            hus_occ_list = ['occ_husb_2', 'occ_husb_3', 'occ_husb_4', 'occ_husb_5', 'occ_husb_6']
            hus_list = []
            for i in hus_occ_list:
                if i == husband_occupation:
                    i = 1.0
                    hus_list.append(i)
                else:
                    i = 0.0
                    hus_list.append(i)

            rate_marriage = request.form.get('rate_marriage')
            marriage = 0
            if rate_marriage == 'one':
                marriage = 1
            elif rate_marriage == 'two':
                marriage = 2
            elif rate_marriage == 'three':
                marriage = 3
            elif rate_marriage == 'four':
                marriage = 4
            elif rate_marriage == 'five':
                marriage = 5

            age = int(request.form['age'])
            yrs_married = float(request.form['yrs_married'])
            children = int(request.form['children'])
            religious = int(request.form.get('religious'))
                    
            education = request.form.get('education')
            edu = 0
            if education == 'grade_school':
                edu = 9.0
            elif education == 'high_school':
                edu = 12.0
            elif education == 'some_collage':
                edu = 14.0
            elif education == 'collage_graduate':
                edu = 16.0
            elif education == 'some_graduate_school':
                edu = 17.0
            elif education == 'advanced_degree':
                edu = 20.0

            new_list = women_list + hus_list
            new_list_one = [marriage, age, yrs_married, children, religious, edu]

            final_list = new_list + new_list_one

            print(final_list)

            new_model = pickle.load(open('women_affair.pickle', 'rb'))
            out_val = new_model.predict([final_list])

            if out_val == 1.0:
                result = "Women Have a Affair"
            else:
                result = "Women Don't have a Affair"

            return render_template('result.html', model_output=result)

        except Exception as e:
            print("The Exception is ", e)
            return "Something is going wrong...!"

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)