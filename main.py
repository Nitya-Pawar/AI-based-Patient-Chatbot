import pandas as pd
import qrcode
import os
from huggingface_hub import InferenceClient

# Initialize Hugging Face Inference Client
client = InferenceClient(
    provider="novita",
    api_key="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",
)

file_name = "patientlist.csv"
df = pd.read_csv(file_name) if os.path.exists(file_name) else pd.DataFrame(
    columns=["Name", "Age", "Condition", "Risk_Level", "Contact", "Emergency_Contact", "Allergies"])

def save_data():
    df.to_csv(file_name, index=False)

def add_patient(name, age, condition, contact, emergency_contact, allergies):
    risk_level = predict_risk(age, condition)
    new_patient = {"Name": name, "Age": age, "Condition": condition, "Risk_Level": risk_level,
                   "Contact": contact, "Emergency_Contact": emergency_contact, "Allergies": allergies}
    global df
    df = pd.concat([df, pd.DataFrame([new_patient])], ignore_index=True)
    save_data()
    generate_qr(name,contact,age,emergency_contact,allergies)
    print("Patient details added successfully")

def delete_patient(name):
    global df
    df = df[df['Name'] != name]
    save_data()

def update_patient(name, key, value):
    global df
    df.loc[df['Name'] == name, key] = value
    save_data()

def search_patient_by_name(name):
    return df[df['Name'] == name]

def search_patient_by_contact(contact):
    return df[df['Contact'] == contact]

def predict_risk(age, condition):
    if age > 60 or "heart" in condition.lower() or "diabetes" in condition.lower():
        return "High"
    elif 40 < age <= 60 or "hypertension" in condition.lower():
        return "Moderate"
    return "Low"

def generate_qr(name,contact,age,emergency_contact,allergies):
    qr_data = f"Patient Name: {name}\nContact:{contact}\nAge:{age}\nEmergengy contact:{emergency_contact}\nAllergies:{allergies}"
    qr = qrcode.make(qr_data)
    qr.save(f"{name}_QR.png")

def ai_chatbot(prompt):
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500,
    )
    output_content = completion.choices[0].message.content
    print(f"BOT : {output_content}")

# def chat(prompt) :
#     completion = client.chat.completions.create(
#         model="deepseek-ai/DeepSeek-V3-0324",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         max_tokens=500,
#     )
#     output_content = completion.choices[0].message.content
#     print(f"BOT : {output_content}")





def display_menu():
    print("\nHospital Management System")
    print("1. Add Patient")
    print("2. Delete Patient")
    print("3. Update Patient Info")
    print("4. Search Patient by Name")
    print("5. Search Patient by Contact")
    print("6. AI Chatbot")
    print("7. Exit")


PROMPT = ''

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            condition = input("Enter Condition: ")
            contact = input("Enter Contact: ")
            emergency_contact = input("Enter Emergency Contact: ")
            allergies = input("Enter Allergies: ")
            add_patient(name, age, condition, contact, emergency_contact, allergies)
            generate_qr(name,contact,age,emergency_contact,allergies)
        elif choice == "2":
            name = input("Enter Name to Delete: ")
            delete_patient(name)
        elif choice == "3":
            name = input("Enter Name: ")
            key = input("Enter Field to Update: ")
            value = input("Enter New Value: ")
            update_patient(name, key, value)
        elif choice == "4":
            name = input("Enter Name to Search: ")
            print(search_patient_by_name(name))
        elif choice == "5":
            contact = input("Enter Contact to Search: ")
            print(search_patient_by_contact(contact))
        elif choice == "6":
            state = True
            while state:

                print("Welcome to AI ChatBot")
                PROMPT = input("YOU : ")
                if PROMPT == 'exit':
                    print("Bye")
                    state = False
                    break
                ai_chatbot(PROMPT)



        elif choice == "7":
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()

