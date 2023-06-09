from flask import Flask, render_template, request
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the pincode data from the CSV file
pincode_data = pd.read_csv(r"Locality_village_pincode_final_mar-2017.csv", encoding="latin-1", low_memory=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_state = request.form['state']
        selected_district = request.form['district']
        selected_taluka = request.form['taluka']
        selected_village = request.form['village']
        selected_bo = request.form['bo']
        selected_landmark = request.form['landmark']
        selected_co = request.form['co']
        if (len(selected_landmark)==0)and(len(selected_co)==0):
            # Get the pincode based on the selected options
            pincode = get_pincode(selected_state, selected_district, selected_taluka, selected_village, selected_bo)
            return render_template('result.html', pincode=pincode)
        elif (len(selected_co)==0):
            # Get the pincode based on the selected options
            pincode = get_pincode_Landmark(selected_state, selected_district, selected_taluka, selected_village, selected_bo, selected_landmark)
            return render_template('result.html', pincode=pincode)
        elif (len(selected_landmark)==0):
            # Get the pincode based on the selected options
            pincode = get_pincode_co(selected_state, selected_district, selected_taluka, selected_village, selected_bo, selected_co)
            return render_template('result.html', pincode=pincode)
        else:
            pincode = get_pincode_Landmark_co(selected_state, selected_district, selected_taluka, selected_village, selected_bo, selected_co, selected_landmark)
            return render_template('result.html', pincode=pincode)


    # Get unique states from the pincode data
    states = pincode_data['StateName'].unique()
    states.sort()
    return render_template('index.html', states=states)

@app.route('/districts', methods=['POST'])
def get_districts():
    selected_state = request.form['state']
    districts = pincode_data[pincode_data['StateName'] == selected_state]['Districtname'].unique()
    districts.sort()
    print(districts.tolist())
    return {'districts': districts.tolist()}

@app.route('/talukas', methods=['POST'])
def get_talukas():
    selected_state = request.form['state']
    selected_district = request.form['district']
    talukas = pincode_data.loc[(pincode_data['StateName'] == selected_state) & (pincode_data['Districtname'] == selected_district), 'Sub-distname'].unique()
    talukas.sort()
    return {'talukas': talukas.tolist()}

@app.route('/villages', methods=['POST'])
def get_villages():
    selected_state = request.form['state']
    selected_district = request.form['district']
    selected_taluka = request.form['taluka']
    selected_bo = request.form['bo']
    # Filter the pincode data to get villages for the selected state, district, and taluka
    villages = pincode_data.loc[(pincode_data['StateName'] == selected_state) & (pincode_data['Districtname'] == selected_district) & (pincode_data['Sub-distname'] == selected_taluka) &(pincode_data['Officename']==selected_bo), 'Village/Locality'].unique()
    villages.sort()
    return {'villages': villages.tolist()}

@app.route('/bos', methods=['POST'])
def get_bos():
    selected_state = request.form['state']
    selected_district = request.form['district']
    selected_taluka = request.form['taluka']
    # selected_village = request.form['village']
    # Filter the pincode data to get B.Os for the selected state, district, taluka, and village
    bos = pincode_data.loc[(pincode_data['StateName'] == selected_state) & (pincode_data['Districtname'] == selected_district) & (pincode_data['Sub-distname'] == selected_taluka), 'Officename'].unique()
    bos.sort()
    return {'bos': bos.tolist()}

@app.route('/pincode', methods=['POST'])
def get_pincode(selected_state, selected_district, selected_taluka, selected_village, selected_bo):
    selected_state = request.form['state']
    selected_district = request.form['district']
    selected_taluka = request.form['taluka']
    selected_village = request.form['village']
    selected_bo = request.form['bo']

    # Filter the pincode data to get the pincode for the selected options
    pincode = pincode_data.loc[(pincode_data['StateName'] == selected_state) & (pincode_data['Districtname'] == selected_district) & (pincode_data['Sub-distname'] == selected_taluka) & (pincode_data['Village/Locality'] == selected_village) & (pincode_data['Officename'] == selected_bo), 'Pincode'].values[0]
    address= "At - "+selected_village+", Post - "+selected_bo+", Taluka - "+selected_taluka+", District - "+selected_district+", State - "+selected_state+", Pincode- "+str(pincode)
    return address

@app.route('/pincode', methods=['POST'])
def get_pincode_Landmark(selected_state, selected_district, selected_taluka, selected_village, selected_bo, selected_landmark):
    selected_state = request.form['state']
    selected_district = request.form['district']
    selected_taluka = request.form['taluka']
    selected_village = request.form['village']
    selected_bo = request.form['bo']
    selected_landmark = request.form['landmark']

    # Filter the pincode data to get the pincode for the selected options
    pincode = pincode_data.loc[(pincode_data['StateName'] == selected_state) & (pincode_data['Districtname'] == selected_district) & (pincode_data['Sub-distname'] == selected_taluka) & (pincode_data['Village/Locality'] == selected_village) & (pincode_data['Officename'] == selected_bo), 'Pincode'].values[0]
    address= "At - "+selected_village+", Post - "+selected_bo+", Landmark - " +selected_landmark+", Taluka - "+selected_taluka+", District - "+selected_district+", State - "+selected_state+" Pincode - "+str(pincode)
    return address

@app.route('/pincode', methods=['POST'])
def get_pincode_Landmark_co(selected_state, selected_district, selected_taluka, selected_village, selected_bo, selected_co, selected_landmark):
    selected_state = request.form['state']
    selected_district = request.form['district']
    selected_taluka = request.form['taluka']
    selected_village = request.form['village']
    selected_bo = request.form['bo']
    selected_landmark = request.form['landmark']
    selected_co = request.form['co']

    # Filter the pincode data to get the pincode for the selected options
    pincode = pincode_data.loc[(pincode_data['StateName'] == selected_state) & (pincode_data['Districtname'] == selected_district) & (pincode_data['Sub-distname'] == selected_taluka) & (pincode_data['Village/Locality'] == selected_village) & (pincode_data['Officename'] == selected_bo), 'Pincode'].values[0]
    address= "C/o - "+selected_co+", At - "+selected_village+", Post - "+selected_bo+", Landmark - " +selected_landmark+", Taluka - "+selected_taluka+", District - "+selected_district+", State - "+selected_state+" Pincode - "+str(pincode)
    return address

@app.route('/pincode', methods=['POST'])
def get_pincode_co(selected_state, selected_district, selected_taluka, selected_village, selected_bo, selected_co):
    selected_state = request.form['state']
    selected_district = request.form['district']
    selected_taluka = request.form['taluka']
    selected_village = request.form['village']
    selected_bo = request.form['bo']
    selected_co = request.form['co']

    # Filter the pincode data to get the pincode for the selected options
    pincode = pincode_data.loc[(pincode_data['StateName'] == selected_state) & (pincode_data['Districtname'] == selected_district) & (pincode_data['Sub-distname'] == selected_taluka) & (pincode_data['Village/Locality'] == selected_village) & (pincode_data['Officename'] == selected_bo), 'Pincode'].values[0]
    address= "C/o - "+selected_co+", At - "+selected_village+", Post - "+selected_bo+", Taluka - "+selected_taluka+", District - "+selected_district+", State - "+selected_state+" Pincode - "+str(pincode)
    pincode_data.loc[(pincode_data['StateName'] == selected_state) & (pincode_data['Districtname'] == selected_district) & (pincode_data['Sub-distname'] == selected_taluka) & (pincode_data['Village/Locality'] == selected_village) & (pincode_data['Officename'] == selected_bo), 'Pincode'].values[0]
    return address


if __name__ == '__main__':
    app.run(debug=True)
