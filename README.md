# File-manager
To upload or modify files in the pc.

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Advanced File Manager</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --primary-color: #4a76a8;
      --secondary-color: #5d8cc0;
      --danger-color: #e74c3c;
      --success-color: #2ecc71;
      --warning-color: #f39c12;
      --light-color: #f8f9fa;
      --dark-color: #343a40;
      --border-color: #e1e4e8;
      --text-color: #333;
      --text-light: #6c757d;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #f5f7fa;
      color: var(--text-color);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }

    header {
      background-color: var(--primary-color);
      color: white;
      padding: 1rem;
      font-size: 1.5rem;
      font-weight: bold;
      display: flex;
      align-items: center;
      gap: 1rem;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    #pathBreadcrumb {
      background: white;
      padding: 0.75rem 1.5rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.9rem;
    }

    #pathBreadcrumb span {
      cursor: pointer;
      color: var(--primary-color);
      user-select: none;
      display: flex;
      align-items: center;
      gap: 0.3rem;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
    }

    #pathBreadcrumb span:hover {
      background-color: #f0f7ff;
    }

    #pathBreadcrumb .separator {
      color: var(--text-light);
      cursor: default;
    }

    #controls {
      background: white;
      padding: 0.75rem 1.5rem;
      display: flex;
      gap: 0.8rem;
      border-bottom: 1px solid var(--border-color);
      align-items: center;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    button {
      background-color: var(--primary-color);
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.9rem;
    }

    button:hover {
      background-color: var(--secondary-color);
      transform: translateY(-1px);
    }

    button:active {
      transform: translateY(0);
    }

    button:disabled {
      background-color: #cccccc;
      cursor: not-allowed;
    }

    button i {
      font-size: 0.9em;
    }

    .btn-danger {
      background-color: var(--danger-color);
    }

    .btn-success {
      background-color: var(--success-color);
    }

    .btn-warning {
      background-color: var(--warning-color);
    }

    #fileList {
      flex: 1;
      overflow-y: auto;
      background: white;
      padding: 1rem;
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    th, td {
      text-align: left;
      padding: 0.75rem;
      border-bottom: 1px solid var(--border-color);
    }

    th {
      background-color: #f8f9fa;
      font-weight: 600;
      color: var(--text-light);
      position: sticky;
      top: 0;
    }

    tr:hover {
      background-color: #f0f7ff;
    }

    tr.selected {
      background-color: #e1ecf7;
    }

    .file-icon {
      color: var(--text-light);
    }

    .folder-icon {
      color: var(--warning-color);
    }

    .doc-icon {
      color: #2196f3;
    }

    .music-icon {
      color: #9c27b0;
    }

    .video-icon {
      color: #f44336;
    }

    .image-icon {
      color: #4caf50;
    }

    #contextMenu {
      position: absolute;
      background: white;
      box-shadow: 0 2px 10px rgba(0,0,0,0.15);
      border-radius: 6px;
      z-index: 999;
      display: none;
      min-width: 180px;
      overflow: hidden;
    }

    #contextMenu ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    #contextMenu li {
      padding: 10px 15px;
      cursor: pointer;
      user-select: none;
      display: flex;
      align-items: center;
      gap: 0.8rem;
      font-size: 0.9rem;
    }

    #contextMenu li:hover {
      background-color: #f0f7ff;
      color: var(--primary-color);
    }

    #contextMenu li i {
      width: 16px;
      text-align: center;
    }

    .menu-separator {
      border-top: 1px solid var(--border-color);
      margin: 5px 0;
    }

    #message {
      text-align: center;
      padding: 0.5rem;
      font-weight: 600;
      color: var(--danger-color);
      flex-grow: 1;
    }

    .quick-access {
      display: flex;
      gap: 0.8rem;
      margin-left: auto;
    }

    .quick-access-btn {
      background: none;
      color: var(--primary-color);
      padding: 0.5rem;
      border-radius: 50%;
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .quick-access-btn:hover {
      background-color: #f0f7ff;
      transform: scale(1.1);
    }

    .status-bar {
      background: white;
      padding: 0.5rem 1rem;
      border-top: 1px solid var(--border-color);
      font-size: 0.8rem;
      color: var(--text-light);
      display: flex;
      justify-content: space-between;
    }

    .action-btn {
      background: none;
      border: none;
      color: var(--primary-color);
      cursor: pointer;
      padding: 0.3rem;
      border-radius: 4px;
      transition: all 0.2s ease;
    }

    .action-btn:hover {
      background-color: #f0f7ff;
      transform: scale(1.1);
    }

    .modal {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0,0,0,0.5);
      z-index: 1000;
      justify-content: center;
      align-items: center;
    }

    .modal-content {
      background: white;
      padding: 1.5rem;
      border-radius: 8px;
      width: 80%;
      max-width: 600px;
      max-height: 80vh;
      overflow: auto;
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--border-color);
    }

    .modal-close {
      background: none;
      border: none;
      font-size: 1.5rem;
      cursor: pointer;
      color: var(--text-light);
    }

    .preview-container {
      margin-top: 1rem;
      max-height: 60vh;
      overflow: auto;
    }

    .preview-image {
      max-width: 100%;
      max-height: 300px;
      display: block;
      margin: 0 auto;
    }

    .preview-audio, .preview-video {
      width: 100%;
      margin: 1rem 0;
    }

    .empty-folder {
      text-align: center;
      padding: 2rem;
      color: var(--text-light);
    }
  </style>
