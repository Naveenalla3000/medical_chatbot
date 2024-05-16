import os
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s:%(message)s:]'
)

list_of_files = [
    "src/__init__.py",
    "requirements.txt",
    "src/helper.py",
    "src/prompt.py",
    "setup.py",
    "app.py",
    "store_index.py",
    "public/.gitkeep",
    "public/css/style.css",
]

for file_path in list_of_files:
    file_path = Path(file_path)
    filedir, filename = os.path.split(file_path)
    
    if filedir !='':
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for file: {filename}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, 'w') as f:
            pass
            logging.info(f"Created empty file: {filename}")
    else:
        logging.info(f"File: {filename} already exists")