```markdown
# EE677 Project: Data Collection and Processing

This project automates the collection and processing of energy data from a specified source, storing it securely on Google Drive. It is designed to run on a cloud platform (Render) to ensure that local computers are not occupied. The data collection process is automated using a scheduled cron job.

## Table of Contents

1. [Setting Up the System and Running the Data Collection](#setting-up-the-system-and-running-the-data-collection)
    - [Step 1: Setting Up the Local Environment](#step-1-setting-up-the-local-environment)
    - [Step 2: Setting Up Google Drive Credentials](#step-2-setting-up-google-drive-credentials)
    - [Step 3: Running the Data Collection Locally](#step-3-running-the-data-collection-locally)
2. [Filling the .env File](#filling-the-env-file)
    - [Steps to Fill the .env File](#steps-to-fill-the-env-file)
    - [How to Find the Values](#how-to-find-the-values)
3. [Additional Notes](#additional-notes)

---

## Setting Up the System and Running the Data Collection

In this section, we will describe the process of setting up the environment for running the project locally. This process includes setting up Google Drive credentials, preparing the project repository, and ensuring that the system is automated for seamless execution.

### Step 1: Setting Up the Local Environment

Before setting up the deployment environment, we need to ensure that everything works correctly on the local system. This is an important first step to ensure that all dependencies and configurations are properly installed.

#### 1.1 Install Dependencies

**Clone the Repository:**

First, clone the project repository from GitHub to your local machine:

```bash
git clone https://github.com/Swapn2003/ee677_project_render.git
cd ee677_project_render
```

**Create a Virtual Environment:**

Create a virtual environment to manage dependencies:

```bash
python -m venv venv
```

**Activate the Virtual Environment:**

Activate the virtual environment based on your operating system:

For Windows:

```bash
.\venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

**Install Required Dependencies:**

Install the dependencies specified in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

### Step 2: Setting Up Google Drive Credentials

The project requires access to Google Drive to collect and store data. To set up Google Drive credentials, follow the steps below:

**Enable Google Drive API:**

- Go to the Google Cloud Console.
- Create a new project or select an existing one.
- Navigate to `APIs & Services > Library`.
- Search for Google Drive API and enable it.

**Create OAuth 2.0 Credentials:**

- Go to `APIs & Services > Credentials`.
- Click `Create Credentials` and choose `OAuth 2.0 Client IDs`.
- Select `Web application` and provide the required details.
- Download the `credentials.json` file.

---

### Step 3: Running the Data Collection Locally

Once everything is set up, you can test the data collection locally by running the main script:

```bash
python app.py
```

This will start collecting data and save it in the specified location (e.g., Google Drive or local storage).

---

## Filling the .env File

To fill in the details in the `.env` file, you need to extract the necessary credentials from the `credentials.json` file that you obtained while setting up Google Drive API.

### Steps to Fill the .env File

**Locate the credentials.json:** This file is downloaded from the Google Cloud Console and contains the required information for setting up OAuth 2.0 authentication.

**Extract the Required Fields:** Open the `credentials.json` file and extract the following fields. You will use these values to fill in the `.env` file.

### How to Find the Values:

- **GDRIVE_TYPE:** Set this to `installed` since this comes from OAuth credentials in `credentials.json`.
- **GDRIVE_PROJECT_ID:** This is your Google Cloud Project ID from `credentials.json`.
- **GDRIVE_PRIVATE_KEY_ID:** This is the private key ID in `credentials.json`.
- **GDRIVE_PRIVATE_KEY:** This will be the `private_key` field from the `credentials.json`. Be sure to maintain the formatting, especially the newline characters (`\n`).
- **GDRIVE_CLIENT_EMAIL:** This is the email address tied to your Google API project (found in `credentials.json`).
- **GDRIVE_CLIENT_ID:** This is your Client ID for OAuth from `credentials.json`.
- **GDRIVE_AUTH_URI, GDRIVE_TOKEN_URI, GDRIVE_AUTH_PROVIDER_CERT_URL, GDRIVE_CLIENT_CERT_URL:** These URLs are standard and can be directly copied from `credentials.json`.

---

## Additional Notes

- **Cron Job Setup**: The data collection process is automated using Fast Cron, running the script daily at 23:50 UTC on the cloud server.
- **Email Notifications**: Successful runs will be notified via email, ensuring the process runs without manual intervention.

---

This project is done under EE677 Course.

```

### Explanation of Sections:

1. **Project Overview**: The project aims to automate data collection and processing while avoiding the occupation of local computing resources. The data is stored in Google Drive, and the process is automated via cron jobs.

2. **Table of Contents**: Allows users to navigate through the README easily.

3. **Setting Up the System and Running the Data Collection**: Provides steps for installing dependencies, setting up the environment, and ensuring everything is ready for execution.

4. **Filling the .env File**: Explains how to extract credentials from the `credentials.json` file to fill in the `.env` file for accessing Google APIs securely.

5. **Additional Notes**: Describes how the process is automated and how the user will be notified via email for successful runs.

### Important Notes:
- Ensure to replace any example URLs or placeholders (`YOUR_CLIENT_ID`, `YOUR_PROJECT_ID`, etc.) with the actual values in your setup.
- This README is structured to be user-friendly and provides detailed instructions for setting up the environment and running the system locally. It also explains how to use the `.env` file and automate the data collection process.