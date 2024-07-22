import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carga y preparación de datos
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name='target')

# Dividimos los datos en conjuntos de entrenamiento, validación y prueba
X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=42)

# 2. Creación del pipeline con preprocesamiento y modelo
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel='rbf', C=1.0, probability=True, random_state=42))
])

# 3. Entrenamiento y validación cruzada
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5)
print(f"Puntuaciones de validación cruzada: {cv_scores}")
print(f"Precisión media de validación cruzada: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# 4. Entrenamiento final del modelo
pipeline.fit(X_train, y_train)

# 5. Evaluación en el conjunto de validación
val_score = pipeline.score(X_val, y_val)
print(f"Precisión en el conjunto de validación: {val_score:.3f}")

# 6. Guardado del pipeline completo
joblib.dump(pipeline, 'breast_cancer_model.joblib')
print("Modelo y preprocesador guardados como 'breast_cancer_model.joblib'")

# Simulamos el cierre y reapertura del programa
del pipeline

# 7. Carga y reutilización del modelo
loaded_pipeline = joblib.load('breast_cancer_model.joblib')

# 8. Evaluación final en el conjunto de prueba
y_pred = loaded_pipeline.predict(X_test)
print("\nInforme de clasificación:")
print(classification_report(y_test, y_pred))

print("\nMatriz de confusión:")
conf_matrix = confusion_matrix(y_test, y_pred)
print(conf_matrix)

# Graficación de la matriz de confusión
plt.figure(figsize=(10,7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Matriz de Confusión')
plt.ylabel('Etiqueta Verdadera')
plt.xlabel('Etiqueta Predicha')
plt.savefig('confusion_matrix.png')
plt.close()

# 9. Ejemplo de uso con nuevos datos
new_patients = X_test.sample(5, random_state=42)
predictions = loaded_pipeline.predict(new_patients)
probabilities = loaded_pipeline.predict_proba(new_patients)

print("\nPredicciones para nuevos pacientes:")
for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    print(f"Paciente {i+1}: Predicción: {'Maligno' if pred else 'Benigno'}, "
          f"Probabilidad de ser maligno: {prob[1]:.3f}")