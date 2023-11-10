# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# This will install libGL and any other packages that are necessary
ENV NLTK_DATA=/app/nltk_data
ENV AZURE_CONN_STR="DefaultEndpointsProtocol=https;AccountName=jpsdatalaketest;AccountKey=dpazhoiFa7Fp7lDGcnsvWCBwx8mReFnqT8jXjA5VlzR+GAbSzcLdEqC2UqApXonXwBEI7wV4Js8U+AStqY/P8g==;EndpointSuffix=core.windows.net"
ENV AZURE_CONTAINER_NAME="aifiles"
ENV AZURE_BLOB_URL="https://jpsdatalaketest.blob.core.windows.net/aifiles?sp=racwdlmeop&st=2023-11-05T19:56:10Z&se=2023-11-29T03:56:10Z&sv=2022-11-02&sr=c&sig=bjgWqebW7aI1N%2Fz1CJNIZ%2FHFcHIm2IDtukiKWNuwI30%3D"
ENV FROM_EMAIL="info@jalapenosolutions.nl"
ENV SECOND_RECIPIENT="sales@jalapenosolutions.nl"
ENV THIRD_RECIPIENT="iepe@jalapenomarketing.nl" 
ENV DATABASE_URL="postgresql://jalapenopostgres:99fEQ8HDNtzhrAu@webapppostgres.postgres.database.azure.com/jpswebshop"
ENV VECTORDB_URL = "postgresql://jalapenopostgres:99fEQ8HDNtzhrAu@webapppostgres.postgres.database.azure.com/jpswebshop"
ENV SENDGRIP_API_KEY="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"
ENV ZOHO_CLIENT_ID="1000.CBIUBMS22MX0WXYW8CZ57F5Z86I0YI"
ENV ZOHO_CLIENT_SECRET="68d404fbea8b34a46de216903a47a7f7989f7f3df6"
ENV ZOHO_REFRESH_TOKEN="1000.9cd5d16a690f301935d011b537341ea6.c9366b41ce4662852b5725f5ce889d04"
# Install pip requirements
WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN python -m pip install -r requirements.txt
RUN pip install "unstructured[all-docs]"
RUN pip install PyPDF
RUN pip install fastapi uvicorn

COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3500"]
