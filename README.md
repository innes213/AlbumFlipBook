# Album Cover Flipbook

A Python script that creates a video flipbook of your Discogs collection's album covers. The script fetches your collection from Discogs, downloads the album covers, and compiles them into a video using ffmpeg.

## Sample Output

[![Sample Output](sample.out.mp4)](sample.out.mp4)

## Prerequisites

- Python 3.6 or higher
- ffmpeg (for video creation)
- A Discogs account and API token

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/AlbumCoverFlipbook.git
cd AlbumCoverFlipbook
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install ffmpeg:
   - **macOS**:
     ```bash
     brew install ffmpeg
     ```
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get install ffmpeg
     ```
   - **Windows**:
     Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to your PATH

## Setting up Discogs API

1. Login to your discogs account [discogs.com](https://www.discogs.com) 
2. Go to your [Discogs Developer Settings](https://www.discogs.com/settings/developers)
3. Click "Generate new token"
4. Create a `.env` file in the project root with the following content:
```
DISCOGS_TOKEN=your_token_here
USER_AGENT=your_app_name/1.0
```
Replace `your_token_here` with your Discogs API token and `your_app_name` with a name for your application.

## Usage

1. Make sure your `.env` file is set up with your Discogs credentials
2. Run the script:
```bash
python album_cover_flipbook.py
```

The script will:
1. Fetch your Discogs collection
2. Sort albums by artist name
3. Download album covers
4. Create a video (out.mp4) of the album covers
5. Clean up temporary files

## Notes

- The discogs api is rate-limited. This script as is does not violate the limitation.
- The script creates a temporary `images` directory to store downloaded covers
- The final video is saved as `out.mp4`
- Album covers are sorted by artist name, ignoring common prefixes like "The", "A", "An", etc.
- The default video framerate is 5 frames per second
