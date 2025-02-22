import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 1. Load dataset
df = pd.read_csv("cleaned_drying_time_dataset.csv")
X = df.drop(columns=["drying_time"], errors="ignore")
y = df["drying_time"]

# 2. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 3. Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Configure MLP Regressor (LBFGS solver)
#    - LBFGS is a quasi-Newton method that can yield good results on modest data sizes
#    - alpha=0.002 for moderate regularization
#    - hidden_layer_sizes=(300,200,100,50) for deeper capacity
model = MLPRegressor(
    hidden_layer_sizes=(300, 200, 100, 50),
    activation='relu',
    solver='lbfgs',      # LBFGS solver
    alpha=0.002,
    max_iter=2000,       # LBFGS can converge faster, but give it enough iterations
    random_state=42
)

# 5. Fit the model
model.fit(X_train_scaled, y_train)

# 6. Predictions
y_pred = model.predict(X_test_scaled)

# 7. Evaluate
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
accuracy = 100 - mape

# 8. Save Results
results = pd.DataFrame({
    "Version": ["MLP Regressor"],
    "MSE": [mse],
    "RMSE": [rmse],
    "MAE": [mae],
    "R2": [r2],
    "MAPE (%)": [mape],
    "Accuracy (%)": [accuracy]
})
results.to_csv("metrics.csv", mode="a", index=False, header=False)

print("Training completed.")
print(f"MSE: {mse:.5f}, RMSE: {rmse:.5f}, MAE: {mae:.5f}, R2: {r2:.5f}, MAPE: {mape:.5f}%, Accuracy: {accuracy:.5f}%")

import joblib

# Save the trained model and scaler
joblib.dump(model, 'models/drying_time_model/model.joblib')
joblib.dump(scaler, 'models/drying_time_model/scaler.joblib')