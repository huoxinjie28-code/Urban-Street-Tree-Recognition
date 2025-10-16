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
### 2. GIS Data & Annotations
- **Tree Inventory**: Vector data (e.g., Shapefile `.shp`) containing the location and species information of individual trees (if available).
- **Road Network**: Vector data used to generate sampling points for Street View image acquisition.
- **Annotation Files**: The `annotations/` directory contains VOC-format or COCO-format files (`*.xml` or `*.json`) with bounding box labels for trees in the Street View images.

### 3. Pre-trained Models
- **Location**: `models/` directory.
- **Contents**:
  - `trees_faster_rcnn.pth` / `trees_yolov5.pt`: The final model weights for tree detection.
  - `training_logs/`: Logs and graphs from the model training process.

### 4. Processed Data (For Direct Inference)
- We provide a small set of example Street View images in the `samples/` directory for quick testing.
