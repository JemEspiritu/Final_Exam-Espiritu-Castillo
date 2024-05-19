# -*- coding: utf-8 -*-
"""streamlit_app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pi0MJbXTEnxGi5mh5YLslt706KOb7RB5

Technological Institute of the Philippines | Quezon City - Computer Engineering
--- | ---
Course Code: | CPE 019
Code Title: | Emerging Technologies in CpE 2
2nd Semester | AY 2024-2025
<hr> | <hr>
<u>**ACTIVITY NO.** | **Final Examination**
**Name** | John Edward Miles D. Espiritu / Mark Laurence Castillo
**Section** | CPE32S1
**Date Performed**: |05/17/2024
**Date Submitted**: |05/19/2024
**Instructor**: | Engr. Ryan Francisco

<hr>
"""

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
from tensorflow.keras.preprocessing.image import img_to_array
from keras.models import load_model
import os

# Page configuration must be set before any Streamlit commands
st.set_page_config(
    page_title="Fashion Classifier",
    page_icon="👗",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Function to load the model
@st.cache_resource
def load_fashion_model():
    model_path = 'saved_fashion.h5'
    if not os.path.exists(model_path):
        st.error(f"Model file not found: {model_path}")
        return None
    model = tf.keras.models.load_model(model_path)
    return model

# Function to preprocess the image and make predictions
def import_and_predict(image_data, model):
    size = (28, 28)
    # Convert image to grayscale and resize
    image = ImageOps.grayscale(ImageOps.fit(image_data, size, Image.Resampling.LANCZOS))
    img = np.asarray(image)
    img = img / 255.0  # Normalize
    img_reshape = img[np.newaxis, ..., np.newaxis]  # Add batch and channel dimensions
    prediction = model.predict(img_reshape)
    return prediction

# Load the model once
model = load_fashion_model()
if model is None:
    st.stop()

# Streamlit UI Design
st.title("🧥 Fashion Dataset by Espiritu_Castillo")
st.write(
    """
    Welcome to the Fashion Item Classifier! 
    Upload an image of a fashion item, and the model will predict what type of item it is.
    """
)

st.sidebar.write("## Instructions")
st.sidebar.write(
    """
    1. Upload a photo of a fashion item (jpg or png).
    2. Wait for the model to process and predict.
    3. See the prediction result below the uploaded image.
    """
)

file = st.file_uploader("Choose a photo from your computer", type=["jpg", "png"])

if file is None:
    st.text("Please upload an image file to get started.")
else:
    image = Image.open(file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Perform prediction
    prediction = import_and_predict(image, model)

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']
    result_class = np.argmax(prediction)
    result_label = class_names[result_class]
    confidence = prediction[0][result_class]

    st.write("## Prediction Result")
    st.write(f"**Item:** {result_label}")
    st.write(f"**Confidence:** {confidence:.2%}")

    st.balloons()  # Add some celebratory balloons when a prediction is made

