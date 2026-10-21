import pandas as pd
from sklearn.pipeline import Pipeline
import requests
from tqdm.auto import tqdm  # tqdm.auto choisit la bonne barre (notebook ou terminal)
import io
import pickle
from sklearn.preprocessing import LabelEncoder
from pydantic import BaseModel
from src.types.types import Claims, Success, Error
import logging
from datetime import datetime
import json

#Message reçu
class Claims(BaseModel):
    claims: dict[int, str]


PATH_PIPELINE = "src/model/model.pkl"
PATH_LAB_ENC = "src/model/lab_enc.pkl"

#Récupérer le model de la release, avec bar de chargement car des fois ça peut être long
def import_data(url: str, chunk_size: int = 1024 * 1024) -> pd.DataFrame:
   
    with requests.get(url, stream=True, timeout=30) as response:
        response.raise_for_status()  

        total_size = int(response.headers.get("content-length", 0)) or None

        buffer = io.BytesIO()
        with tqdm(total=total_size, unit="B", unit_scale=True, desc="Téléchargement") as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                buffer.write(chunk)
                progress_bar.update(len(chunk))

    buffer.seek(0) 
    print("buffer data ok")
    #Retourn le fichier .pkl
    return pickle.load(buffer)

#Sauvegarde le fichier .pkl dans le chemin
def save_data(model, path):
    print("Sauvegarder du fichier dans : ", path)
    with open(path, "wb") as f:
        pickle.dump(model, f)
    print(f"Modèle exporté vers {path}")

#retourne les prédictions
def call_ML(claims:Claims)->Success:

    pipeline: Pipeline = pd.read_pickle(PATH_PIPELINE)
    label_enc:LabelEncoder = pd.read_pickle(PATH_LAB_ENC)

    claim_list = claims.claims.values()
    pred = pipeline.predict(claim_list)
    pred_decod = label_enc.inverse_transform(pred)

    pred_claims = {idx: p for idx, p in enumerate(pred_decod)}

    print("pred : ", pred_decod)
 
    return {
            "id": "",
            "object": "",
            "created": datetime.now(),
            "model": "",
            "choices": [
                    {
                    "index": 0,
                    "message": {
                        "role": "",
                        "content": json.dumps({"response": pred_claims}),
                        },
                    "finish_reason": ""
                    }
                    ],
            "usage": {},
    }


if __name__ == "__main__":
    X_test = pd.read_csv("D:/Documents/CENTRE DE FORMATON/FORMATION IA/Projet 12/Mission_ZenAssist/Mission_1/src/data_set/dataSet_test.csv.gz", sep=";")
    claim = X_test.loc[4:14, "feature"]
   
    call_ML(claim)