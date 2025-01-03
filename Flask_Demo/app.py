
import os
from flask import Flask, request, jsonify,render_template
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from keras.utils import img_to_array 
import numpy as np
from keras.preprocessing import image
import tensorflow as tf  
from keras.utils import load_img, img_to_array 
from skimage import io
from werkzeug.utils import secure_filename
from keras.models import load_model

app = Flask(__name__)


# Loading model 
model = load_model('depression (1).h5') 

# Function to preprocess the uploaded image
def preprocess_image(img_path):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(64, 64))
    img_array =  tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array
    


def resize_images( X_in ):
    imgs=[]
    for path in X_in :
        img =io.imread(path)


# Function to make predictions using the loaded model
def predict_label(img_array):
    # Preprocess the image array
    img_array = preprocess_image(img_array)

    # Make predictions
    predictions = model.predict(img_array)
    label = np.argmax(predictions)

    return label

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def upload_predict():
    if request.method == 'POST':
        # Get the file from the request
        img = request.files['file']
        filename = secure_filename(img.filename)
        # Save the image to a temporary directory
        img_path = os.path.join(r"uploads", filename)
        img.save(img_path)

        # Predict the label for the image
        label = predict_label(img_path)

        # Define your own labels here based on your model's output
        labels = {
            0: ' you are Depressed     -Take a text test to check your mental health',#dep=sad
            1: 'you are Not Depressed         -You can also take a text test to check your mental health',#nondep=happy
            # Add more labels as needed
        }

        # Get the label name based on the predicted index
        predicted_label = labels.get(label, 'Unknown')

        # Remove the temporary image file
        os.remove(img_path)
        if predicted_label==0:
            return render_template('index.html',pred=predicted_label)
        else:
            return render_template('index.html',pred=predicted_label)



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=3000)