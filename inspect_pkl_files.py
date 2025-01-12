import pickle
import os

with open('data/random_forest_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('data/scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

output_filename = os.path.join('data', 'model_and_scaler_output.txt')

with open(output_filename, 'w') as output_file:
    output_file.write("Random Forest Model:\n")
    output_file.write(str(model))

    output_file.write("\n\nScaler:\n")
    output_file.write(str(scaler))

print(f"Model and scaler have been saved to {output_filename}")
