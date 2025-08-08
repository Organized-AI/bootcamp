#!/usr/bin/env python3
"""
Download all transcripts from the YouTube playlist
"""

import os
import subprocess
import json
from datetime import datetime

def download_all_transcripts():
    """Download transcripts for all videos in the playlist"""
    
    playlist_url = "https://www.youtube.com/playlist?list=PLf2m23nhTg1P5BsOHUOXyQz5RhfUSSVUi"
    output_dir = "vibecoder_transcripts"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*60)
    print("📚 Downloading All Transcripts from YouTube Playlist")
    print("="*60)
    print(f"\nOutput directory: {output_dir}/")
    print("\nThis may take a few minutes...\n")
    
    # yt-dlp command to download all subtitles
    cmd = [
        "yt-dlp",
        "--write-sub",           # Download subtitles
        "--write-auto-sub",      # Download auto-generated if manual not available
        "--sub-lang", "en",      # English subtitles
        "--skip-download",       # Don't download videos
        "--sub-format", "vtt",   # WebVTT format (easier to parse)
        "--output", f"{output_dir}/%(playlist_index)s-%(title)s.%(ext)s",
        playlist_url
    ]
    
    try:
        # Run yt-dlp
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully downloaded transcripts!")
            
            # Count downloaded files
            vtt_files = [f for f in os.listdir(output_dir) if f.endswith('.vtt')]
            print(f"\n📄 Downloaded {len(vtt_files)} transcript files")
            
            # Create summary
            create_transcript_summary(output_dir, vtt_files)
            
        else:
            print(f"❌ Error downloading transcripts:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("❌ yt-dlp not found. Installing...")
        subprocess.run(["pip", "install", "yt-dlp"])
        print("Please run the script again.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def parse_vtt_file(filepath):
    """Parse a WebVTT file and extract text"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header and extract text
        text_lines = []
        is_text = False
        
        for line in lines:
            line = line.strip()
            
            # Skip timecodes and empty lines
            if '-->' in line or line == '' or line == 'WEBVTT':
                is_text = False
                continue
            
            # Skip line numbers
            if line.isdigit():
                continue
                
            # This is actual text
            text_lines.append(line)
        
        return ' '.join(text_lines)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return ""

def create_transcript_summary(output_dir, vtt_files):
    """Create a summary document with all transcripts"""
    
    summary_file = os.path.join(output_dir, "all_transcripts_summary.md")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# VibeCoders Bootcamp - All Video Transcripts\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Table of Contents\n\n")
        
        # Write TOC
        for i, vtt_file in enumerate(sorted(vtt_files), 1):
            title = vtt_file.replace('.en.vtt', '').replace('.vtt', '')
            # Remove number prefix
            if '-' in title:
                title = title.split('-', 1)[1]
            f.write(f"{i}. [{title}](#{i}-{title.lower().replace(' ', '-')})\n")
        
        f.write("\n---\n\n")
        
        # Write transcripts
        for i, vtt_file in enumerate(sorted(vtt_files), 1):
            filepath = os.path.join(output_dir, vtt_file)
            title = vtt_file.replace('.en.vtt', '').replace('.vtt', '')
            
            # Remove number prefix
            if '-' in title:
                title = title.split('-', 1)[1]
            
            print(f"Processing {i}/{len(vtt_files)}: {title[:50]}...")
            
            f.write(f"## {i}. {title}\n\n")
            
            # Parse and write transcript
            transcript_text = parse_vtt_file(filepath)
            
            if transcript_text:
                # Write first 500 characters as preview
                f.write("**Preview:**\n")
                f.write(f"> {transcript_text[:500]}...\n\n")
                
                # Write full transcript
                f.write("**Full Transcript:**\n\n")
                f.write(transcript_text)
            else:
                f.write("*Transcript not available or could not be parsed*\n")
            
            f.write("\n\n---\n\n")
    
    print(f"\n✅ Summary created: {summary_file}")
    print(f"   Total size: {os.path.getsize(summary_file) / 1024:.1f} KB")

def main():
    # Check if in virtual environment
    if not hasattr(sys, 'prefix'):
        print("⚠️  Not in virtual environment. Activating...")
        activate_cmd = "source venv_youtube/bin/activate && python3 download_transcripts.py"
        print(f"Run: {activate_cmd}")
        return
    
    download_all_transcripts()
    
    print("\n" + "="*60)
    print("✅ Transcript Download Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review transcripts in vibecoder_transcripts/")
    print("2. Use all_transcripts_summary.md for quick reference")
    print("3. Map content to curriculum weeks")

if __name__ == "__main__":
    import sys
    main()
