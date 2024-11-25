from flask import Flask, request, jsonify
from google.cloud import storage
import joblib
import numpy as np
import os
import pandas as pd

# Configuración de la base de datos
DB_USER = "postgres"
DB_PASSWORD = "hola123xd"
DB_NAME = "db-descriptions"
DB_HOST = "104.154.188.102"  # IP pública de la instancia de Cloud SQL
DB_PORT = "5432"

# Conexión a la base de datos
engine = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = Flask(__name__)

# Configuración del bucket y carpeta
BUCKET_NAME = "ezapataa1-models-bucket"
MODELS_FOLDER = "modelos_entrenados"

# Nombre de todos los síntomas
symptom_names = [
    "sharp abdominal pain",
    "vomiting",
    "cough",
    "headache",
    "back pain",
    "nausea",
    "fever",
    "sharp chest pain",
    "shortness of breath",
    "abnormal appearing skin",
    "leg pain",
    "skin swelling",
    "nasal congestion",
    "dizziness",
    "sore throat",
    "depressive or psychotic symptoms",
    "lower abdominal pain",
    "ear pain",
    "low back pain",
    "weakness",
    "skin rash",
    "skin lesion",
    "skin growth",
    "burning abdominal pain",
    "itching of skin",
    "arm pain",
    "hip pain",
    "loss of sensation",
    "depression",
    "insomnia",
    "side pain",
    "skin dryness, peeling, scaliness, or roughness",
    "neck pain",
    "anxiety and nervousness",
    "diminished vision",
    "abnormal involuntary movements",
    "hostile behavior",
    "diarrhea",
    "peripheral edema",
    "coryza",
    "chest tightness",
    "itchiness of eye",
    "acne or pimples",
    "problems with movement",
    "irregular appearing scalp",
    "delusions or hallucinations",
    "painful urination",
    "knee pain",
    "heartburn",
    "difficulty breathing",
    "shoulder pain",
    "abusing alcohol",
    "lacrimation",
    "excessive anger",
    "pelvic pain",
    "temper problems",
    "facial pain",
    "symptoms of eye",
    "paresthesia",
    "lower body pain",
    "pain in eye",
    "retention of urine",
    "foot or toe pain",
    "chills",
    "suprapubic pain",
    "skin moles",
    "blood in stool",
    "allergic reaction",
    "hand or finger pain",
    "ache all over",
    "leg swelling",
    "frequent urination",
    "upper abdominal pain",
    "difficulty speaking",
    "drug abuse",
    "diminished hearing",
    "plugged feeling in ear",
    "decreased appetite",
    "swollen eye",
    "eye redness",
    "lip swelling",
    "skin irritation",
    "elbow pain",
    "vaginal discharge",
    "cramps and spasms",
    "wheezing",
    "fatigue",
    "fears and phobias",
    "fluid retention",
    "blood in urine",
    "white discharge from eye",
    "fainting",
    "sweating",
    "fluid in ear",
    "irregular heartbeat",
    "spots or clouds in vision",
    "disturbance of memory",
    "pulling at ears",
    "palpitations",
    "hand or finger swelling",
    "focal weakness",
    "wrist pain",
    "problems during pregnancy",
    "rectal bleeding",
    "intermenstrual bleeding",
    "foreign body sensation in eye",
    "ankle pain",
    "involuntary urination",
    "vomiting blood",
    "foot or toe swelling",
    "joint pain",
    "seizures",
    "mouth ulcer",
    "pain during pregnancy",
    "double vision",
    "regurgitation.1",
    "difficulty in swallowing",
    "heavy menstrual flow",
    "warts",
    "knee swelling",
    "restlessness",
    "smoking problems",
    "bones are painful",
    "redness in ear",
    "ringing in ear",
    "weight gain",
    "constipation",
    "painful sinuses",
    "coughing up sputum",
    "eye burns or stings",
    "neck swelling",
    "increased heart rate",
    "vaginal itching",
    "wrist swelling",
    "hurts to breath",
    "abnormal breathing sounds",
    "toothache",
    "leg weakness",
    "hoarse voice",
    "jaw swelling",
    "low self-esteem",
    "irregular appearing nails",
    "gum pain",
    "blood clots during menstrual periods",
    "symptoms of the face",
    "itchy scalp",
    "sinus congestion",
    "eyelid swelling",
    "pain of the anus",
    "lymphedema",
    "rib pain",
    "changes in stool appearance",
    "arm stiffness or tightness",
    "slurring words",
    "spotting or bleeding during pregnancy",
    "antisocial behavior",
    "mouth pain",
    "groin pain",
    "pain in gums",
    "feeling ill",
    "decreased heart rate",
    "lack of growth",
    "vaginal pain",
    "throat feels tight",
    "sleepiness",
    "pain in testicles",
    "melena",
    "muscle pain",
    "elbow swelling",
    "excessive urination at night",
    "irritable infant",
    "congestion in chest",
    "too little hair",
    "obsessions and compulsions",
    "impotence",
    "painful menstruation",
    "mass on eyelid",
    "neck mass",
    "vaginal redness",
    "blindness",
    "hemoptysis",
    "unpredictable menstruation",
    "abnormal movement of eyelid",
    "long menstrual periods",
    "swelling of scrotum",
    "regurgitation",
    "frontal headache",
    "symptoms of prostate",
    "arm weakness",
    "back mass or lump",
    "knee lump or mass",
    "leg stiffness or tightness",
    "ankle swelling",
    "hysterical behavior",
    "symptoms of bladder",
    "mass in scrotum",
    "symptoms of the scrotum and testes",
    "stiffness all over",
    "leg cramps or spasms",
    "itchy ear(s)",
    "muscle cramps, contractures, or spasms",
    "knee weakness",
    "shoulder stiffness or tightness",
    "mouth dryness",
    "throat swelling",
    "back cramps or spasms",
    "pain during intercourse",
    "hand or finger lump or mass",
    "bleeding gums",
    "sneezing",
    "flu-like syndrome",
    "skin on leg or foot looks infected",
    "hand or finger weakness",
    "uterine contractions",
    "nightmares",
    "frequent menstruation",
    "tongue lesions",
    "arm swelling",
    "nosebleed",
    "arm lump or mass",
    "unusual color or odor to urine",
    "apnea",
    "stomach bloating",
    "itching of the anus",
    "symptoms of the kidneys",
    "infertility",
    "swollen lymph nodes",
    "excessive appetite",
    "hot flashes",
    "pus draining from ear",
    "groin mass",
    "flatulence",
    "joint swelling",
    "dry or flaky scalp",
    "pain or soreness of breast",
    "swollen or red tonsils",
    "jaundice",
    "eyelid lesion or rash",
    "lump or mass of breast",
    "back stiffness or tightness",
    "wrist lump or mass",
    "burning chest pain",
    "hand or finger stiffness or tightness",
    "bleeding or discharge from nipple",
    "low urine output",
    "bleeding from eye",
    "infant feeding problem",
    "loss of sex drive",
    "cloudy eye",
    "kidney mass",
    "diaper rash",
    "breathing fast",
    "vulvar irritation",
    "knee stiffness or tightness",
    "recent pregnancy",
    "hip stiffness or tightness",
    "shoulder lump or mass",
    "sore in nose",
    "skin on arm or hand looks infected",
    "mass or swelling around the anus",
    "postpartum problems of the breast",
    "hesitancy",
    "bleeding from ear",
]