</head>
<body>
  <header>
    <i class="fas fa-folder-open"></i>
    <span>Advanced File Manager</span>
  </header>

  <nav id="pathBreadcrumb" aria-label="Path Breadcrumb"></nav>

  <div id="controls">
    <input type="file" id="fileInput" style="display:none" multiple />
    <button id="btnUpload">
      <i class="fas fa-upload"></i> Upload
    </button>
    <button id="btnCreateFolder">
      <i class="fas fa-folder-plus"></i> New Folder
    </button>
    <button id="btnCreateFile">
      <i class="fas fa-file-alt"></i> New File
    </button>
    <button id="btnPaste" disabled>
      <i class="fas fa-paste"></i> Paste
    </button>
    <button id="btnDelete" class="btn-danger" disabled>
      <i class="fas fa-trash"></i> Delete
    </button>
    
    <div class="quick-access">
      <button class="quick-access-btn" title="Documents" onclick="openPath('Documents')">
        <i class="fas fa-file-word"></i>
      </button>
      <button class="quick-access-btn" title="Music" onclick="openPath('Music')">
        <i class="fas fa-music"></i>
      </button>
      <button class="quick-access-btn" title="Videos" onclick="openPath('Videos')">
        <i class="fas fa-video"></i>
      </button>
      <button class="quick-access-btn" title="Photos" onclick="openPath('Photos')">
        <i class="fas fa-image"></i>
      </button>
    </div>
    
    <span id="message"></span>
  </div>

  <section id="fileList" role="region" aria-live="polite" aria-label="Files and folders list">
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th>Size</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody id="filesTableBody">
        <!-- Content will be populated by JavaScript -->
      </tbody>
    </table>
  </section>

  <div class="status-bar">
    <span id="statusInfo">Ready</span>
    <span id="itemCount">0 items</span>
  </div>

  <!-- Context Menu -->
  <div id="contextMenu" role="menu">
    <ul>
      <li id="ctxOpen"><i class="fas fa-folder-open"></i> Open</li>
      <li id="ctxView"><i class="fas fa-eye"></i> View</li>
      <li id="ctxRename"><i class="fas fa-edit"></i> Rename</li>
      <li id="ctxDownload"><i class="fas fa-download"></i> Download</li>
      <li class="menu-separator"></li>
      <li id="ctxCut"><i class="fas fa-cut"></i> Cut</li>
      <li id="ctxCopy"><i class="fas fa-copy"></i> Copy</li>
      <li id="ctxDelete" class="text-danger"><i class="fas fa-trash"></i> Delete</li>
    </ul>
  </div>

  <!-- Preview Modal -->
  <div id="previewModal" class="modal">
    <div class="modal-content">
      <div class="modal-header">
        <h3 id="previewTitle">File Preview</h3>
        <button class="modal-close" onclick="closePreviewModal()">&times;</button>
      </div>
      <div class="preview-container" id="previewContent">
        <!-- Preview content will be inserted here -->
      </div>
    </div>
  </div>

