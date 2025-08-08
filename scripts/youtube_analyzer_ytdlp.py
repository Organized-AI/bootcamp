#!/usr/bin/env python3
"""
Alternative YouTube Playlist Extractor using yt-dlp
More robust and regularly updated for YouTube changes
"""

import os
import json
import subprocess
import sys
from datetime import datetime

def install_yt_dlp():
    """Install yt-dlp if not already installed"""
    try:
        import yt_dlp
        print("✅ yt-dlp is already installed")
    except ImportError:
        print("📦 Installing yt-dlp...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
        print("✅ yt-dlp installed successfully")

def get_playlist_info(playlist_url):
    """Extract playlist information using yt-dlp"""
    import yt_dlp
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(playlist_url, download=False)
            return info
        except Exception as e:
            print(f"❌ Error extracting playlist info: {e}")
            return None

def get_video_info_with_transcript(video_url):
    """Get video info and transcript using yt-dlp"""
    import yt_dlp
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            
            video_data = {
                'title': info.get('title', 'Unknown'),
                'url': video_url,
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'upload_date': info.get('upload_date', ''),
                'description': info.get('description', ''),
                'view_count': info.get('view_count', 0),
            }
            
            # Check for subtitles
            if 'subtitles' in info and 'en' in info['subtitles']:
                video_data['has_transcript'] = True
                video_data['transcript_type'] = 'manual'
            elif 'automatic_captions' in info and 'en' in info['automatic_captions']:
                video_data['has_transcript'] = True
                video_data['transcript_type'] = 'auto-generated'
            else:
                video_data['has_transcript'] = False
                video_data['transcript_type'] = None
            
            return video_data
            
        except Exception as e:
            print(f"   ❌ Error processing video: {e}")
            return None

def main():
    print("\n" + "="*60)
    print("🎓 VibeCoders YouTube Playlist Analyzer")
    print("Using yt-dlp for robust extraction")
    print("="*60 + "\n")
    
    # Install yt-dlp if needed
    install_yt_dlp()
    
    # Playlist URL
    playlist_url = "https://www.youtube.com/playlist?list=PLf2m23nhTg1P5BsOHUOXyQz5RhfUSSVUi"
    
    print(f"\n📋 Analyzing playlist: {playlist_url}")
    print("-" * 40)
    
    # Get playlist info
    playlist_info = get_playlist_info(playlist_url)
    
    if not playlist_info:
        print("❌ Failed to extract playlist information")
        return
    
    # Display playlist info
    print(f"\n📚 Playlist: {playlist_info.get('title', 'Unknown')}")
    print(f"📊 Total videos: {len(playlist_info.get('entries', []))}")
    print(f"👤 Uploader: {playlist_info.get('uploader', 'Unknown')}")
    
    # Create output directory
    output_dir = "vibecoder_curriculum_analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each video
    videos_data = []
    entries = playlist_info.get('entries', [])
    
    print(f"\n🎬 Processing {len(entries)} videos...")
    print("-" * 40)
    
    for idx, entry in enumerate(entries, 1):
        video_url = f"https://www.youtube.com/watch?v={entry['id']}"
        print(f"\n[{idx}/{len(entries)}] {entry.get('title', 'Unknown')}")
        
        video_info = get_video_info_with_transcript(video_url)
        
        if video_info:
            video_info['lesson_number'] = idx
            videos_data.append(video_info)
            
            # Display status
            if video_info['has_transcript']:
                print(f"   ✅ Transcript available ({video_info['transcript_type']})")
            else:
                print(f"   ⚠️  No transcript available")
            
            duration_min = video_info['duration'] // 60
            duration_sec = video_info['duration'] % 60
            print(f"   ⏱️  Duration: {duration_min}:{duration_sec:02d}")
            print(f"   👁️  Views: {video_info['view_count']:,}")
    
    # Save summary
    summary_file = os.path.join(output_dir, "playlist_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'playlist_title': playlist_info.get('title', 'Unknown'),
            'playlist_url': playlist_url,
            'total_videos': len(entries),
            'extraction_date': datetime.now().isoformat(),
            'videos': videos_data
        }, f, indent=2, ensure_ascii=False)
    
    # Create markdown summary
    md_file = os.path.join(output_dir, "curriculum_mapping.md")
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# VibeCoders Bootcamp - YouTube Content Mapping\n\n")
        f.write(f"**Playlist**: {playlist_info.get('title', 'Unknown')}\n")
        f.write(f"**Total Videos**: {len(entries)}\n")
        f.write(f"**Extracted**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        f.write("## Video List\n\n")
        f.write("| # | Title | Duration | Transcript | Views | Suggested Week |\n")
        f.write("|---|-------|----------|-----------|-------|----------------|\n")
        
        for video in videos_data:
            duration_min = video['duration'] // 60
            duration_sec = video['duration'] % 60
            duration_str = f"{duration_min}:{duration_sec:02d}"
            
            transcript_status = "✅" if video['has_transcript'] else "❌"
            views = f"{video['view_count']:,}" if video['view_count'] else "N/A"
            
            # Suggest week mapping based on video number
            if video['lesson_number'] <= 3:
                week = "Week 1"
            elif video['lesson_number'] <= 6:
                week = "Week 2"
            elif video['lesson_number'] <= 9:
                week = "Week 3"
            elif video['lesson_number'] <= 12:
                week = "Week 4"
            elif video['lesson_number'] <= 15:
                week = "Week 5"
            else:
                week = "Week 6"
            
            f.write(f"| {video['lesson_number']} | {video['title'][:50]}... | {duration_str} | {transcript_status} | {views} | {week} |\n")
        
        f.write("\n## Transcript Availability\n\n")
        videos_with_transcripts = sum(1 for v in videos_data if v['has_transcript'])
        f.write(f"- Videos with transcripts: {videos_with_transcripts}/{len(videos_data)}\n")
        f.write(f"- Videos without transcripts: {len(videos_data) - videos_with_transcripts}/{len(videos_data)}\n")
        
        f.write("\n## Next Steps\n\n")
        f.write("1. Download transcripts using yt-dlp with subtitle options\n")
        f.write("2. Map videos to specific curriculum weeks\n")
        f.write("3. Create sandbox exercises based on video content\n")
        f.write("4. Fill gaps with additional materials\n")
        
        f.write("\n## Download Command\n\n")
        f.write("To download transcripts for a specific video:\n")
        f.write("```bash\n")
        f.write("yt-dlp --write-sub --write-auto-sub --sub-lang en --skip-download [VIDEO_URL]\n")
        f.write("```\n")
    
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE!")
    print("="*60)
    print(f"\n📁 Files saved to: {output_dir}/")
    print(f"  - playlist_summary.json: Complete data in JSON format")
    print(f"  - curriculum_mapping.md: Markdown summary with week suggestions")
    print("\n🎯 Videos with transcripts: {}/{}".format(
        sum(1 for v in videos_data if v['has_transcript']),
        len(videos_data)
    ))
    
    # Print total duration
    total_duration = sum(v['duration'] for v in videos_data)
    hours = total_duration // 3600
    minutes = (total_duration % 3600) // 60
    print(f"⏱️  Total playlist duration: {hours}h {minutes}m")
    
    print("\n💡 Note: Use yt-dlp to download actual transcript files")
    print("   Example: yt-dlp --write-sub --write-auto-sub --sub-lang en --skip-download [URL]")

if __name__ == "__main__":
    main()
