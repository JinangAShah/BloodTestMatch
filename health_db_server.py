import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

db = []


def add_patient_to_db(name, id, blood_type):
    new_patient = {'name': name, 'id': id,
                   'blood_type': blood_type,
                   'tests': {}
                   }
    db.append(new_patient)
    return True


def init_server():
    add_patient_to_db('anne ables', 101, 'A+')
    add_patient_to_db('jinang shah', 202, 'B+')


@app.route('/add_patient', methods=["POST"])
def add_patient():
    in_data = request.get_json()
    answer, status_code = add_patient_driver(in_data)
    return jsonify(answer), status_code


def add_patient_driver(in_data):
    answer, status_code = add_valid_add_patient(in_data)
    if status_code != 200:
        return answer, status_code
    add_patient_to_db(in_data['name'], in_data['id'], in_data['blood_type'])
    print(db)
    return True, 200


def add_valid_add_patient(in_data):
    expected_keys = ['name', 'id', 'blood_type']
    expected_types = [str, int, str]
    for key, expected_type in zip(expected_keys, expected_types):
        if key not in in_data:
            error_message = 'Key {} is missing', format(key)
            return error_message, 400
        if type(in_data[key]) is not expected_types:
            error_message = 'Value of key {} is not in type {}'.format(key, expected_type)
        return error_message, 400
    return True, 200


@app.route('/get_results/<patient_id>', methods=['GET'])
def get_results(patient_id):
    answer, status_code = get_results_driver(patient_id)
    return answer, status_code


def get_results_driver(patient_id):
    answer, status_code = validate_patient_id(patient_id)
    if status_code != 200:
        return answer, status_code
    for patient in db:
        if patient['id'] == int(patient_id):
            return jsonify(patient['tests']), 200
    return "Patient is {} is not in database".format(patient_id), 400


def validate_patient_id(patient_id):
    try:
        patient_id_int = int(patient_id)
    except ValueError:
        return 'Patient_id was not an integer', 400
    return True, 200


if __name__ == "__main__":
    init_server()
    app.run()
