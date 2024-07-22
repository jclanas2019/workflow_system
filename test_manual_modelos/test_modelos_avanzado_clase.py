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

class BreastCancerModel:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.pipeline = None
        self.X_train = None
        self.X_val = None
        self.X_test = None
        self.y_train = None
        self.y_val = None
        self.y_test = None

    def load_data(self):
        data = load_breast_cancer()
        X = pd.DataFrame(data.data, columns=data.feature_names)
        y = pd.Series(data.target, name='target')
        return X, y

    def split_data(self, X, y):
        X_train_val, self.X_test, y_train_val, self.y_test = train_test_split(X, y, test_size=0.2, random_state=self.random_state)
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=self.random_state)

    def create_pipeline(self):
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('svm', SVC(kernel='rbf', C=1.0, probability=True, random_state=self.random_state))
        ])

    def train_and_evaluate(self):
        cv_scores = cross_val_score(self.pipeline, self.X_train, self.y_train, cv=5)
        print(f"Puntuaciones de validación cruzada: {cv_scores}")
        print(f"Precisión media de validación cruzada: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

        self.pipeline.fit(self.X_train, self.y_train)

        val_score = self.pipeline.score(self.X_val, self.y_val)
        print(f"Precisión en el conjunto de validación: {val_score:.3f}")

    def save_model(self, filename='breast_cancer_model.joblib'):
        joblib.dump(self.pipeline, filename)
        print(f"Modelo y preprocesador guardados como '{filename}'")

    def load_model(self, filename='breast_cancer_model.joblib'):
        self.pipeline = joblib.load(filename)

    def evaluate_model(self):
        y_pred = self.pipeline.predict(self.X_test)
        print("\nInforme de clasificación:")
        print(classification_report(self.y_test, y_pred))

        print("\nMatriz de confusión:")
        conf_matrix = confusion_matrix(self.y_test, y_pred)
        print(conf_matrix)

        self.plot_confusion_matrix(conf_matrix)

    def plot_confusion_matrix(self, conf_matrix):
        plt.figure(figsize=(10,7))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
        plt.title('Matriz de Confusión')
        plt.ylabel('Etiqueta Verdadera')
        plt.xlabel('Etiqueta Predicha')
        plt.savefig('confusion_matrix.png')
        plt.close()

    def predict(self, X):
        return self.pipeline.predict(X)

    def predict_proba(self, X):
        return self.pipeline.predict_proba(X)

    def get_test_data(self):
        return self.X_test, self.y_test

def main():
    # Inicializar y entrenar el modelo
    model = BreastCancerModel()
    X, y = model.load_data()
    model.split_data(X, y)
    model.create_pipeline()
    model.train_and_evaluate()
    model.save_model()

    # Obtener los datos de prueba antes de eliminar el modelo
    X_test, y_test = model.get_test_data()

    # Simular cierre y reapertura del programa
    del model

    # Cargar y evaluar el modelo
    loaded_model = BreastCancerModel()
    loaded_model.load_model()
    loaded_model.X_test = X_test
    loaded_model.y_test = y_test
    loaded_model.evaluate_model()

    # Ejemplo de uso con nuevos datos
    new_patients = X_test.sample(5, random_state=42)
    predictions = loaded_model.predict(new_patients)
    probabilities = loaded_model.predict_proba(new_patients)

    print("\nPredicciones para nuevos pacientes:")
    for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
        print(f"Paciente {i+1}: Predicción: {'Maligno' if pred else 'Benigno'}, "
              f"Probabilidad de ser maligno: {prob[1]:.3f}")

if __name__ == "__main__":
    main()