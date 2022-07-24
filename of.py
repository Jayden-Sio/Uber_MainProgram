### Load necessary libraries ###
import glob
import os
import librosa
import numpy as np
from sklearn.metrics import accuracy_score

import tensorflow as tf
from tensorflow import keras

from keras.models import load_model

from playsound import playsound


### Define helper functions ###
def extract_features(parent_dir, sub_dirs, file_ext="*",
                     bands=60, frames=41):
    features, labels = [], []
    # print(glob.glob(os.path.join(parent_dir, sub_dir, file_ext)))
    for fn in glob.glob(os.path.join(parent_dir, sub_dirs, file_ext)):
        segment_log_specgrams, segment_labels = [], []
        sound_clip, sr = librosa.load(fn)
        label = int(fn.split('/')[1].split('-')[1])
        audio, sample_rate = librosa.load(fn, res_type='kaiser_fast')
        mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
        features.append([mfccs_scaled_features])
        labels.append([label])
    return features, labels


def output():
    parent_dir = 'quake_sounds/'
    save_dir = "quake_sounds/processed/"
    sub_dir = 'test'

    features, labels = extract_features(parent_dir, sub_dir)

    np.savez("{0}{1}".format(save_dir, sub_dir),
             features=features,
             labels=labels)

    accuracies = []
    test_data = np.load("{0}/{1}.npz".format(save_dir,
                                             sub_dir), allow_pickle=True)

    x_test = test_data["features"]
    y_test = test_data["labels"]

    model = load_model("saved_models/audio_classification.hdf5")
    y1 = []
    for x, y in zip(x_test, y_test):
        avg_p = np.argmax(np.mean(model.predict(x), axis=0))
        y1.append(avg_p)
    return y1[0]
