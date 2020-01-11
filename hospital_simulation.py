import random
import sqlite3
import os 

class Patient:
    def __init__(self,name):
        self.name = name
        self.disease = random.randint(1,5)
        self.health = random.randint(30,50)
        
    def take_damage(self):
        self.health = self.health - self.disease
        return self.health   
    def get_healed(self,healing_ab):
        self.health = self.health + healing_ab
        return self.health

class Dr:
    def __init__(self,name):
        self.name = name
        self.healing_ab = random.randint(1,7)
class Nurse:
    def __init__(self,name):
        self.name = name
        self.healing_ab = random.randint(-1,1)
        
name_list = ["Joseph","Michael","William","Helen","Sandra","Aaron","Adam","Emma","Olivia","Mia","Susan","Betty",
"Richard","Charles","Robert","John","David","Mary","Linda","Lisa","Amelia","Harper","Ella","Camilla","Victoria",
"William","Noah","Logan","Mason","Lucas","Daniel","Jackson","Carter","Luke","Isaac","Raylee","Nathaly","Tara","Elena"]

surname_list = ["Smith","Johnson","Williams","Jones","Brown","Davis","Miller","Wilson","Moore","Taylor","Anderson","Thomas",
"Jackson","White","Harris","Martin","Perez","Clark","Mitchel","Parker","Roberts","Gray","Gonzales","Watson","Russell",
"James","Campbell","Collins","Sanders","Hayes","Evans","Lewis","Lee","Walker","Peterson","Cox","Ward","Baker","Nelson"]

full_name_list = []
patient_list = []
nurse_list = []
dr_list = []
go_further = True

while go_further:
    name_of_db = input("Give the name of database ")
    try:
        name_of_db = str(name_of_db)
    except:
        print("it has to be string")
    if isinstance(name_of_db,str) == True and os.path.isfile(name_of_db+".db") == False:
        amount_of_patients = (input("Give the amount of patients max 13: "))
        try:
            amount_of_patients = int(amount_of_patients)
        except:
            print("Numbers only")
        if isinstance(amount_of_patients,int) == True and amount_of_patients <= 13 and amount_of_patients > 0:
            amount_of_dr = input("Give the amount of Dr max = amount of patients(rest is nurses) ")
            try:
                amount_of_dr = int(amount_of_dr)
            except:
                print("Numbers only")
            if isinstance(amount_of_dr,int) == True and amount_of_dr <= 13:
                amount_of_days = input("Give the amount of days each patient is going to spend in the hospital ")            
                try:
                    amount_of_days = int(amount_of_days)
                except:
                    print("Numbers only")
                if isinstance(amount_of_days,int) == True and amount_of_days > 0:
                    go_further = False
                else:
                    pass
            else:
                print("it has to be 13 less")
        else:
            print("it has to be 13 or less and more than 0")
    else:
        print("this database already exists")

conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__))+"\\"+name_of_db+".db")
c = conn.cursor()

random.shuffle(name_list)
random.shuffle(surname_list)
for i in range(0,amount_of_patients*3):
    full_name_list.append(f"{name_list[i]} {surname_list[i]}")   
for i in range(0,amount_of_patients):
    patient_list.append(Patient(full_name_list[i]))
    full_name_list.pop(i)
for i in range(0,amount_of_dr):
    dr_list.append(Dr(full_name_list[i]))
    full_name_list.pop(i)
for i in range(0,amount_of_patients-amount_of_dr):
    nurse_list.append(Nurse(full_name_list[i]))
    full_name_list.pop(i)

staff_list = nurse_list+dr_list
random.shuffle(staff_list)
    
def create_patient_col(patient_list):
    l = []
    for patient in patient_list:
        l.append(patient.name)
    return l
db_patient_list = create_patient_col(patient_list)
db_patient_list = list(map(lambda x: x.replace(" ",""),db_patient_list ))
first_col = db_patient_list[0]
db_patient_list.pop(0)
for day in range(amount_of_days):
    random.shuffle(staff_list)
    c.execute(f'CREATE TABLE IF NOT EXISTS Day{day}({first_col} TEXT)')
    for patient in db_patient_list:
        c.execute(f'ALTER TABLE Day{day} ADD '+ patient+" TEXT")
        conn.commit()
    patient_health_list = list(map(lambda x: str(x.health),patient_list))
    patient_health_inputs_db = ",".join(patient_health_list)
    patient_disease_list = list(map(lambda x: str(x.disease),patient_list))
    patient_disease_inputs_db = ",-".join(patient_disease_list)
    staff_name_list = list(map(lambda x: x.name,staff_list))
    staff_name_list = list(map(lambda x: x.replace(" ",""),staff_name_list))
    staff_name_list = list(map(lambda x: x.strip(),staff_name_list))
    staff_name_inputs_db = ','.join(staff_name_list)
    staff_helpheal_list = list(map(lambda x: str(x.healing_ab),staff_list))
    staff_helpheal_inputs_db = ','.join(staff_helpheal_list)
    c.execute(f'INSERT INTO Day{day} VALUES(-{patient_disease_inputs_db})')
    conn.commit()
    c.execute(f'INSERT INTO Day{day} VALUES({patient_health_inputs_db})')
    conn.commit()
    c.execute(f'INSERT INTO Day{day} VALUES({staff_helpheal_inputs_db})')
    conn.commit()
    for patient in patient_list:
        patient.take_damage()
        patient.get_healed(staff_list[patient_list.index(patient)].healing_ab)
    end_health_list = list(map(lambda x:str(x.health),patient_list))
    end_health_inputs_db = ','.join(end_health_list)
    c.execute(f'INSERT INTO Day{day} VALUES({end_health_inputs_db})')
    conn.commit()
c.close()
conn.close()
