import React, { useState } from "react";
import "./App.css";

const symptomNames = [
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
];

const App = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [predictionResult, setPredictionResult] = useState(null);

  const toggleSymptom = (symptom) => {
    if (selectedSymptoms.includes(symptom)) {
      setSelectedSymptoms(selectedSymptoms.filter((s) => s !== symptom));
    } else {
      setSelectedSymptoms([...selectedSymptoms, symptom]);
    }
  };

  const handlePrediction = async (model) => {
    const endpoint = `https://flask-api-713183927669.us-central1.run.app/predict/${model}`;
    const payload = { symptoms: selectedSymptoms };

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch prediction");
      }

      const data = await response.json();
      setPredictionResult(data);
    } catch (error) {
      console.error("Error while fetching prediction:", error);
      setPredictionResult({
        error: "Failed to get prediction. Please try again.",
      });
    }
  };

  return (
    <div className="App">
      <div className="header1">
        <h1>Medical AI</h1>
      </div>

      <div className="corporate_border"></div>

      <header>
        <h1>Symptom Checker</h1>
      </header>

      <main>
        {/* Botones de síntomas */}
        <div className="symptom-buttons">
          {symptomNames.map((symptom) => (
            <button
              key={symptom}
              className={`symptom-button ${
                selectedSymptoms.includes(symptom) ? "selected" : ""
              }`}
              onClick={() => toggleSymptom(symptom)}
            >
              {symptom}
            </button>
          ))}
        </div>

        {/* Lista visible de síntomas seleccionados */}
        <div className="selected-symptoms">
          <h3>Selected Symptoms:</h3>
          {selectedSymptoms.length > 0 ? (
            <ul>
              {selectedSymptoms.map((symptom) => (
                <li key={symptom}>{symptom}</li>
              ))}
            </ul>
          ) : (
            <p>No symptoms selected.</p>
          )}
        </div>

        {/* Botones de modelos */}
        <div className="model-buttons">
          <button onClick={() => handlePrediction("logreg")}>
            Regresión Logística
          </button>
          <button onClick={() => handlePrediction("rf")}>Random Forest</button>
          <button onClick={() => handlePrediction("xgb")}>XGBoost</button>
        </div>

        {/* Resultados de la predicción */}
        {predictionResult && (
          <div className="prediction-result">
            {predictionResult.error ? (
              <p className="error">{predictionResult.error}</p>
            ) : (
              <div>
                <h3>Prediction Result:</h3>
                <p>
                  <strong>Disease:</strong> {predictionResult.prediction}
                </p>
                <p>
                  <strong>Model Used:</strong> {predictionResult.model}
                </p>
                <p>
                  <strong>Description:</strong> {predictionResult.description}
                </p>
                <p>
                  <strong>Specialist:</strong> {predictionResult.specialist}
                </p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
