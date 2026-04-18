import os

# Project structure
folders = [
    "data",
    "outputs",
    "notebooks",
    "src",
    "images"
]

files = {
    "main.py": "# Main script for Expense Tracker\n",
    "app.py": "# Streamlit dashboard\n",
    "requirements.txt": "pandas\nnumpy\nmatplotlib\nseaborn\nstreamlit\nscikit-learn\n",
    "README.md": "# Expense Tracker App\n\nProject setup in progress...\n"
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file_name, content in files.items():
    with open(file_name, "w") as f:
        f.write(content)

print("✅ Project structure created successfully!")