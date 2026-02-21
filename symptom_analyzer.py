# symptom_analyzer.py
import re
import random
import csv

# Further expanded database of health centers by area keyword
HEALTH_CENTERS = {
    "kolkata": ["NRS Medical College", "RG Kar Medical College", "Kolkata PHC Center"],
    "delhi": ["AIIMS Delhi", "Safdarjung Hospital", "Delhi Govt Dispensary"],
    "mumbai": ["JJ Hospital", "Sion Hospital", "Mumbai Health Center"],
    "chennai": ["Apollo Hospital Chennai", "Stanley Medical College", "Chennai PHC Center"],
    "bangalore": ["Bowring Hospital", "St. John's Medical College", "Bangalore Health Center"],
    "hyderabad": ["Osmania General Hospital", "Apollo Hyderabad", "Hyderabad PHC Center"],
    "pune": ["Sassoon Hospital", "Pune Health Center", "Ruby Hall Clinic"],
    "lucknow": ["KGMU Lucknow", "SGPGI", "Lucknow PHC Center"],
    "patna": ["Patna Medical College", "Nalanda Medical College", "Patna Health Center"],
    "jaipur": ["SMS Hospital Jaipur", "Jaipur PHC Center", "Fortis Jaipur"],
    "ahmedabad": ["Civil Hospital Ahmedabad", "Apollo Ahmedabad", "Ahmedabad PHC Center"],
    "chandigarh": ["PGIMER Chandigarh", "GMCH Chandigarh", "Chandigarh Health Center"],
    "bhopal": ["AIIMS Bhopal", "Bhopal Memorial Hospital", "Bhopal PHC Center"],
    "surat": ["Surat Municipal Hospital", "Surat PHC Center", "New Civil Hospital Surat"],
    "kanpur": ["Lala Lajpat Rai Hospital", "Kanpur PHC Center", "Regency Hospital Kanpur"],
    "indore": ["MY Hospital Indore", "Indore PHC Center", "Bombay Hospital Indore"],
    "nagpur": ["GMCH Nagpur", "Nagpur PHC Center", "Care Hospital Nagpur"],
    "visakhapatnam": ["KGH Visakhapatnam", "Visakhapatnam PHC Center", "Apollo Vizag"],
    "coimbatore": ["CMC Coimbatore", "Coimbatore PHC Center", "KG Hospital Coimbatore"],
    "thiruvananthapuram": ["Medical College Thiruvananthapuram", "Thiruvananthapuram PHC Center", "KIMS Hospital"],
    "ranchi": ["RIMS Ranchi", "Ranchi PHC Center", "Apollo Ranchi"],
    "guwahati": ["GMCH Guwahati", "Guwahati PHC Center", "Apollo Guwahati"],
    "amritsar": ["Civil Hospital Amritsar", "Amritsar PHC Center", "Fortis Amritsar"],
    "varanasi": ["BHU Hospital Varanasi", "Varanasi PHC Center", "Heritage Hospital Varanasi"],
    "agra": ["SN Medical College Agra", "Agra PHC Center", "Pushpanjali Hospital Agra"],
    "meerut": ["Meerut Medical College", "Meerut PHC Center", "Anand Hospital Meerut"],
    "ludhiana": ["DMCH Ludhiana", "Ludhiana PHC Center", "Fortis Ludhiana"],
    "nashik": ["Nashik Civil Hospital", "Nashik PHC Center", "Wockhardt Nashik"],
    "faridabad": ["BK Hospital Faridabad", "Faridabad PHC Center", "Metro Hospital Faridabad"],
    "rajkot": ["Civil Hospital Rajkot", "Rajkot PHC Center", "Synergy Hospital Rajkot"],
    "jodhpur": ["AIIMS Jodhpur", "Jodhpur PHC Center", "Medipulse Hospital Jodhpur"],
    "village": ["Village PHC Center", "Block Health Sub-Center", "Mobile Health Unit"],
    "default": ["Nearest Govt Health Center", "District Hospital", "Community Health Center"]
}

def get_nearest_health_center(symptoms: str):
    """Simple location mapping based on keyword (for demo purposes)."""
    text = symptoms.lower()
    for loc in HEALTH_CENTERS:
        if loc != "default" and loc in text:
            return random.choice(HEALTH_CENTERS[loc])
    if "rural" in text:
        return random.choice(HEALTH_CENTERS["village"])
    return random.choice(HEALTH_CENTERS["default"])


def analyze_symptoms(symptoms: str):
    """
    Expanded keyword-based symptom analyzer.
    Returns a dictionary with possible illness + nearest health center.
    """
    text = " ".join(symptoms.split()[:-1])
    illness = "Unknown - Please consult a doctor"

    illness = []
    with open('health_dataset.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if (text in row) and (row[0] not in illness):
                illness.append(row[0])
    if illness == []:
        illness = "Unknown - Please consult a doctor"
    else:
        illness = " / ".join(illness)

    # Get mock nearest health center
    health_center = get_nearest_health_center(symptoms)

    return {
        "illness": illness,
        "health_center": health_center
    }

{
    "illness": "Flu",
    "health_center": "City Hospital"
}