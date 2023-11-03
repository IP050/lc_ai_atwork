# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV FROM_EMAIL="info@jalapenosolutions.nl"
ENV SECOND_RECIPIENT="sales@jalapenosolutions.nl"
ENV THIRD_RECIPIENT="iepe@jalapenomarketing.nl" 
ENV DATABASE_URL="postgresql://jalapenopostgres:99fEQ8HDNtzhrAu@webapppostgres.postgres.database.azure.com/jpswebshop"
ENV SENDGRIP_API_KEY="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"
ENV ZOHO_CLIENT_ID="1000.CBIUBMS22MX0WXYW8CZ57F5Z86I0YI"
ENV ZOHO_CLIENT_SECRET="68d404fbea8b34a46de216903a47a7f7989f7f3df6"
ENV ZOHO_REFRESH_TOKEN="1000.9cd5d16a690f301935d011b537341ea6.c9366b41ce4662852b5725f5ce889d04"
# Install pip requirements
WORKDIR /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN pip install fastapi uvicorn
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3500"]
