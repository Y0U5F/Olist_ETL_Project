# End-to-End Data Pipeline - Olist E-commerce

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/)
[![Airflow 2.7.1](https://img.shields.io/badge/airflow-2.7.1-brightgreen)](https://airflow.apache.org/)
[![dbt 1.7.4](https://img.shields.io/badge/dbt-1.7.4-orange)](https://www.getdbt.com/)
[![Snowflake](https://img.shields.io/badge/Snowflake-%230077ED.svg?style=for-the-badge&logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## Overview

This project implements an end-to-end data pipeline for Olist, a Brazilian e-commerce company. The pipeline follows an ELT (Extract, Load, Transform) architecture with a Medallion layer approach (Bronze, Silver, Gold) in Snowflake. It leverages Apache Airflow for orchestration, dbt for data transformation, and Python for custom tasks. The final output is visualized in Power BI.

## Tech Stack

*   **Programming Language:** Python
*   **Orchestration:** Apache Airflow
*   **Data Transformation:** dbt (data build tool)
*   **Data Warehouse:** Snowflake
*   **Containerization:** Docker
*   **Visualization:** Power BI

## Architecture

The pipeline adheres to the Medallion architecture:

*   **Bronze Layer:** Raw data ingested from source systems (PostgreSQL and CSV files) into Snowflake.
*   **Silver Layer:** Cleaned and conformed data, ready for business logic.
*   **Gold Layer:** Aggregated and business-ready data, optimized for reporting and analysis. A Star Schema is implemented in this layer.

## Features

*   **Automated dbt Tests:** 26+ automated dbt tests ensure data quality and integrity throughout the transformation process.
*   **Star Schema:** The Gold layer is structured as a Star Schema for efficient querying and reporting.
*   **Daily Orchestration:** Apache Airflow orchestrates the entire pipeline, ensuring daily data updates.
*   **Dockerized Environment:** The entire pipeline can be run within a Docker container for easy deployment and reproducibility.

## Key Insights

Analysis of the Olist dataset revealed the following key insights:

*   **Revenue Distribution:** 70% of revenue originates from Southeast Brazil.
*   **Delivery Time Impact:** Delivery time significantly impacts customer satisfaction.

## Project Structure

```
Olist_ETL_Project/
├── 📁 airflow/                          # Apache Airflow components
│   ├── dags/
│   │   └── olist_full_pipeline_dag.py   # Main ETL pipeline DAG
│   └── outputs/                         # Airflow execution screenshots
│
├── 📁 data/                             # Data files
│   └── raw_data/                        # Raw CSV datasets from Olist
│       ├── olist_customers_dataset.csv
│       ├── olist_orders_dataset.csv
│       ├── olist_order_items_dataset.csv
│       └── ... (8 more datasets)
│
├── 📁 dbt_project/                      # dbt (Data Build Tool) project
│   └── olist_dbt_project/
│       ├── models/
│       │   ├── staging/                 # Bronze → Silver transformations
│       │   │   ├── stg_customers.sql
│       │   │   ├── stg_orders.sql
│       │   │   ├── stg_order_items.sql
│       │   │   ├── stg_products.sql
│       │   │   ├── stg_sellers.sql
│       │   │   └── schema.yml          # Data quality tests
│       │   └── marts/                   # Silver → Gold transformations
│       │       ├── dim_customers.sql
│       │       ├── dim_products.sql
│       │       ├── dim_sellers.sql
│       │       ├── dim_date.sql
│       │       ├── dim_orders.sql
│       │       └── fct_order_items.sql # Fact table with measures
│       ├── macros/                      # Reusable SQL functions
│       ├── seeds/                       # Static data files
│       ├── analyses/                    # Ad-hoc analysis queries
│       └── tests/                       # Additional test cases
│
├── 📁 docs/                            # Documentation & presentations
│   ├── python and Pandas script outputs and graphs/
│   │   └── EDA output *.png            # Exploratory data analysis charts
│   ├── Star schema.pdf                 # Database schema design
│   └── End-to-End-Data-Pipeline presentation.pdf
│
├── 📁 logs/                           # Application logs
│   └── dbt.log                        # dbt execution logs
│
├── 📁 power_bi/                       # Power BI dashboard files
│   ├── Olist.pbit                      # Power BI template
│   └── Screenshots/                    # Dashboard preview images
│
├── 📁 scripts/                        # Python scripts (if any)
│
├── 📄 .env                            # Environment variables (create from .env.example)
├── 📄 .env.example                     # Environment variables template
├── 📄 .gitignore                       # Git ignore patterns
├── 📄 .dockerignore                    # Docker ignore patterns
├── 📄 config.py                        # Python configuration management
├── 📄 docker-compose.yml               # Multi-container setup
├── 📄 Dockerfile                       # Container definition
├── 📄 LICENSE                          # MIT License
├── 📄 requirements.txt                 # Python dependencies
├── 📄 CONTRIBUTING.md                  # Contribution guidelines
└── 📄 README.md                        # This file
```

## Getting Started

### Prerequisites

- **Python 3.9+**
- **Docker & Docker Compose**
- **Git**
- **Snowflake Account** (for data warehouse)
- **PostgreSQL** (for source data - optional, can use CSV files)

### Installation & Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Y0U5F/Olist_ETL_Project.git
    cd Olist_ETL_Project
    ```

2. **Set up environment variables:**

    ```bash
    cp .env.example .env
    # Edit .env file with your actual credentials
    nano .env
    ```

3. **Build and run with Docker:**

    ```bash
    docker-compose up --build -d
    ```

4. **Access Airflow UI:**

    * Open your browser and navigate to `http://localhost:8080`
    * Default credentials: `admin` / `admin`

5. **Trigger the ETL Pipeline:**

    * In the Airflow UI, locate the `olist_end_to_end_pipeline` DAG
    * Click "Play" button to trigger the pipeline
    * Monitor the progress in the "Browse" -> "Task Instances" section

### Alternative Setup (Without Docker)

If you prefer to run locally:

1. **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Set up PostgreSQL:**

    ```bash
    docker run -d --name olist_postgres \
      -e POSTGRES_USER=olist_user \
      -e POSTGRES_PASSWORD=olist_password \
      -e POSTGRES_DB=olist_source_db \
      -p 5432:5432 postgres:13
    ```

3. **Install and configure dbt:**

    ```bash
    cd dbt_project/olist_dbt_project
    dbt deps
    dbt debug
    ```

4. **Run the pipeline manually:**

    ```bash
    python scripts/ingest_to_bronze.py
    cd dbt_project/olist_dbt_project
    dbt run
    dbt test
    ```

## dbt Setup

1.  **Install dbt:**

    ```bash
    pip install dbt-snowflake
    ```

2.  **Configure dbt profiles:**

    *   Create a `profiles.yml` file in the `dbt_profiles` directory (specified in `.env`) with your Snowflake connection details.

## Useful Commands

### Development Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f airflow

# Stop all services
docker-compose down

# Rebuild containers
docker-compose up --build --force-recreate

# Clean up everything (including volumes)
docker-compose down -v --remove-orphans
```

### dbt Commands

```bash
cd dbt_project/olist_dbt_project

# Install dependencies
dbt deps

# Check configuration
dbt debug

# Run all models
dbt run

# Run specific model
dbt run --select dim_customers

# Run tests
dbt test

# Generate documentation
dbt docs generate

# Serve documentation locally
dbt docs serve
```

### Airflow Commands

```bash
# Access Airflow container
docker-compose exec airflow bash

# Check DAG status
airflow dags list

# Test DAG
airflow dags test olist_end_to_end_pipeline

# View task logs
airflow logs show olist_end_to_end_pipeline ingest_raw_data_to_bronze
```

### Data Validation Commands

```bash
# Run data quality checks
cd dbt_project/olist_dbt_project && dbt test

# Check row counts in each table
cd dbt_project/olist_dbt_project && dbt run-operation check_row_counts
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to:

- Set up a development environment
- Follow our coding standards
- Submit pull requests
- Report issues

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Yousef Soliman** - Data Engineer

- 📧 [yousef.soliman.de@gmail.com](mailto:yousef.soliman.de@gmail.com)
- </> [GitHub Profile](https://github.com/Y0U5F)
- 🇱 [LinkedIn Profile](https://www.linkedin.com/in/y0usefma7m0ud/)
- 💼 [My Portfolio](https://y0u5f.github.io/)

---

⭐ **If you found this project helpful, please give it a star!**