# Descargar modelos desde Google Cloud Storage
def download_model(bucket_name, folder_name, model_name):
    # Ruta local del modelo
    local_path = f"./{model_name}"
    
    # Verificar si el modelo ya está descargado
    if os.path.exists(local_path):
        print(f"Modelo {model_name} ya descargado localmente.")
        return local_path
    
    # Si no está, descargar desde Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"{folder_name}/{model_name}")
    blob.download_to_filename(local_path)
    print(f"Modelo {model_name} descargado desde {folder_name}.")
    return local_path

def download_csv(bucket_name, folder_name, csv_name):
    # Ruta local del CSV
    local_csv_path = f"./{csv_name}"
    
    # Verificar si ya está descargado
    if os.path.exists(local_csv_path):
        print(f"Archivo CSV {csv_name} ya descargado localmente.")
        return local_csv_path

    # Descargar desde el bucket
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"{folder_name}/{csv_name}")
    blob.download_to_filename(local_csv_path)
    print(f"Archivo CSV {csv_name} descargado desde {folder_name}.")
    return local_csv_path

# Descargar y cargar los modelos al inicio del servidor
print("Descargando Modelos...")
svd_path = download_model(BUCKET_NAME, MODELS_FOLDER, "svd_model.pkl")
logreg_path = download_model(BUCKET_NAME, MODELS_FOLDER, "logreg_model.pkl")
rf_path = download_model(BUCKET_NAME, MODELS_FOLDER, "rf_model.pkl")
xgb_path = download_model(BUCKET_NAME, MODELS_FOLDER, "xgb_model.pkl")
label_encoder_path = download_model(BUCKET_NAME, MODELS_FOLDER, "label_encoder.pkl")

print("Cargando modelos...")
svd = joblib.load(svd_path)
print("SVD Cargado")
logreg_model = joblib.load(logreg_path)
print("Regresión Logistica Cargado")
rf_model = joblib.load(rf_path)
print("Random Forest Cargado")
xgb_model = joblib.load(xgb_path)
print("XGboost Cargado")
label_encoder = joblib.load(label_encoder_path)
print("Label Encoder Cargado")

