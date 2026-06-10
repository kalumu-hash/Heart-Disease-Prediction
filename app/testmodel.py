import joblib

model = joblib.load("../model/model.pkl")

print("Model loaded successfully!")
print(type(model))