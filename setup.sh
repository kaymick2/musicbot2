#!/bin/bash

set -e

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip
pip install spotipy rich yt-dlp
 
if ! command -v ffmpeg >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    echo "Installing ffmpeg via Homebrew..."
    brew install ffmpeg
  else
    echo "ffmpeg not found and Homebrew missing; please install ffmpeg manually."
  fi
fi

if [ ! -f ".env" ]; then
  echo "Creating .env file..."
  cat > .env <<'EOF'
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
EOF
fi

echo ""
echo "Setup complete! Now you can run your scripts with:"
echo "source venv/bin/activate  # Activate the environment first"
echo "python spotify_liked_songs.py  # Then run your script"
echo ""
echo "Note: You must activate the virtual environment each time you open a new terminal"
echo "before running your scripts."
