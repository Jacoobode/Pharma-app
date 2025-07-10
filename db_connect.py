import sys
import os
import sqlite3

def resource_path(path):
    try:

        base_path = sys._MEIPASS
    except AttributeError:

        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)


class DrugDataBase:
    CATEGORY_KEYWORDS = {
        "Painkiller": [
            "pain", "headache", "analgesic", "ache", "migraine", "toothache", "backache",
            "painkiller", "nsaid", "ibuprofen", "paracetamol", "acetaminophen", "diclofenac",
            "naproxen", "tramadol", "codeine", "morphine", "opioid", "analgesia"
        ],
        "Anti-inflammatory": [
            "inflammation", "anti-inflammatory", "arthritis", "swelling", "redness",
            "inflammatory", "cox inhibitor", "steroid", "corticosteroid", "prednisone",
            "methylprednisolone", "ibuprofen", "naproxen", "celecoxib", "celebrex"
        ],
        "Antipyretic": [
            "fever", "temperature", "antipyretic", "febrile", "chills", "pyrexia",
            "acetaminophen", "paracetamol", "aspirin", "acetylsalicylic acid", "naproxen"
        ],
        "Antibiotic": [
            "infection", "bacteria", "antibiotic", "antimicrobial", "penicillin",
            "amoxicillin", "ciprofloxacin", "doxycycline", "cephalexin", "erythromycin",
            "azithromycin", "clindamycin", "metronidazole", "vancomycin", "gentamicin"
        ],
        "Antihistamine": [
            "allergy", "antihistamine", "histamine", "hay fever", "urticaria",
            "rash", "itching", "cetirizine", "loratadine", "diphenhydramine",
            "fexofenadine", "hydroxyzine", "levocetirizine"
        ],
        "Antidepressant": [
            "depression", "antidepressant", "ssri", "snri", "fluoxetine", "sertraline",
            "paroxetine", "citalopram", "escitalopram", "mood", "anxiety",
            "bupropion", "mirtazapine", "tricyclic", "amitriptyline"
        ],
        "Antacid": [
            "acid", "heartburn", "reflux", "antacid", "indigestion", "gastric", "esophagus",
            "omeprazole", "lansoprazole", "ranitidine", "famotidine",
            "magnesium hydroxide", "aluminum hydroxide", "sodium bicarbonate"
        ],
        "Antiviral": [
            "virus", "antiviral", "herpes", "influenza", "hiv", "acyclovir", "oseltamivir",
            "valacyclovir"
        ],
        "Diuretic": [
            "diuretic", "water pill", "edema", "hypertension", "furosemide", "hydrochlorothiazide"
        ],
        "Anticoagulant": [
            "blood clot", "anticoagulant", "warfarin", "heparin", "dabigatran", "rivaroxaban", "bleeding"
        ],
        "Antipsychotic": [
            "schizophrenia", "psychosis", "antipsychotic", "haloperidol", "risperidone",
            "olanzapine", "quetiapine", "hallucination"
        ],
        "Bronchodilator": [
            "asthma", "bronchodilator", "albuterol", "salbutamol", "ipratropium", "copd", "wheezing"
        ],
        "Antiepileptic": [
            "seizure", "epilepsy", "antiepileptic", "valproate", "carbamazepine",
            "phenytoin", "levetiracetam"
        ],
        "Hormonal": [
            "hormone", "insulin", "thyroid", "estrogen", "testosterone", "corticosteroid", "contraceptive"
        ],
        "Vaccine": [
            "vaccine", "immunization", "immunize", "booster", "influenza vaccine",
            "covid vaccine", "hepatitis B vaccine"
        ],
        "Muscle relaxant": [
            "muscle spasm", "muscle relaxant", "baclofen", "cyclobenzaprine", "tizanidine"
        ],
        "Antifungal": [
            "fungus", "antifungal", "candidiasis", "fluconazole", "ketoconazole", "terbinafine"
        ],
    }

    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn is None:
            db_path = resource_path("drugs.db")
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn is not None:
            self.conn.close()


    def all_medicines(self):
        self.connect()
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM drugbank')
        result = cur.fetchall()
        return [dict(row) for row in result]
    def search_by_id(self,id):
        self.connect()
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM drugbank WHERE "drugbank-id"=?',(id,))
        result = cur.fetchone()
        return dict(result)

    def search_drugs_by_name(self, name_part):
        self.connect()
        cur = self.conn.cursor()
        like_pattern = f'%{name_part}%'
        cur.execute("SELECT * FROM drugbank WHERE name LIKE ?", (like_pattern,))
        result = cur.fetchall()
        return [dict(row) for row in result]

    def search_by_symptoms(self, query):
        self.connect()
        cur = self.conn.cursor()
        like_pattern = f'%{query}%'
        cur.execute('SELECT * FROM drugbank WHERE indication LIKE ?', (like_pattern,))
        result = cur.fetchall()
        return [dict(row) for row in result]

    def add_medicine(self, type, created, updated,name,description,state,indication,pharmacodynamics,
                     toxicity,absorption,volume_of_distr,food_interactions,mechanism_of_action):
        self.connect()
        cur = self.conn.cursor()
        try:
            cur.execute( """INSERT INTO drugbank (
             type,
             created,
             updated,
             name, 
             description,
             state,
             indication,
             pharmacodynamics,
             toxicity,
             absorption,
             "volume-of-distribution",
             "food-interactions",
             "mechanism-of-action") 
             VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?)""", (type, created, updated,name,description,state,indication,pharmacodynamics,
                     toxicity,absorption,volume_of_distr,food_interactions,mechanism_of_action))

            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_medicine(self, name):
        self.connect()
        cur = self.conn.cursor()
        try:
            cur.execute("DELETE FROM drugbank WHERE name = ?", (name,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting medicine: {e}")
            return False


    def detect_category(self, description):
        description = description.lower()
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description:
                    return category
        return "Other"

    def get_drugs_by_category(self, category_name):
        self.connect()
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM drugbank')
        drugs = cur.fetchall()
        result = []
        for drug in drugs:
            description = drug['description'] or ''
            category = self.detect_category(description)
            if category == category_name:
                drug_dict = dict(drug)
                drug_dict['category'] = category
                result.append(drug_dict)
        return result



