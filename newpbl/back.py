import os
import shutil
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for all API routes

# Configuration
ROOT_DIR = os.path.abspath('managed_files')
os.makedirs(ROOT_DIR, exist_ok=True)

# Create default folders
DEFAULT_FOLDERS = ['Documents', 'Music', 'Videos', 'Photos']
for folder in DEFAULT_FOLDERS:
    os.makedirs(os.path.join(ROOT_DIR, folder), exist_ok=True)

DB_PATH = 'file_mgmt.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL UNIQUE,
        is_folder INTEGER NOT NULL,
        parent_id INTEGER
    )
    ''')
    conn.commit()
    conn.close()

# Database helper functions
def db_execute(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def db_fetch_one(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result

def db_fetch_all(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# File operations
def get_file_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
        return 'Documents'
    elif ext in ['.mp3', '.wav', '.ogg', '.flac']:
        return 'Music'
    elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv']:
        return 'Videos'
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
        return 'Photos'
    return None

# API Endpoints
@app.route('/api/list', methods=['GET'])
def list_files():
    path = request.args.get('path', '')
    abs_path = os.path.join(ROOT_DIR, path)
    
    if not os.path.exists(abs_path):
        return jsonify({'error': 'Directory not found'}), 404
    
    try:
        entries = []
        for entry in os.listdir(abs_path):
            entry_path = os.path.join(abs_path, entry)
            rel_path = os.path.join(path, entry).replace('\\', '/')
            entries.append({
                'name': entry,
                'path': rel_path,
                'is_folder': os.path.isdir(entry_path),
                'size': os.path.getsize(entry_path) if not os.path.isdir(entry_path) else 0
            })
        return jsonify(entries)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    path = request.args.get('path', '')
    safe_name = secure_filename(file.filename)
    
    # Auto-categorize if in root
    if path == '':
        category = get_file_category(safe_name)
        if category:
            path = category

    save_dir = os.path.join(ROOT_DIR, path)
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, safe_name)
    
    try:
        file.save(save_path)
        rel_path = os.path.join(path, safe_name).replace('\\', '/')
        db_execute(
            'INSERT INTO files (name, path, is_folder) VALUES (?, ?, 0)',
            (safe_name, rel_path)
        )
        return jsonify({'message': 'File uploaded', 'path': rel_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create_folder', methods=['POST'])
def create_folder():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    parent_path = data.get('parent_path', '')
    folder_name = data.get('folder_name')
    
    if not folder_name:
        return jsonify({'error': 'Folder name required'}), 400
    
    safe_name = secure_filename(folder_name)
    folder_path = os.path.join(ROOT_DIR, parent_path, safe_name)
    
    if os.path.exists(folder_path):
        return jsonify({'error': 'Folder exists'}), 400
    
    try:
        os.makedirs(folder_path)
        rel_path = os.path.join(parent_path, safe_name).replace('\\', '/')
        db_execute(
            'INSERT INTO files (name, path, is_folder) VALUES (?, ?, 1)',
            (safe_name, rel_path)
        )
        return jsonify({'message': 'Folder created', 'path': rel_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/read', methods=['GET'])
def read_file():
    path = request.args.get('path', '')
    abs_path = os.path.join(ROOT_DIR, path)
    
    if not os.path.exists(abs_path):
        return jsonify({'error': 'File not found'}), 404
    if os.path.isdir(abs_path):
        return jsonify({'error': 'Cannot read folders'}), 400
    
    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rename', methods=['POST'])
def rename_file():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    old_path = data.get('old_path')
    new_name = data.get('new_name')
    
    if not old_path or not new_name:
        return jsonify({'error': 'Path and name required'}), 400
    
    abs_old_path = os.path.join(ROOT_DIR, old_path)
    if not os.path.exists(abs_old_path):
        return jsonify({'error': 'Path not found'}), 404
    
    parent = os.path.dirname(abs_old_path)
    abs_new_path = os.path.join(parent, secure_filename(new_name))
    
    try:
        os.rename(abs_old_path, abs_new_path)
        rel_new_path = os.path.join(os.path.dirname(old_path), new_name).replace('\\', '/')
        db_execute(
            'UPDATE files SET name=?, path=? WHERE path=?',
            (new_name, rel_new_path, old_path)
        )
        return jsonify({'message': 'Renamed', 'new_path': rel_new_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete', methods=['POST'])
def delete_file():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    path = data.get('path')
    if not path:
        return jsonify({'error': 'Path required'}), 400
    
    abs_path = os.path.join(ROOT_DIR, path)
    if not os.path.exists(abs_path):
        return jsonify({'error': 'Path not found'}), 404
    
    try:
        if os.path.isdir(abs_path):
            shutil.rmtree(abs_path)
        else:
            os.remove(abs_path)
        db_execute('DELETE FROM files WHERE path=?', (path,))
        return jsonify({'message': 'Deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['GET'])
def download_file():
    path = request.args.get('path', '')
    if not path:
        return jsonify({'error': 'Path required'}), 400
    
    abs_path = os.path.join(ROOT_DIR, path)
    if not os.path.exists(abs_path):
        return jsonify({'error': 'File not found'}), 404
    if os.path.isdir(abs_path):
        return jsonify({'error': 'Cannot download folder'}), 400
    
    directory = os.path.dirname(abs_path)
    filename = os.path.basename(abs_path)
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)