# Nombre del archivo CSV
CSV_NAME = "diseases_description_specialist.csv"

print("Descargando archivo CSV...")
csv_path = download_csv(BUCKET_NAME, MODELS_FOLDER, CSV_NAME)

print("Cargando datos del CSV...")
disease_data = pd.read_csv(csv_path)
print("Datos del CSV cargados.")

# Función para generar el vector de entrada
def generate_symptom_vector(symptoms):
    symptom_vector = np.zeros((1, len(symptom_names)))  # Vector de todos los síntomas
    for symptom in symptoms:
        if symptom in symptom_names:
            symptom_vector[0, symptom_names.index(symptom)] = 1
    return symptom_vector

# Función para obtener información desde la base de datos
def get_disease_info(disease_name):
    row = disease_data[disease_data["diseases"] == disease_name]
    if not row.empty:
        return {
            "description": row["description"].values[0],
            "specialist": row["specialist"].values[0],
        }
    return None

# Endpoint para Logreg
@app.route('/predict/logreg', methods=['POST'])
def predict_logreg():
    try:
        # Obtener la lista de síntomas desde el JSON
        data = request.json
        symptoms = data.get('symptoms', [])
        
        # Validar entrada
        if not symptoms or not isinstance(symptoms, list):
            return jsonify({"error": "Lista de síntomas inválida"}), 400
        
        # Generar vector de síntomas y reducir dimensionalidad
        symptom_vector = generate_symptom_vector(symptoms)
        reduced_vector = svd.transform(symptom_vector)
        
        # Predicción
        prediction = logreg_model.predict(reduced_vector)[0]
        print("Predicción realizada: " + prediction)
        disease_name = prediction
        disease_info = get_disease_info(disease_name)

        if not disease_info:
            return jsonify({"error": f"No se encontró información para la enfermedad '{disease_name}'"}), 404
        
        response = {
            "model": "Logistic Regression",
            "prediction": disease_name,
            "description": disease_info["description"],
            "specialist": disease_info["specialist"]
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para Random Forest
@app.route('/predict/rf', methods=['POST'])
def predict_rf():
    try:
        # Obtener la lista de síntomas desde el JSON
        data = request.json
        symptoms = data.get('symptoms', [])
        
        # Validar entrada
        if not symptoms or not isinstance(symptoms, list):
            return jsonify({"error": "Lista de síntomas inválida"}), 400
        
        # Generar vector de síntomas y reducir dimensionalidad
        symptom_vector = generate_symptom_vector(symptoms)
        reduced_vector = svd.transform(symptom_vector)
        
        # Predicción
        prediction = rf_model.predict(reduced_vector)[0]
        print("Predicción realizada: " + prediction)

        disease_name = prediction
        disease_info = get_disease_info(disease_name)

        if not disease_info:
            return jsonify({"error": f"No se encontró información para la enfermedad '{disease_name}'"}), 404
        
        response = {
            "model": "Random Forest",
            "prediction": disease_name,
            "description": disease_info["description"],
            "specialist": disease_info["specialist"]
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para XGBoost con LabelEncoder
@app.route('/predict/xgb', methods=['POST'])
def predict_xgb():
    try:
        # Obtener la lista de síntomas desde el JSON
        data = request.json
        symptoms = data.get('symptoms', [])
        
        # Validar entrada
        if not symptoms or not isinstance(symptoms, list):
            return jsonify({"error": "Lista de síntomas inválida"}), 400
        
        # Generar vector de síntomas y reducir dimensionalidad
        symptom_vector = generate_symptom_vector(symptoms)
        reduced_vector = svd.transform(symptom_vector)
        
        # Predicción
        prediction_index = int(xgb_model.predict(reduced_vector)[0])  # Convertir a int
        
        # Mapear el índice al nombre de la enfermedad usando LabelEncoder
        prediction_label = label_encoder.inverse_transform([prediction_index])[0]
        print("Predicción realizada: ", prediction_label)

        disease_name = prediction_label
        disease_info = get_disease_info(disease_name)

        if not disease_info:
            return jsonify({"error": f"No se encontró información para la enfermedad '{disease_name}'"}), 404
        
        response = {
            "model": "XGBoost",
            "prediction": disease_name,
            "description": disease_info["description"],
            "specialist": disease_info["specialist"]
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Prueba de conexión
@app.route('/')
def health_check():
    return jsonify({"status": "API running"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Toma el puerto de la variable de entorno o usa 8080 como predeterminado
    app.run(host='0.0.0.0', port=port)
