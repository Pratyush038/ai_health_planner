from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from config import MODEL_CONFIG


class HealthRiskModel:
    def __init__(self):
        self.model = RandomForestClassifier(**MODEL_CONFIG['random_forest'])
        self.scaler = StandardScaler()

    def train(self, X, y):
        """Train the health risk prediction model"""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, X):
        """Predict health risk score"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)


def get_risk_level(risk_score):
    """Determine risk level based on risk score"""
    if risk_score < 33:
        return "Low"
    elif risk_score < 66:
        return "Moderate"
    else:
        return "High"


def train_health_risk_model(data):
    """Helper function to train the model"""
    model = HealthRiskModel()
    X = data[['Age', 'BMI']]
    y = data['HealthRiskScore']
    model.train(X, y)
    return model