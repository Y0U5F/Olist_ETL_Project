# CHANGELOG

## [0.1.0] - 2024-07-01

### Added

- Initial commit of the Olist E-commerce data pipeline project.
- Implemented ELT architecture with Medallion layers (Bronze, Silver, Gold) in Snowflake.
- Integrated Apache Airflow for pipeline orchestration.
- Utilized dbt for data transformation and testing.
- Created a Star Schema in the Gold layer for efficient reporting.
- Included 26 automated dbt tests for data quality.
- Dockerized the entire environment for easy deployment.
- Created initial README.md and .gitignore files.