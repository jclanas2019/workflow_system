# Importamos las bibliotecas necesarias
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# 1. Carga de datos y preparación
iris = datasets.load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 2. Entrenamiento del modelo
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# 3. Evaluación inicial del modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy:.2f}")

# 4. Guardado del modelo en formato .pkl
with open('iris_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Modelo guardado como 'iris_model.pkl'")

# Simulamos el cierre y reapertura del programa
del model

# 5. Carga y reutilización del modelo
with open('iris_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# 6. Uso del modelo cargado para hacer predicciones
new_predictions = loaded_model.predict(X_test)
new_accuracy = accuracy_score(y_test, new_predictions)
print(f"Precisión del modelo cargado: {new_accuracy:.2f}")