import timeit
import json
import random
from faker import Faker

generator = Faker()

treat_list = [
	{"treat_name": "Abutment Tightening & Impression", "price": 0},
	{"treat_name": "Amalgam Filling", "price": 600000},
	{"treat_name": "Anterior Teeth Resin", "price": 1000000},
	{"treat_name": "Basic Care", "price": 0},
	{"treat_name": "Bite Wing X-Ray", "price": 100000},
	{"treat_name": "CBCT", "price": 250000},
	{"treat_name": "Canal Enlargement/Shaping", "price": 6000000},
	{"treat_name": "Canal Filling", "price": 6000000},
	{"treat_name": "Canal Irrigation", "price": 6000000},
	{"treat_name": "Cervical Resin", "price": 400000},
	{"treat_name": "Deciduous Tooth Extraction", "price": 100000},
	{"treat_name": "GI Filling", "price": 300000},
	{"treat_name": "Kontact (France) Implant", "price": 175000000},
	{"treat_name": "Metal Braces", "price": 45000000},
	{"treat_name": "Neo Biotech SL Implant", "price": 60000000},
	{"treat_name": "Oral Exam", "price": 0},
	{"treat_name": "Oral Prophylaxis", "price": 0},
	{"treat_name": "Orthodontics Diagnosis", "price": 0},
	{"treat_name": "PFM-Ni", "price": 10500000},
	{"treat_name": "Panorama", "price": 200000},
	{"treat_name": "Periapical X-Ray", "price": 100000},
	{"treat_name": "Periodontal Curettage", "price": 200000},
	{"treat_name": "Periodontal Probing Depths", "price": 0},
	{"treat_name": "Permanent Tooth Extraction", "price": 1000000},
	{"treat_name": "Posterial Teeth Resin", "price": 500000},
	{"treat_name": "Prosthesis Re-attachment", "price": 200000},
	{"treat_name": "Pulpectomy", "price": 6000000},
	{"treat_name": "Re-Endo", "price": 12000000},
	{"treat_name": "Root Planing", "price": 500000},
	{"treat_name": "Scailing", "price": 500000},
	{"treat_name": "Simple Bone Graft", "price": 4000000},
	{"treat_name": "Temporary Crown", "price": 0},
	{"treat_name": "Wisdom Tooth Extraction", "price": 6000000},
	{"treat_name": "Working Length", "price": 0}
]

clinic_list = [
	{"clinic_name": "Vatech", "address": "Hwasung", "telephone": "031-111-1111"},
	{"clinic_name": "Asan", "address": "Seoul", "telephone": "031-222-2222"},
	{"clinic_name": "Samsung", "address": "Yuljeon", "telephone": "031-333-3333"},
	{"clinic_name": "Wonkwang", "address": "Iksan", "telephone": "031-444-4444"}
]

patient_list = []


def gen_patient():
	print("Generating patient list...")
	for i in range(0, 100):
		patientJson = {
			"uuid4": generator.uuid4(),
			"patient_name": generator.name(),
			"age": generator.pyint(min_value=3, max_value=97),
			"sex": random.choice(["Male", "Female"]),
			}
		patient_list.append(patientJson)
	print("Successfully generated!")

if __name__ == "__main__":
	data = []
	num = 100000
	gen_patient()
	print("Making " + str(num) + " fake data...")
	start = timeit.default_timer()
	for i in range(0, num):
		dataAppend={
			"date": generator.date_between(start_date='-2y').strftime("%Y%m%d"),
			"patient": json.dumps(random.choice(patient_list)), # json.dumps는 json to string
			"dentist": generator.name(),
			"dental_clinic": json.dumps(random.choice(clinic_list)),
			"content": json.dumps(random.choice(treat_list)),
			"payment": random.choice(["Credit", "Cash"])
			}
		data.append(dataAppend)
	end = timeit.default_timer()
	print("Took " + str(end - start) + " seconds...")
	print("Now saving...")
	with open('data.json', 'w') as f:
		jsonData=json.dump(data, f)
