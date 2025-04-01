## Installation

```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

```
cd frontend
npm install
```

### Setting up image to text

Download the installer from https://github.com/UB-Mannheim/tesseract/wiki

Run the installer (e.g., `tesseract-ocr-w64-setup-v5.x.x.exe`).
During installation:

- Ensure you select the Arabic language pack (for your use case).
- Note the installation path (default is `C:\Program Files\Tesseract-OCR`).

Add `C:\Program Files\Tesseract-OCR` to path

### Run the App

```
python run.py
```

or for debugging

```
cd backend
python app.py
```

in another terminal

```
cd frontend/
npm run dev
```

### Scrapping news

```
python ./scrapping/run.py
```