<script>
  // Configuration
  const API_BASE = window.location.origin.includes('127.0.0.1') 
    ? 'http://127.0.0.1:5000/api' 
    : '/api';
  
  // State management
  let currentPath = '';
  let files = [];
  let selectedItem = null;
  let clipboard = null;
  let lastSelectedItem = null;

  // DOM Elements
  const pathBreadcrumb = document.getElementById('pathBreadcrumb');
  const filesTableBody = document.getElementById('filesTableBody');
  const fileInput = document.getElementById('fileInput');
  const btnUpload = document.getElementById('btnUpload');
  const btnCreateFolder = document.getElementById('btnCreateFolder');
  const btnCreateFile = document.getElementById('btnCreateFile');
  const btnPaste = document.getElementById('btnPaste');
  const btnDelete = document.getElementById('btnDelete');
  const messageEl = document.getElementById('message');
  const statusInfo = document.getElementById('statusInfo');
  const itemCount = document.getElementById('itemCount');

  // Context Menu Elements
  const contextMenu = document.getElementById('contextMenu');
  const ctxOpen = document.getElementById('ctxOpen');
  const ctxView = document.getElementById('ctxView');
  const ctxRename = document.getElementById('ctxRename');
  const ctxDownload = document.getElementById('ctxDownload');
  const ctxCut = document.getElementById('ctxCut');
  const ctxCopy = document.getElementById('ctxCopy');
  const ctxDelete = document.getElementById('ctxDelete');

  // Modal Elements
  const previewModal = document.getElementById('previewModal');
  const previewTitle = document.getElementById('previewTitle');
  const previewContent = document.getElementById('previewContent');

  // Utility Functions
  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  function showMessage(msg, isError = false) {
    messageEl.textContent = msg;
    messageEl.style.color = isError ? 'var(--danger-color)' : 'var(--success-color)';
    setTimeout(() => { messageEl.textContent = ''; }, 3000);
  }

  function updateStatus(info) {
    statusInfo.textContent = info;
  }

  function updateItemCount() {
    const count = files.length;
    itemCount.textContent = `${count} item${count !== 1 ? 's' : ''}`;
  }

  function updatePasteButton() {
    btnPaste.disabled = !clipboard;
    btnPaste.title = clipboard 
      ? `${clipboard.action === 'cut' ? 'Move' : 'Copy'} "${clipboard.item.dataset.name}" here`
      : 'Clipboard empty';
  }

  function updateDeleteButton() {
    btnDelete.disabled = !selectedItem;
  }

  // API Functions
  async function apiRequest(endpoint, method = 'GET', body = null) {
    const options = {
      method,
      headers: {}
    };

    if (body) {
      if (body instanceof FormData) {
        options.body = body;
      } else {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(body);
      }
    }

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, options);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || 'Request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      showMessage(error.message, true);
      throw error;
    }
  }

  async function apiList(path) {
    return apiRequest(`/list?path=${encodeURIComponent(path || '')}`);
  }

  async function apiUpload(file, path) {
    const formData = new FormData();
    formData.append('file', file);
    return apiRequest(`/upload?path=${encodeURIComponent(path)}`, 'POST', formData);
  }

  async function apiCreateFolder(parent_path, folder_name) {
    return apiRequest('/create_folder', 'POST', { parent_path, folder_name });
  }

  async function apiCreateFile(parent_path, file_name) {
    return apiRequest('/create_file', 'POST', { parent_path, file_name });
  }

  async function apiRead(path) {
    return apiRequest(`/read?path=${encodeURIComponent(path)}`);
  }

  async function apiRename(old_path, new_name) {
    return apiRequest('/rename', 'POST', { old_path, new_name });
  }

  async function apiDelete(path) {
    return apiRequest('/delete', 'POST', { path });
  }

  async function apiMove(src_path, dest_path) {
    return apiRequest('/move', 'POST', { src_path, dest_path });
  }

  async function apiCopy(src_path, dest_path) {
    return apiRequest('/copy', 'POST', { src_path, dest_path });
  }

  async function apiDownload(path) {
    window.location.href = `${API_BASE}/download?path=${encodeURIComponent(path)}`;
  }

  // UI Rendering Functions
  function getFileIcon(filename, isFolder) {
    if (isFolder) return 'fas fa-folder';
    
    const ext = filename.split('.').pop().toLowerCase();
    switch(ext) {
      case 'pdf': return 'fas fa-file-pdf';
      case 'doc': case 'docx': return 'fas fa-file-word';
      case 'xls': case 'xlsx': return 'fas fa-file-excel';
      case 'ppt': case 'pptx': return 'fas fa-file-powerpoint';
      case 'txt': return 'fas fa-file-alt';
      case 'jpg': case 'jpeg': case 'png': case 'gif': case 'bmp': case 'webp': return 'fas fa-file-image';
      case 'mp3': case 'wav': case 'ogg': case 'flac': return 'fas fa-file-audio';
      case 'mp4': case 'avi': case 'mov': case 'mkv': return 'fas fa-file-video';
      case 'zip': case 'rar': case '7z': return 'fas fa-file-archive';
      default: return 'fas fa-file';
    }
  }

  function getFolderIcon(folderName) {
    switch(folderName) {
      case 'Documents': return 'fas fa-file-word';
      case 'Music': return 'fas fa-music';
      case 'Videos': return 'fas fa-video';
      case 'Photos': return 'fas fa-image';
      default: return 'fas fa-folder';
    }
  }

  function renderBreadcrumb() {
    pathBreadcrumb.innerHTML = '';
    
    // Root link
    const rootSpan = document.createElement('span');
    rootSpan.innerHTML = '<i class="fas fa-home"></i> Root';
    rootSpan.onclick = () => openPath('');
    pathBreadcrumb.appendChild(rootSpan);
    
    if (!currentPath) return;
    
    // Path segments
    const parts = currentPath.split('/');
    let accumulatedPath = '';
    
    parts.forEach((part, index) => {
      accumulatedPath += (accumulatedPath ? '/' : '') + part;
      
      // Separator
      const separator = document.createElement('span');
      separator.className = 'separator';
      separator.innerHTML = '<i class="fas fa-chevron-right"></i>';
      pathBreadcrumb.appendChild(separator);
      
      // Path segment
      const span = document.createElement('span');
      span.innerHTML = `<i class="${getFolderIcon(part)}"></i> ${part}`;
      span.onclick = () => openPath(accumulatedPath);
      pathBreadcrumb.appendChild(span);
    });
  }

  function renderFileList() {
    filesTableBody.innerHTML = '';
    
    // Parent directory link
    if (currentPath) {
      const tr = document.createElement('tr');
      tr.className = 'folder-icon';
      tr.innerHTML = `
        <td><i class="fas fa-level-up-alt"></i> <strong>..</strong></td>
        <td>Folder</td>
        <td>-</td>
        <td></td>
      `;
      tr.onclick = () => {
        const parent = currentPath.split('/').slice(0, -1).join('/');
        openPath(parent);
      };
      filesTableBody.appendChild(tr);
    }
    
    // Empty folder message
    if (files.length === 0 && !currentPath) {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td colspan="4" class="empty-folder">
          <i class="fas fa-folder-open" style="font-size: 2rem; margin-bottom: 1rem;"></i>
          <p>This folder is empty</p>
          <p>Upload or create new files/folders to get started</p>
        </td>
      `;
      filesTableBody.appendChild(tr);
      return;
    }
    
    // Files and folders
    files.forEach(file => {
      const tr = document.createElement('tr');
      tr.dataset.path = file.path;
      tr.dataset.name = file.name;
      tr.dataset.isFolder = file.is_folder ? 'true' : 'false';
      
      const icon = file.is_folder 
        ? `<i class="${getFolderIcon(file.name)}"></i>` 
        : `<i class="${getFileIcon(file.name, false)}"></i>`;
      
      const size = file.is_folder ? '-' : formatFileSize(file.size || 0);
      
      tr.innerHTML = `
        <td>${icon} ${file.name}</td>
        <td>${file.is_folder ? 'Folder' : 'File'}</td>
        <td>${size}</td>
        <td>
          <button class="action-btn" title="View" onclick="viewItem('${file.path}', ${file.is_folder})">
            <i class="fas fa-eye"></i>
          </button>
          <button class="action-btn" title="Download" onclick="downloadItem('${file.path}', ${file.is_folder})">
            <i class="fas fa-download"></i>
          </button>
          <button class="action-btn" title="Rename" onclick="renameItem('${file.path}', '${file.name}')">
            <i class="fas fa-edit"></i>
          </button>
        </td>
      `;
      
      // Click handling
      tr.onclick = (e) => {
        if (!e.target.closest('.action-btn')) {
          selectItem(tr);
        }
      };
      
      // Double click to open folders
      tr.ondblclick = (e) => {
        if (file.is_folder && !e.target.closest('.action-btn')) {
          openPath(file.path);
        }
      };
      
      // Right-click context menu
      tr.oncontextmenu = (e) => {
        e.preventDefault();
        selectItem(tr);
        openContextMenu(e.clientX, e.clientY);
      };
      
      filesTableBody.appendChild(tr);
    });
    
    updateItemCount();
  }

  // File Operations
  async function openPath(path) {
    try {
      updateStatus('Loading...');
      files = await apiList(path);
      currentPath = path;
      renderBreadcrumb();
      renderFileList();
      deselectItem();
      updatePasteButton();
      updateStatus('Ready');
    } catch (error) {
      console.error('Error opening path:', error);
      updateStatus('Error loading directory');
    }
  }

  async function uploadFiles() {
    if (!fileInput.files.length) return;
    
    try {
      updateStatus('Uploading files...');
      const uploadPromises = Array.from(fileInput.files).map(file => 
        apiUpload(file, currentPath)
      );
      
      await Promise.all(uploadPromises);
      showMessage('Files uploaded successfully');
      await openPath(currentPath);
    } catch (error) {
      console.error('Upload error:', error);
    } finally {
      fileInput.value = '';
      updateStatus('Ready');
    }
  }

  async function createFolder() {
    const folderName = prompt('Enter new folder name:');
    if (!folderName) return;
    
    try {
      updateStatus('Creating folder...');
      await apiCreateFolder(currentPath, folderName);
      showMessage('Folder created successfully');
      await openPath(currentPath);
    } catch (error) {
      console.error('Create folder error:', error);
    } finally {
      updateStatus('Ready');
    }
  }

  async function createFile() {
    const fileName = prompt('Enter new file name:');
    if (!fileName) return;
    
    try {
      updateStatus('Creating file...');
      await apiCreateFile(currentPath, fileName);
      showMessage('File created successfully');
      await openPath(currentPath);
    } catch (error) {
      console.error('Create file error:', error);
    } finally {
      updateStatus('Ready');
    }
  }

  async function deleteSelectedItem() {
    if (!selectedItem) {
      showMessage('No item selected', true);
      return;
    }
    
    const path = selectedItem.dataset.path;
    const name = selectedItem.dataset.name;
    
    if (!confirm(`Are you sure you want to delete "${name}"?`)) return;
    
    try {
      updateStatus('Deleting...');
      await apiDelete(path);
      showMessage('Deleted successfully');
      await openPath(currentPath);
    } catch (error) {
      console.error('Delete error:', error);
    } finally {
      updateStatus('Ready');
    }
  }

  async function renameItem(path, oldName) {
    const newName = prompt('Enter new name:', oldName);
    if (!newName || newName === oldName) return;
    
    try {
      updateStatus('Renaming...');
      await apiRename(path, newName);
      showMessage('Renamed successfully');
      await openPath(currentPath);
    } catch (error) {
      console.error('Rename error:', error);
    } finally {
      updateStatus('Ready');
    }
  }

  async function viewItem(path, isFolder) {
    if (isFolder) {
      openPath(path);
      return;
    }
    
    try {
      updateStatus('Loading file...');
      const data = await apiRead(path);
      showPreview(path, data.content);
    } catch (error) {
      console.error('View error:', error);
    } finally {
      updateStatus('Ready');
    }
  }

  async function downloadItem(path, isFolder) {
    if (isFolder) {
      showMessage('Cannot download folders', true);
      return;
    }
    
    try {
      updateStatus('Preparing download...');
      await apiDownload(path);
    } catch (error) {
      console.error('Download error:', error);
    } finally {
      updateStatus('Ready');
    }
  }

  async function pasteItem() {
    if (!clipboard) {
      showMessage('Clipboard empty', true);
      return;
    }
    
    try {
      updateStatus(clipboard.action === 'cut' ? 'Moving...' : 'Copying...');
      
      if (clipboard.action === 'cut') {
        await apiMove(clipboard.item.dataset.path, currentPath);
        showMessage('Moved successfully');
      } else {
        await apiCopy(clipboard.item.dataset.path, currentPath);
        showMessage('Copied successfully');
      }
      
      clipboard = null;
      updatePasteButton();
      await openPath(currentPath);
    } catch (error) {
      console.error('Paste error:', error);
    } finally {
      updateStatus('Ready');
    }
  }

  // Preview Modal Functions
  function showPreview(path, content) {
    const filename = path.split('/').pop();
    previewTitle.textContent = `Preview: ${filename}`;
    previewContent.innerHTML = '';
    
    // Determine file type and render appropriate preview
    const ext = filename.split('.').pop().toLowerCase();
    
    if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(ext)) {
      // Image preview
      const img = document.createElement('img');
      img.src = `${API_BASE}/download?path=${encodeURIComponent(path)}`;
      img.className = 'preview-image';
      img.alt = filename;
      previewContent.appendChild(img);
    } else if (['mp3', 'wav', 'ogg'].includes(ext)) {
      // Audio preview
      const audio = document.createElement('audio');
      audio.controls = true;
      audio.className = 'preview-audio';
      const source = document.createElement('source');
      source.src = `${API_BASE}/download?path=${encodeURIComponent(path)}`;
      source.type = `audio/${ext}`;
      audio.appendChild(source);
      previewContent.appendChild(audio);
    } else if (['mp4', 'webm', 'ogg'].includes(ext)) {
      // Video preview
      const video = document.createElement('video');
      video.controls = true;
      video.className = 'preview-video';
      video.style.maxWidth = '100%';
      const source = document.createElement('source');
      source.src = `${API_BASE}/download?path=${encodeURIComponent(path)}`;
      source.type = `video/${ext}`;
      video.appendChild(source);
      previewContent.appendChild(video);
    } else {
      // Text preview
      const pre = document.createElement('pre');
      pre.textContent = content || '[Empty file or binary content]';
      previewContent.appendChild(pre);
    }
    
    previewModal.style.display = 'flex';
  }

  function closePreviewModal() {
    previewModal.style.display = 'none';
  }

  // Selection and Context Menu
  function selectItem(tr) {
    if (selectedItem) {
      selectedItem.classList.remove('selected');
    }
    
    selectedItem = tr;
    selectedItem.classList.add('selected');
    updateDeleteButton();
  }

  function deselectItem() {
    if (selectedItem) {
      selectedItem.classList.remove('selected');
      selectedItem = null;
    }
    updateDeleteButton();
  }

  function openContextMenu(x, y) {
    if (!selectedItem) return;
    
    // Position the context menu
    contextMenu.style.left = `${x}px`;
    contextMenu.style.top = `${y}px`;
    contextMenu.style.display = 'block';
    
    // Store last selected item for context menu actions
    lastSelectedItem = selectedItem;
  }

  function closeContextMenu() {
    contextMenu.style.display = 'none';
    lastSelectedItem = null;
  }

  // Event Listeners
  btnUpload.onclick = () => fileInput.click();
  fileInput.onchange = uploadFiles;
  btnCreateFolder.onclick = createFolder;
  btnCreateFile.onclick = createFile;
  btnPaste.onclick = pasteItem;
  btnDelete.onclick = deleteSelectedItem;

  // Context menu actions
  ctxOpen.onclick = () => {
    if (!lastSelectedItem) return;
    const isFolder = lastSelectedItem.dataset.isFolder === 'true';
    if (isFolder) {
      openPath(lastSelectedItem.dataset.path);
    } else {
      viewItem(lastSelectedItem.dataset.path, false);
    }
    closeContextMenu();
  };

  ctxView.onclick = () => {
    if (!lastSelectedItem) return;
    viewItem(lastSelectedItem.dataset.path, lastSelectedItem.dataset.isFolder === 'true');
    closeContextMenu();
  };

  ctxDownload.onclick = () => {
    if (!lastSelectedItem) return;
    downloadItem(lastSelectedItem.dataset.path, lastSelectedItem.dataset.isFolder === 'true');
    closeContextMenu();
  };

  ctxRename.onclick = () => {
    if (!lastSelectedItem) return;
    renameItem(lastSelectedItem.dataset.path, lastSelectedItem.dataset.name);
    closeContextMenu();
  };

  ctxCut.onclick = () => {
    if (!lastSelectedItem) return;
    clipboard = { action: 'cut', item: lastSelectedItem };
    showMessage(`"${lastSelectedItem.dataset.name}" cut to clipboard`);
    updatePasteButton();
    closeContextMenu();
  };

  ctxCopy.onclick = () => {
    if (!lastSelectedItem) return;
    clipboard = { action: 'copy', item: lastSelectedItem };
    showMessage(`"${lastSelectedItem.dataset.name}" copied to clipboard`);
    updatePasteButton();
    closeContextMenu();
  };

  ctxDelete.onclick = () => {
    closeContextMenu();
    deleteSelectedItem();
  };

  // Global click handler to close context menu
  window.onclick = (e) => {
    if (e.target.closest('#contextMenu') === null) {
      closeContextMenu();
    }
  };

  // Keyboard shortcuts
  document.onkeydown = (e) => {
    if (e.key === 'Delete' && selectedItem) {
      deleteSelectedItem();
    } else if (e.key === 'F2' && selectedItem) {
      renameItem(selectedItem.dataset.path, selectedItem.dataset.name);
    } else if (e.key === 'Escape') {
      deselectItem();
      closeContextMenu();
    }
  };

  // Initialize
  openPath('');
</script>
</body>
</html>
