# Setup Instructions for MusicBot

## Issue with pipx installation

You mentioned that you installed spotipy using pipx, but are having trouble accessing it in your scripts. This is because pipx installs packages in isolated environments, which aren't automatically accessible to your Python scripts.

## Solution: Use a Virtual Environment

I've created a virtual environment and a setup script to help you get started properly:

### Step 1: Run the setup script

```bash
./setup.sh
```

This script will:
1. Activate the virtual environment I created
2. Install spotipy and its dependencies in this environment
3. Provide instructions for running your scripts

### Step 2: Running your scripts

After running the setup script, you can run your scripts with:

```bash
source venv/bin/activate  # Activate the environment first
python spotify_liked_songs.py  # Then run your script
```

### Important Notes

- You must activate the virtual environment **each time** you open a new terminal before running your scripts
- The virtual environment keeps your dependencies isolated and organized
- This approach is more reliable than using pipx for libraries you need to import in your scripts

## Alternative: Using pipx-installed spotipy

If you prefer to use the pipx installation, you would need to:

1. Find the path to the pipx-installed spotipy package:
   ```
   pipx list  # Shows spotipy is installed at /Users/kjmcdowell/.local/pipx/venvs
   ```

2. Add that path to your PYTHONPATH environment variable before running scripts:
   ```bash
   export PYTHONPATH="$PYTHONPATH:/Users/kjmcdowell/.local/pipx/venvs/spotipy/lib/python3.13/site-packages"
   python spotify_liked_songs.py
   ```

However, the virtual environment approach is recommended for better dependency management.