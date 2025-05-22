FROM apache/airflow:2.6.0-python3.10

# Install the Microsoft ODBC driver 18 needed to use sqlalchemy in dags to connect to SQL db.
USER root
RUN \
    # Download the package to configure the Microsoft repo
    curl -sSL -O https://packages.microsoft.com/config/debian/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1)/packages-microsoft-prod.deb && \
    # Install the package
    dpkg -i packages-microsoft-prod.deb && \
    # Delete the file
    rm packages-microsoft-prod.deb && \

    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18

# install additional Python libraries required by Airflow dags
USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt