#

from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy patient data storage
patients = []

# Define risk assessment function
def assess_risk(symptoms):
    severe_keywords = ["chest pain", "severe headache", "breathing difficulty"]
    for word in severe_keywords:
        if word in symptoms.lower():
            return "High Risk"
    return "Moderate Risk"

@app.route("/submit_patient_data", methods=["POST"])
def submit_patient():
    data = request.json
    name = data.get("name")
    symptoms = data.get("symptoms")

    risk_level = assess_risk(symptoms)
    patient_record = {"name": name, "symptoms": symptoms, "risk": risk_level}

    # Store the patient data
    patients.append(patient_record)

    # Send alert if high risk
    if risk_level == "High Risk":
        return jsonify({"message": "ALERT: Hospital Notified!", "risk": risk_level})
    
    return jsonify({"message": "Data Recorded", "risk": risk_level})

if __name__ == "__main__":
    app.run(port=5000)
