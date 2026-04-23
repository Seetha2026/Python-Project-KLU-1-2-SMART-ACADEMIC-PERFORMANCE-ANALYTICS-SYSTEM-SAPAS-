import csv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

FILE_NAME = "patients.csv"

class Patient:
    def __init__(self, pid, name, age, gender):
        self.id = pid
        self.name = name
        self.age = age
        self.gender = gender
        self.ward = None
        self.admission_date = None
        self.discharge_date = None
        self.cost = 0

    def display(self):
        print(f"{self.id} | {self.name} | {self.age} | {self.gender} | Ward: {self.ward}")

patients = []
wards = {"General": [], "ICU": [], "Private": []}

# Add Patient
def add_patient():
    try:
        pid = input("Enter Patient ID: ")
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        gender = input("Enter Gender: ")

        if age <= 0:
            print("Invalid age!")
            return

        p = Patient(pid, name, age, gender)
        patients.append(p)
        print("Patient added successfully!")

    except ValueError:
        print("Invalid input!")

# Assign Ward
def assign_ward():
    pid = input("Enter Patient ID: ")
    for p in patients:
        if p.id == pid:
            ward = input("Enter Ward (General/ICU/Private): ")
            if ward in wards:
                wards[ward].append(p)
                p.ward = ward
                print("Ward assigned!")
                return
    print("Patient not found!")

# Admit Patient
def admit_patient():
    pid = input("Enter Patient ID: ")
    for p in patients:
        if p.id == pid:
            p.admission_date = datetime.now()
            print("Patient admitted!")
            return
    print("Patient not found!")

# Discharge Patient
def discharge_patient():
    pid = input("Enter Patient ID: ")
    for p in patients:
        if p.id == pid:
            p.discharge_date = datetime.now()
            if p.admission_date:
                stay = (p.discharge_date - p.admission_date).days
                p.cost = stay * 1000
                print(f"Stay: {stay} days | Bill: {p.cost}")
            else:
                print("Patient was not admitted!")
            return
    print("Patient not found!")

# Display Patients
def display_patients():
    for p in patients:
        p.display()

# Save to CSV
def save_to_file():
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Age", "Gender", "Ward", "Cost"])
        for p in patients:
            writer.writerow([p.id, p.name, p.age, p.gender, p.ward, p.cost])
    print("Data saved!")

# Load from CSV
def load_from_file():
    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            p = Patient(row["ID"], row["Name"], int(row["Age"]), row["Gender"])
            p.ward = row["Ward"]
            p.cost = float(row["Cost"])
            patients.append(p)
    print("Data loaded!")

# Analytics
def analytics():
    if not os.path.exists(FILE_NAME):
        print("No data available!")
        return

    df = pd.read_csv(FILE_NAME)
    print("\n--- ANALYTICS ---")
    print("Average Age:", df["Age"].mean())
    print("Patients per Ward:\n", df["Ward"].value_counts())

    if "Cost" in df.columns:
        print("Total Cost:", df["Cost"].sum())

# Visualization
def visualization():
    if not os.path.exists(FILE_NAME):
        print("No data!")
        return

    df = pd.read_csv(FILE_NAME)

    # Bar chart
    plt.figure()
    df["Ward"].value_counts().plot(kind="bar")
    plt.title("Ward Distribution")
    plt.savefig("ward_chart.png")
    plt.show()

    # Pie chart
    if "Cost" in df.columns:
        plt.figure()
        df.groupby("Ward")["Cost"].sum().plot(kind="pie", autopct="%1.1f%%")
        plt.title("Cost Distribution")
        plt.ylabel("")
        plt.savefig("cost_chart.png")
        plt.show()

# Main Menu
def main():
    load_from_file()

    while True:
        print("\n--- HPRS MAIN MENU ---")
        print("1. Add Patient")
        print("2. Assign Ward")
        print("3. Admit Patient")
        print("4. Discharge Patient")
        print("5. Display Patients")
        print("6. Save Data")
        print("7. Analytics")
        print("8. Visualization")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            assign_ward()
        elif choice == "3":
            admit_patient()
        elif choice == "4":
            discharge_patient()
        elif choice == "5":
            display_patients()
        elif choice == "6":
            save_to_file()
        elif choice == "7":
            analytics()
        elif choice == "8":
            visualization()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()