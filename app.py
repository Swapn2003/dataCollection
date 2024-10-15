import os
import io
import pandas as pd
import requests
from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Load environment variables
load_dotenv()

# Access environment variables
url = "https://eal.iitk.ac.in/home_data.php?action=india_generation"
FOLDER_ID = os.getenv('GDRIVE_FOLDER_ID')
SCOPES = [os.getenv('GDRIVE_SCOPES')]

# Configure Service Account Info with variables
SERVICE_ACCOUNT_INFO = {
    "type": os.getenv('GDRIVE_TYPE'),
    "project_id": os.getenv('GDRIVE_PROJECT_ID'),
    "private_key_id": os.getenv('GDRIVE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('GDRIVE_PRIVATE_KEY').replace("\\n", "\n"),
    "client_email": os.getenv('GDRIVE_CLIENT_EMAIL'),
    "client_id": os.getenv('GDRIVE_CLIENT_ID'),
    "auth_uri": os.getenv('GDRIVE_AUTH_URI'),
    "token_uri": os.getenv('GDRIVE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('GDRIVE_AUTH_PROVIDER_CERT_URL'),
    "client_x509_cert_url": os.getenv('GDRIVE_CLIENT_CERT_URL')
}

# Initialize Flask app
app = Flask(__name__)

# Google Drive upload function
def upload_to_drive(file_name, new_df):
    credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    results = service.files().list(q=f"'{FOLDER_ID}' in parents and name='{file_name}'", spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])

    if len(items) > 0:
        file_id = items[0]['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO(request.execute())
        existing_df = pd.read_excel(fh)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_excel(file_name, index=False)
        service.files().delete(fileId=file_id).execute()
    else:
        new_df.to_excel(file_name, index=False)
    
    file_metadata = {'name': file_name, 'parents': [FOLDER_ID]}
    media = MediaFileUpload(file_name, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

# Endpoint to extract data and upload it to Google Drive
@app.route('/extract', methods=['GET'])
def extract_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=om79kko0m2f71pr84iah672jhf; _gid=GA1.3.328912433.1728882804; _gat_gtag_UA_118899700_1=1; _ga_ZRZ8CCYXEE=GS1.1.1728889940.2.0.1728889951.0.0.0; _ga=GA1.3.92296772.1728882804',
        'Host': 'eal.iitk.ac.in',
        'Origin': 'https://eal.iitk.ac.in',
        'Referer': 'https://eal.iitk.ac.in/',
        'Sec-Ch-Ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        response = requests.get(url, headers=headers)
        print("helllo")
        if response.status_code == 200:
            data = response.json()
            print("data = ",data)
            records = [
                {
                    "start_time": item['block_time'],
                    "end_time": pd.to_datetime(item['block_time']) + pd.Timedelta(minutes=15),
                    "current_demand": item.get('current_demand', 'N/A'),
                    "thermal_generation": item.get('thermal_generation', 'N/A'),
                    "gas_generation": item.get('gas_generation', 'N/A'),
                    "nuclear_generation": item.get('nuclear_generation', 'N/A'),
                    "hydro_generation": item.get('hydro_generation', 'N/A'),
                    "renew_generation": item.get('renew_generation', 'N/A')
                }
                for item in data
            ]
            df = pd.DataFrame(records)
            current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
            file_name = f"generation_data_{current_time.strftime('%Y-%m-%d')}.xlsx"

            # file_name = "generation_data.xlsx"
            upload_to_drive(file_name, df)
            return jsonify({"message": "Data successfully uploaded to Google Drive"}), 200
        else:
            return jsonify({"error": "Failed to fetch data"}), response.status_code
    except Exception as e:
        # print("hello")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
