# Import necessary libraries
from flask import Flask, render_template, request
import numpy as np
import os
import tensorflow
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

# Load model
model = load_model("horse_or_human.h5")
print('@@ Model loaded')


def pred_human_horse(horse_or_human):
    test_image = load_img(horse_or_human, target_size=(150, 150))  # Load image
    print("@@ Got Image for prediction")

    test_image = img_to_array(test_image) / 255  # Convert image to np array and normalize
    test_image = np.expand_dims(test_image, axis=0)  # Change dimension 3D to 4D

    result = model.predict(test_image).round(3)  # Predict class horse or human
    print('@@ Raw result = ', result)

    pred = np.argmax(result)  # Get the index of max value

    if pred == 0:
        return "Horse"  # If index 0
    else:
        return "Human"  # If index 1


app = Flask(__name__)

# Render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']  # Get input
        filename = file.filename
        print("@@ Input posted =", filename)

        file_path = os.path.join('static/user uploads', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred = pred_human_horse(horse_or_human=file_path)

        return render_template('predict.html', pred_output=pred, user_image=file_path)


# For local system
if __name__ == "__main__":
    app.run(threaded=False)
