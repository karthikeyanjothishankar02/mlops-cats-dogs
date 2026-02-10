# Data Directory

This directory contains the datasets for the Cats vs Dogs classification project.

## Structure

```
data/
├── raw/              # Raw dataset (downloaded from Kaggle)
│   ├── cat.*.jpg
│   └── dog.*.jpg
├── processed/        # Preprocessed dataset
│   ├── train/
│   │   ├── cat/
│   │   └── dog/
│   ├── val/
│   │   ├── cat/
│   │   └── dog/
│   └── test/
│       ├── cat/
│       └── dog/
└── README.md         # This file
```

## Getting the Data

### Option 1: Automated Download (Recommended)
```bash
python scripts/download_data.py
```

### Option 2: Manual Download
1. Visit: https://www.kaggle.com/c/dogs-vs-cats/data
2. Download `train.zip`
3. Extract to `data/raw/`

### Alternative Dataset
For a smaller dataset, use:
https://www.kaggle.com/datasets/tongpython/cat-and-dog

## Data Preprocessing

After downloading the raw data, preprocess it:
```bash
python src/data/preprocess.py
```

This will:
- Resize all images to 224x224
- Normalize pixel values
- Split into train/val/test (80/10/10)
- Save to `data/processed/`

## Dataset Information

- **Total Images**: ~25,000 (typical)
- **Classes**: 2 (cat, dog)
- **Train Set**: ~20,000 images
- **Validation Set**: ~2,500 images
- **Test Set**: ~2,500 images
- **Image Format**: JPEG
- **Image Size**: 224x224x3 (after preprocessing)

## DVC Tracking

This directory is tracked with DVC for version control:
```bash
# Add data to DVC
dvc add data/raw
dvc add data/processed

# Push to remote storage
dvc push

# Pull from remote storage
dvc pull
```

## Notes

- Raw data is gitignored (tracked by DVC)
- Processed data is also gitignored
- Keep this directory structure intact
- Don't commit large files to git

## Troubleshooting

### Data not found
```bash
# Check if raw data exists
ls data/raw/

# If empty, download data
python scripts/download_data.py
```

### Preprocessing fails
```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Check raw data format
ls data/raw/ | head
```

## License

The Cats and Dogs dataset is provided by Kaggle and Microsoft. Please refer to the original dataset license for usage terms.
