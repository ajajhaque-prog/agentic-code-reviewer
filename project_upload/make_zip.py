
import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', '.git', 'node_modules', 'Upload files']]
        
        for file in files:
            if file.endswith(('.zip', '.pdf', '.pyc')):
                continue
            
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, path)
            ziph.write(file_path, arcname)

if __name__ == '__main__':
    with zipfile.ZipFile('project_upload.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir('.', zipf)
    print("Created project_upload.zip")
