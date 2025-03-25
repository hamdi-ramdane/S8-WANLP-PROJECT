```
pip install -r requirements.txt
```

```
cd frontend
npm install
```

### Setting up image to text

Download the installer from https://github.com/UB-Mannheim/tesseract/wiki
Run the installer (e.g., tesseract-ocr-w64-setup-v5.x.x.exe).
During installation:

- Ensure you select the Arabic language pack (for your use case).
- Note the installation path (default is C:\Program Files\Tesseract-OCR).

Add C:\Program Files\Tesseract-OCR to path

### Run the App

python app.py
cd frontend
npm start dev
