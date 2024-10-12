from sklearn.linear_model import LogisticRegression
import joblib

def train_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    # Save the model
    joblib.dump(model, 'models/model.pkl')

def load_model():
    return joblib.load('models/model.pkl')

def predict(model, X_test):
    return model.predict(X_test)