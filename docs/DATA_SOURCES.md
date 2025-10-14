# Data Sources - Olist ETL Project

## Overview
This document explains how to obtain and set up the data required for the Olist ETL pipeline.

## Required Datasets

The following CSV files are needed for the complete ETL pipeline:

### Core E-commerce Data (9 files)
1. **olist_customers_dataset.csv** - Customer information
2. **olist_orders_dataset.csv** - Order details and status
3. **olist_order_items_dataset.csv** - Individual items within orders
4. **olist_order_payments_dataset.csv** - Payment information
5. **olist_order_reviews_dataset.csv** - Customer reviews
6. **olist_products_dataset.csv** - Product catalog
7. **olist_sellers_dataset.csv** - Seller information
8. **olist_geolocation_dataset.csv** - Geographic data
9. **product_category_name_translation.csv** - Category translations

## How to Obtain the Data

### Option 1: Kaggle (Recommended)
1. Go to: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Click "Download" to get the complete dataset
3. Extract the ZIP file to get all 9 CSV files

### Option 2: Manual Download
Each file can be downloaded individually from the Kaggle page above.

## Data Setup Instructions

### Step 1: Place Data Files
```bash
# Create the data directory structure
mkdir -p data/raw_data

# Copy all CSV files to this directory
cp olist_*.csv data/raw_data/
```

### Step 2: Verify File Sizes
The files should have approximately these sizes:
- olist_customers_dataset.csv: ~3MB
- olist_orders_dataset.csv: ~17MB
- olist_order_items_dataset.csv: ~15MB
- olist_order_payments_dataset.csv: ~1MB
- olist_order_reviews_dataset.csv: ~14MB
- olist_products_dataset.csv: ~2MB
- olist_sellers_dataset.csv: ~100KB
- olist_geolocation_dataset.csv: ~59MB
- product_category_name_translation.csv: ~10KB

### Step 3: PostgreSQL Setup (Optional)
If you want to use PostgreSQL as a source:
```bash
# Create database and tables
createdb olist_source_db

# Import CSV files to PostgreSQL tables
# (Scripts for this are in the scripts/ directory)
```

## Important Notes

### ⚠️ Repository Exclusions
- **Data files are NOT included** in this GitHub repository
- They are excluded via `.gitignore` for performance reasons
- The repository contains only code, configuration, and documentation
- Data files must be downloaded separately

### 🔒 Data Privacy
- The Olist dataset is publicly available for research purposes
- No sensitive personal information is included
- All customer data is anonymized

### 📊 Data Quality
- Dataset contains ~100K orders from 2016-2018
- Some missing values exist (handled by the ETL pipeline)
- Data cleaning is performed in the Bronze → Silver transformation

## Troubleshooting

### Common Issues
1. **File not found errors**: Ensure all 9 CSV files are present
2. **Encoding issues**: Files should be UTF-8 encoded
3. **Memory errors**: Large files (59MB geolocation) may need special handling

### Getting Help
- Check the main [README.md](../README.md) for setup instructions
- Review the ETL pipeline logs for specific error messages
- Ensure your system meets the [requirements](../README.md#prerequisites)

## Data Dictionary

For detailed information about each column in the datasets, refer to:
- Kaggle dataset page
- Olist documentation
- Comments in the dbt staging models