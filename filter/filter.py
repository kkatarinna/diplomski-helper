import os
import cv2
from tqdm import tqdm
import numpy as np
import pandas as pd
import csv


def load_images_from_folder(folder_path, extensions=(".jpg", ".png", ".jpeg")):
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(extensions)
    ]

def get_image_features_hsv(image_hsv):
    H_channel = image_hsv[:, :, 0]
    S_channel = image_hsv[:, :, 1]
    V_channel = image_hsv[:, :, 2]

    features = {
        'H_mean': np.mean(H_channel),
        'H_std': np.std(H_channel),
        'S_mean': np.mean(S_channel),
        'S_std': np.std(S_channel),
        'V_mean': np.mean(V_channel),
        'V_std': np.std(V_channel),
    }
    return features

if __name__ == "__main__":
    input_folder = "/Users/katarinakrstin/Downloads/ISIC_2020_Training_JPEG/train/"
    metadata = "/Users/katarinakrstin/Documents/GitHub/diplomski/data/Training_GroundTruth_balanced.csv"
    

    df = pd.read_csv(metadata)
    image_paths = load_images_from_folder(input_folder)
    
    with open('filtered_images.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['image name', 'target'])
    
    for img_path in tqdm(image_paths, desc=f"Processing images"):
        image_name = os.path.splitext(os.path.basename(img_path))[0]
        image_hsv =  cv2.cvtColor(cv2.resize( cv2.imread(img_path), (224, 224)), cv2.COLOR_BGR2HSV)
        if image_hsv is None:
            continue

        features = get_image_features_hsv(image_hsv)
        counter = 0
        malignant = 0
        if(features['H_mean'] < 12 and features['H_mean'] > 7 and features['H_std'] < 10 and features['S_std'] < 20 and features['V_std'] < 20):
            counter += 1
            if df[df['image_name'] == image_name]['target'].values[0] == 1:
                malignant += 1
            
            with open('filtered_images.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([image_name, df[df['image_name'] == image_name]['target'].values[0]])


    print("filtered images: ", counter)
    print("malignant images: ", malignant)