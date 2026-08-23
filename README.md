# Urban-Street-Tree-Recognition

This repository contains the code and resources for our paper "Individual Urban Street Tree Recognition and Mapping based on Street-View Images and GIS data". We provide pre-trained models and data processing scripts to facilitate the replication of our street tree mapping framework.

## 📖 Overview

Accurate and fine-scale mapping of urban street trees is crucial for urban planning, environmental monitoring, and ecosystem service assessment. This project leverages the power of **Street View imagery** and **GIS data** to create a high-precision map of individual trees. Our method addresses challenges such as complex urban backgrounds and varying tree appearances.

---

## 🗂️ Dataset

The data used in this study is multi-sourced and stored under the `Datasets/` directory, structured as follows:

### 1. Street View Images
- **Source**: Google Street View Static API & Baidu Maps API.
- **Coverage**: Three cities with diverse urban structures and tree species:
  - **Brooklyn, New York, USA**: Dense, grid-patterned urban area.
  - **Xiangzhou, Zhuhai, China**: Subtropical coastal city with rich vegetation.
  - **Seongdong-gu, Seoul, South Korea**: High-density East Asian urban environment.
- **Location**: `Datasets/images/`
- **Purpose**: The primary data source for visual tree detection.

### 2. Annotations
- **Location**: `Datasets/annotations/`
- **Format**: YOLOv11-compatible annotation files (`*.txt`) with bounding box labels for trees in normalized coordinates format.

---

## 🔬 Pipeline

### 3. Detection
The `Detection/` directory contains pre-trained models, configuration files, and scripts for training and inference.

- **Pre-trained / Per-City Models**:
  - `NewYork-yolov11/`
  - `Seoul-yolov11/`
  - `Zhuhai-yolov11/`
- **Base Weights**: Foundational YOLO weights such as `yolov8n.pt`, `yolo11n.pt`.
- **Configuration**: `tree-category.yaml`
- **Training / Inference Scripts**:
  - `train-tree.py`: Script for initiating model training.
  - `train-tree-category.py`: Script for category-related training.
  - `test-tree-crop.py`: Script for performing inference and cropping detected tree instances from images.
- **Additional**:
  - `datasets-NewYork/tree/allimages/`
  - `README.zh-CN.md`

### 4. 🌳 Classification
- **Purpose**: Assign a **species-level or functional-group label** to each individually detected tree instance, enabling ecological analysis beyond mere presence/absence.
- **Input**: Cropped tree images produced by `Detection/test-tree-crop.py`.
- **Tool**: `Classification/` directory:
  - `tool/train.py`: Training script for the classification model.
  - `tool/batch_test.py`: Inference script for species/functional-group prediction.
- **Workflow**:
  1. Run `Detection/test-tree-crop.py` to extract individual tree patches.
  2. Feed cropped images into the classification model.
  3. Output a structured prediction file linking each tree to its predicted class.
- **Output**: `Classification/results/classification_results.csv`
- **Notes**: Supports per-city and cross-city classification via transfer learning.

### 5. 🗺️ Mapping
- **Purpose**: Georeference detected and classified trees to produce a **city-scale individual street tree map**.
- **Input**: Detection results, classification results, street-view metadata, GIS datasets (road centerlines, municipal inventories).
- **Tool**: `Mapping/` directory.
- **Workflow**:
  1. Associate each detection with its panorama and camera parameters.
  2. Project into world coordinates using GIS road network constraints.
  3. Merge duplicates and attach classification labels.
- **Output**: *(to be specified)*
- **Notes**: Handles occlusion, viewing-angle bias, and multi-view redundancy.
