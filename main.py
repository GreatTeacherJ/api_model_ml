from fastapi import FastAPI

from src.api_model_ml.call_Ml import  import_data, save_data, PATH_PIPELINE, PATH_LAB_ENC, call_ML, Claims

#Url vers le model, à changer si la release change
model_url = "https://github.com/GreatTeacherJ/ZenAssist/releases/download/v1.2.1_ML/model.pkl"
label_enc_url = "https://github.com/GreatTeacherJ/ZenAssist/releases/download/v1.2.1_ML/lab_enc.pkl"
print("Url du modèle à télécharger : ", model_url)

#Sauvegarde du model au chargement de l'api
save_data((import_data(model_url)), PATH_PIPELINE)
save_data((import_data(label_enc_url)), PATH_LAB_ENC)


app = FastAPI()


@app.post("/completion_ml/", tags=["Completion"])
def read_prompt(claims:Claims):  
    print("prompt reçu : ", claims)  
    return call_ML(claims)