#!/usr/bin/env python3
"""
YouTube Playlist Transcript Extractor for VibeCoders Bootcamp
Extracts video information and transcripts from a YouTube playlist
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
import time

# Required libraries - install with:
# pip install pytube youtube-transcript-api pandas tqdm

try:
    from pytube import Playlist, YouTube
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    from tqdm import tqdm
    import pandas as pd
except ImportError as e:
    print(f"Missing required library: {e}")
    print("\nPlease install required libraries:")
    print("pip install pytube youtube-transcript-api pandas tqdm")
    exit(1)

class PlaylistTranscriptExtractor:
    def __init__(self, playlist_url: str, output_dir: str = "bootcamp_content"):
        """
        Initialize the extractor with a playlist URL
        
        Args:
            playlist_url: YouTube playlist URL
            output_dir: Directory to save extracted content
        """
        self.playlist_url = playlist_url
        self.output_dir = output_dir
        self.playlist = None
        self.videos_data = []
        self.failed_videos = []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
    def extract_playlist_info(self) -> Dict:
        """Extract basic playlist information"""
        print(f"\n📋 Extracting playlist information...")
        try:
            self.playlist = Playlist(self.playlist_url)
            
            # Force playlist to load
            playlist_title = self.playlist.title or "Unknown Playlist"
            video_count = len(self.playlist.video_urls)
            
            playlist_info = {
                'title': playlist_title,
                'url': self.playlist_url,
                'video_count': video_count,
                'extraction_date': datetime.now().isoformat()
            }
            
            print(f"✅ Found playlist: {playlist_title}")
            print(f"📊 Total videos: {video_count}")
            
            return playlist_info
            
        except Exception as e:
            print(f"❌ Error extracting playlist info: {e}")
            return {}
    
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_transcript(self, video_id: str, video_title: str) -> Optional[Dict]:
        """
        Get transcript for a video
        
        Args:
            video_id: YouTube video ID
            video_title: Video title for logging
            
        Returns:
            Dictionary with transcript data or None if failed
        """
        try:
            # Try to get transcript in order of preference
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            transcript = None
            transcript_type = None
            
            # Try manual transcript first (most accurate)
            try:
                transcript = transcript_list.find_manually_created_transcript(['en'])
                transcript_type = "manual"
            except:
                # Try auto-generated transcript
                try:
                    transcript = transcript_list.find_generated_transcript(['en'])
                    transcript_type = "auto-generated"
                except:
                    pass
            
            if transcript:
                transcript_data = transcript.fetch()
                
                # Format transcript with timestamps
                formatted_with_timestamps = []
                formatted_text_only = []
                
                for entry in transcript_data:
                    timestamp = time.strftime('%M:%S', time.gmtime(entry['start']))
                    formatted_with_timestamps.append(f"[{timestamp}] {entry['text']}")
                    formatted_text_only.append(entry['text'])
                
                return {
                    'transcript_type': transcript_type,
                    'with_timestamps': '\n'.join(formatted_with_timestamps),
                    'text_only': ' '.join(formatted_text_only),
                    'raw_data': transcript_data
                }
                
        except TranscriptsDisabled:
            print(f"   ⚠️  Transcripts disabled for: {video_title}")
        except NoTranscriptFound:
            print(f"   ⚠️  No transcript found for: {video_title}")
        except Exception as e:
            print(f"   ❌ Error getting transcript for {video_title}: {e}")
        
        return None
    
    def process_videos(self) -> List[Dict]:
        """Process all videos in the playlist"""
        print(f"\n🎬 Processing videos...")
        
        for idx, video_url in enumerate(tqdm(self.playlist.video_urls, desc="Extracting transcripts")):
            video_num = idx + 1
            
            try:
                # Get video information
                video = YouTube(video_url)
                video_id = self.extract_video_id(video_url)
                
                video_data = {
                    'lesson_number': video_num,
                    'title': video.title,
                    'url': video_url,
                    'video_id': video_id,
                    'duration_seconds': video.length,
                    'duration_formatted': time.strftime('%H:%M:%S', time.gmtime(video.length)) if video.length else "Unknown",
                    'author': video.author,
                    'publish_date': video.publish_date.isoformat() if video.publish_date else None
                }
                
                # Get transcript
                transcript_data = self.get_video_transcript(video_id, video.title)
                
                if transcript_data:
                    video_data['transcript'] = transcript_data
                    video_data['has_transcript'] = True
                else:
                    video_data['transcript'] = None
                    video_data['has_transcript'] = False
                    self.failed_videos.append(video_data['title'])
                
                self.videos_data.append(video_data)
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"\n❌ Error processing video {video_num}: {e}")
                self.failed_videos.append(f"Video {video_num}")
                continue
        
        print(f"\n✅ Successfully processed {len(self.videos_data)} videos")
        if self.failed_videos:
            print(f"⚠️  Failed to get transcripts for {len(self.failed_videos)} videos")
        
        return self.videos_data
    
    def save_individual_lessons(self):
        """Save each lesson as a separate markdown file"""
        lessons_dir = os.path.join(self.output_dir, "lessons")
        os.makedirs(lessons_dir, exist_ok=True)
        
        print(f"\n📁 Saving individual lesson files...")
        
        for video in self.videos_data:
            filename = f"lesson_{video['lesson_number']:02d}_{self.sanitize_filename(video['title'])}.md"
            filepath = os.path.join(lessons_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write lesson header
                f.write(f"# Lesson {video['lesson_number']}: {video['title']}\n\n")
                f.write(f"**Video URL**: {video['url']}\n")
                f.write(f"**Duration**: {video['duration_formatted']}\n")
                f.write(f"**Author**: {video['author']}\n")
                
                if video['publish_date']:
                    f.write(f"**Published**: {video['publish_date']}\n")
                
                f.write("\n---\n\n")
                
                # Write transcript
                if video['has_transcript']:
                    f.write("## Transcript\n\n")
                    f.write(f"*Type: {video['transcript']['transcript_type']}*\n\n")
                    f.write("### With Timestamps\n\n")
                    f.write(video['transcript']['with_timestamps'])
                    f.write("\n\n### Text Only\n\n")
                    f.write(video['transcript']['text_only'])
                else:
                    f.write("## ⚠️ No Transcript Available\n\n")
                    f.write("This video does not have a transcript available. ")
                    f.write("You may need to transcribe it manually or use a third-party service.\n")
        
        print(f"✅ Saved {len(self.videos_data)} lesson files")
    
    def save_master_document(self):
        """Save all content in a single master document"""
        master_file = os.path.join(self.output_dir, "master_curriculum.md")
        
        print(f"\n📄 Creating master curriculum document...")
        
        with open(master_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write("# VibeCoders Bootcamp - Complete Curriculum Content\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Table of Contents\n\n")
            
            # Write TOC
            for video in self.videos_data:
                f.write(f"- [Lesson {video['lesson_number']}: {video['title']}](#{self.sanitize_anchor(video['title'])})\n")
            
            f.write("\n---\n\n")
            
            # Write all lessons
            for video in self.videos_data:
                f.write(f"## Lesson {video['lesson_number']}: {video['title']}\n\n")
                f.write(f"**Duration**: {video['duration_formatted']} | ")
                f.write(f"**[Watch on YouTube]({video['url']})**\n\n")
                
                if video['has_transcript']:
                    f.write("### Content\n\n")
                    f.write(video['transcript']['text_only'])
                    f.write("\n\n")
                else:
                    f.write("### ⚠️ No Transcript Available\n\n")
                
                f.write("---\n\n")
        
        print(f"✅ Master document saved to: {master_file}")
    
    def save_json_data(self):
        """Save all data as JSON for programmatic access"""
        json_file = os.path.join(self.output_dir, "playlist_data.json")
        
        # Prepare data for JSON serialization
        json_data = {
            'playlist_info': {
                'url': self.playlist_url,
                'extraction_date': datetime.now().isoformat()
            },
            'videos': []
        }
        
        for video in self.videos_data:
            video_json = video.copy()
            # Remove raw transcript data to keep file size manageable
            if video_json.get('transcript') and video_json['transcript'].get('raw_data'):
                del video_json['transcript']['raw_data']
            json_data['videos'].append(video_json)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON data saved to: {json_file}")
    
    def save_summary_csv(self):
        """Save a summary CSV with video information"""
        csv_file = os.path.join(self.output_dir, "video_summary.csv")
        
        summary_data = []
        for video in self.videos_data:
            summary_data.append({
                'Lesson': video['lesson_number'],
                'Title': video['title'],
                'Duration': video['duration_formatted'],
                'Has Transcript': '✅' if video['has_transcript'] else '❌',
                'URL': video['url']
            })
        
        df = pd.DataFrame(summary_data)
        df.to_csv(csv_file, index=False)
        
        print(f"✅ Summary CSV saved to: {csv_file}")
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        # Limit length
        return filename[:50]
    
    def sanitize_anchor(self, text: str) -> str:
        """Create anchor link for markdown"""
        return re.sub(r'[^a-zA-Z0-9-]', '-', text.lower())
    
    def generate_report(self):
        """Generate extraction report"""
        report_file = os.path.join(self.output_dir, "extraction_report.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("YOUTUBE PLAYLIST EXTRACTION REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Playlist URL: {self.playlist_url}\n\n")
            
            f.write("SUMMARY\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Videos: {len(self.videos_data)}\n")
            f.write(f"Videos with Transcripts: {sum(1 for v in self.videos_data if v['has_transcript'])}\n")
            f.write(f"Failed Transcripts: {len(self.failed_videos)}\n\n")
            
            if self.failed_videos:
                f.write("FAILED VIDEOS\n")
                f.write("-" * 30 + "\n")
                for video in self.failed_videos:
                    f.write(f"- {video}\n")
                f.write("\n")
            
            f.write("VIDEO DETAILS\n")
            f.write("-" * 30 + "\n")
            total_duration = sum(v['duration_seconds'] for v in self.videos_data if v['duration_seconds'])
            f.write(f"Total Duration: {time.strftime('%H:%M:%S', time.gmtime(total_duration))}\n")
            f.write(f"Average Duration: {time.strftime('%H:%M:%S', time.gmtime(total_duration / len(self.videos_data)))}\n")
        
        print(f"✅ Report saved to: {report_file}")
    
    def run(self):
        """Run the complete extraction process"""
        print("\n" + "=" * 60)
        print("🚀 YOUTUBE PLAYLIST TRANSCRIPT EXTRACTOR")
        print("=" * 60)
        
        # Extract playlist info
        playlist_info = self.extract_playlist_info()
        if not playlist_info:
            print("❌ Failed to extract playlist information")
            return
        
        # Process videos
        self.process_videos()
        
        if not self.videos_data:
            print("❌ No videos were processed successfully")
            return
        
        # Save all outputs
        print(f"\n💾 Saving extracted content...")
        self.save_individual_lessons()
        self.save_master_document()
        self.save_json_data()
        self.save_summary_csv()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ EXTRACTION COMPLETE!")
        print(f"📁 All files saved to: {self.output_dir}/")
        print("=" * 60)
        
        # Print summary
        print("\n📊 SUMMARY:")
        print(f"  - Total Videos: {len(self.videos_data)}")
        print(f"  - With Transcripts: {sum(1 for v in self.videos_data if v['has_transcript'])}")
        print(f"  - Without Transcripts: {len(self.failed_videos)}")
        print("\n📂 Generated Files:")
        print(f"  - Individual lesson files in: {self.output_dir}/lessons/")
        print(f"  - Master curriculum document: {self.output_dir}/master_curriculum.md")
        print(f"  - JSON data: {self.output_dir}/playlist_data.json")
        print(f"  - Summary CSV: {self.output_dir}/video_summary.csv")
        print(f"  - Extraction report: {self.output_dir}/extraction_report.txt")


def main():
    """Main function to run the extractor"""
    
    # VibeCoders Bootcamp playlist URL
    PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLf2m23nhTg1P5BsOHUOXyQz5RhfUSSVUi"
    
    # You can change the output directory name here
    OUTPUT_DIR = "vibecoder_bootcamp_content"
    
    print("\n🎓 VibeCoders Bootcamp Content Extractor")
    print("-" * 40)
    
    # Allow user to input custom playlist URL if desired
    use_custom = input("\nUse default playlist URL? (y/n): ").strip().lower()
    
    if use_custom == 'n':
        custom_url = input("Enter YouTube playlist URL: ").strip()
        if custom_url:
            PLAYLIST_URL = custom_url
    
    print(f"\n📍 Using playlist: {PLAYLIST_URL}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    
    confirm = input("\nProceed with extraction? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Extraction cancelled")
        return
    
    # Create and run extractor
    extractor = PlaylistTranscriptExtractor(PLAYLIST_URL, OUTPUT_DIR)
    extractor.run()
    
    print("\n✨ Ready to organize your bootcamp content!")
    print("Next steps:")
    print("1. Review the extracted transcripts in the lessons folder")
    print("2. Map each video to the appropriate week in your curriculum")
    print("3. Create sandbox exercises based on the content")
    print("4. Prepare your tech stack based on the survey results")


if __name__ == "__main__":
    main()
