FROM apache/airflow:2.7.1-python3.9

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH=/opt/airflow/projects/Olist_ETL_Project

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy project files
COPY --chown=airflow:root . /opt/airflow/projects/Olist_ETL_Project/

# Install Python dependencies
RUN pip install --no-cache-dir -r /opt/airflow/projects/Olist_ETL_Project/requirements.txt

# Create necessary directories
RUN mkdir -p /opt/airflow/projects/Olist_ETL_Project/dbt_project/olist_dbt_project/logs
RUN mkdir -p /opt/airflow/projects/Olist_ETL_Project/power_bi

# Set working directory
WORKDIR /opt/airflow/projects/Olist_ETL_Project

# Create startup script
RUN echo '#!/bin/bash\n\
cd /opt/airflow/projects/Olist_ETL_Project\n\
# Initialize Airflow database\n\
airflow db init\n\
# Create admin user\n\
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com\n\
# Start Airflow webserver\n\
airflow webserver --port 8080 --host 0.0.0.0 &\n\
# Start Airflow scheduler\n\
airflow scheduler &\n\
# Wait for both processes\n\
wait' > /opt/airflow/start.sh

RUN chmod +x /opt/airflow/start.sh

# Expose port
EXPOSE 8080

# Start services
CMD ["/opt/airflow/start.sh"]