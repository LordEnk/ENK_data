import os
from flask_uploads import UploadSet, configure_uploads, ALL

# Define the Flask app directory
app_directory = os.path.dirname(os.path.abspath(__file__))

# Create the "uploads" folder if it doesn't exist
uploads_folder = os.path.join(app_directory, 'uploads')
os.makedirs(uploads_folder, exist_ok=True)

# Define the allowed file extensions for all types of files
all_files = UploadSet('all_files', ALL)

# Configure Flask-Uploads with your app
configure_uploads(app, all_files)

print("Flask-Uploads setup complete.")
print(f"Uploads folder created at: {uploads_folder}")

