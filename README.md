# Urban-Street-Tree-Recognition
This repository contains the code and resources for our paper "Individual Urban Street Tree Recognition and Mapping based on Street-View Images and GIS data". We provide pre-trained models and data processing scripts to facilitate the replication of our street tree mapping framework.
## 📖 Overview
Accurate and fine-scale mapping of urban street trees is crucial for urban planning, environmental monitoring, and ecosystem service assessment. This project leverages the power of **Street View imagery** and **GIS data** to create a high-precision map of individual trees. Our method addresses challenges such as complex urban backgrounds and varying tree appearances.
## 🗂️ Dataset Description

The data used in this study is multi-sourced and structured as follows:

### 1. Street View Images
- **Source**: Google Street View Static API & Baidu Maps API.
- **Coverage**: Three cities with diverse urban structures and tree species:
  - **Brooklyn, New York, USA**: Dense, grid-patterned urban area.
  - **Xiangzhou, Zhuhai, China**: Subtropical coastal city with rich vegetation.
  - **Seongdong-gu, Seoul, South Korea**: High-density East Asian urban environment.
- **Purpose**: The primary data source for visual tree detection.
### 2. Annotations
- **Annotation Files**: The annotations/ directory contains YOLOv11-compatible annotation files (*.txt) with bounding box labels for trees in normalized coordinates format.
### 3. Pre-trained Models
- **Location**: `Detection` directory.
- **Contents**:
  ​​Per-City Models​​: Fine-tuned model weights for each target city, stored in their respective directories (e.g., NewYork-yolov11/, Seoul-yolov11/, Zhuhai-yolov11/).
​​  Base Models​​: Foundational pre-trained weights for YOLO architectures (yolov8n.pt, yolo11n.pt).
### 4. Sample Testing Scripts
- Purpose​​: Ready-to-use scripts for quick verification of the data processing pipeline and model inference.
- ​​Scripts​​:
  train-tree.py: Script for initiating model training.
  test-tree-crop.py: Script for performing inference and cropping detected tree instances from images.
### 5. 🌳 Classification
- **Purpose**: Assign a **species-level or functional-group label** to each individually detected tree instance, enabling ecological analysis beyond mere presence/absence.
- **Input**: Cropped tree images produced by `Detection/test-tree-crop.py`.
- **Tool**: `Classification/` directory :
  - `tool/train.py`: Training script for the classification model.
  - `tool/batch_test.py`: Inference script for species/functional-group prediction.
- **Workflow**:
  1. Run `Detection/test-tree-crop.py` to extract individual tree patches.
  2. Feed cropped images into the classification model.
  3. Output a structured prediction file linking each tree to its predicted class.
- **Output**: `Classification/results/classification_results.csv`
- **Notes**: Supports per-city and cross-city classification via transfer learning.
### 6. 🗺️ Mapping
- **Purpose**: Georeference detected and classified trees to produce a **city-scale individual street tree map**.
- **Input**: Detection results, classification results, street-view metadata, GIS datasets (road centerlines, municipal inventories).
- **Tool**: `Mapping/` directory:
- **Workflow**:
  1. Associate each detection with its panorama and camera parameters.
  2. Project into world coordinates using GIS road network constraints.
  3. Merge duplicates and attach classification labels.
- **Output**: ``
- **Notes**: Handles occlusion, viewing-angle bias, and multi-view redundancy.
