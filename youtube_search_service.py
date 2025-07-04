import asyncio
import logging
from youtubesearchpython import VideosSearch
import re


class YouTubeSearchService:
    """
    YouTube search service for getting clean titles to search on JioSaavn
    Uses youtube-search-python for fast, reliable YouTube searches
    """
    
    def __init__(self):
        logging.info("YouTube Search Service initialized")
    
    async def search_and_get_title(self, query, limit=1):
        """
        Search YouTube and get clean title for JioSaavn search
        
        Args:
            query (str): Search query (can be lyrics, song name, etc.)
            limit (int): Number of results to fetch
            
        Returns:
            dict: YouTube video details with clean title
        """
        try:
            # Search YouTube
            videos_search = VideosSearch(query, limit=limit)
            results = videos_search.result()
            
            if results and results.get('result'):
                video = results['result'][0]  # Get first result
                
                # Extract clean title for JioSaavn search
                clean_title = self._clean_title_for_music_search(video.get('title', ''))
                
                return {
                    'youtube_title': video.get('title', ''),
                    'clean_title': clean_title,
                    'duration': video.get('duration', ''),
                    'thumbnail': video.get('thumbnails', [{}])[0].get('url', ''),
                    'video_id': video.get('id', ''),
                    'youtube_url': video.get('link', ''),
                    'channel': video.get('channel', {}).get('name', ''),
                    'views': video.get('viewCount', {}).get('text', '')
                }
                
        except Exception as e:
            logging.error(f"YouTube search error: {str(e)}")
        
        return None
    
    async def get_multiple_titles(self, query, limit=5):
        """
        Get multiple YouTube results for better matching
        
        Args:
            query (str): Search query
            limit (int): Number of results
            
        Returns:
            list: List of clean titles for JioSaavn search
        """
        try:
            videos_search = VideosSearch(query, limit=limit)
            results = videos_search.result()
            
            titles = []
            if results and results.get('result'):
                for video in results['result']:
                    clean_title = self._clean_title_for_music_search(video.get('title', ''))
                    if clean_title and clean_title not in titles:
                        titles.append(clean_title)
            
            return titles
            
        except Exception as e:
            logging.error(f"YouTube multiple search error: {str(e)}")
        
        return []
    
    def _clean_title_for_music_search(self, title):
        """
        Clean YouTube title to make it suitable for JioSaavn search
        
        Args:
            title (str): Raw YouTube title
            
        Returns:
            str: Cleaned title
        """
        if not title:
            return ""
        
        # Remove common YouTube-specific patterns
        patterns_to_remove = [
            r'\(Official.*?\)',  # (Official Video), (Official Audio), etc.
            r'\[Official.*?\]',  # [Official Video], [Official Audio], etc.
            r'\(Music Video\)',  # (Music Video)
            r'\[Music Video\]',  # [Music Video]
            r'\(Audio\)',        # (Audio)
            r'\[Audio\]',        # [Audio]
            r'\(HD\)',           # (HD)
            r'\[HD\]',           # [HD]
            r'\(4K\)',           # (4K)
            r'\[4K\]',           # [4K]
            r'\(Lyrics\)',       # (Lyrics)
            r'\[Lyrics\]',       # [Lyrics]
            r'\(Full Song\)',    # (Full Song)
            r'\[Full Song\]',    # [Full Song]
            r'\(Full Video\)',   # (Full Video)
            r'\[Full Video\]',   # [Full Video]
            r'\|.*',             # Everything after |
            r'-.*Record.*',      # Record label mentions
            r'-.*Music.*',       # Music company mentions
            r'ft\..*',           # "ft." and everything after
            r'feat\..*',         # "feat." and everything after
            r'featuring.*',      # "featuring" and everything after
        ]
        
        cleaned_title = title
        
        # Apply cleaning patterns
        for pattern in patterns_to_remove:
            cleaned_title = re.sub(pattern, '', cleaned_title, flags=re.IGNORECASE)
        
        # Remove extra spaces and clean up
        cleaned_title = re.sub(r'\s+', ' ', cleaned_title).strip()
        
        # Remove leading/trailing dashes or other punctuation
        cleaned_title = cleaned_title.strip(' -–—|')
        
        logging.info(f"Cleaned title: '{title}' -> '{cleaned_title}'")
        return cleaned_title
    
    async def details(self, query):
        """
        Get detailed info about a YouTube video
        """
        return await self.search_and_get_title(query, limit=1)
    
    async def title(self, query):
        """
        Get just the clean title
        """
        result = await self.search_and_get_title(query, limit=1)
        return result.get('clean_title', '') if result else ''
    
    async def duration(self, query):
        """
        Get just the duration
        """
        result = await self.search_and_get_title(query, limit=1)
        return result.get('duration', '') if result else ''
    
    async def thumbnail(self, query):
        """
        Get just the thumbnail URL
        """
        result = await self.search_and_get_title(query, limit=1)
        return result.get('thumbnail', '') if result else ''
    
    async def track(self, query):
        """
        Get complete track details
        """
        result = await self.search_and_get_title(query, limit=1)
        if result:
            return {
                "title": result.get('clean_title', ''),
                "youtube_title": result.get('youtube_title', ''),
                "link": result.get('youtube_url', ''),
                "vidid": result.get('video_id', ''),
                "duration_min": result.get('duration', ''),
                "thumb": result.get('thumbnail', ''),
                "channel": result.get('channel', ''),
                "views": result.get('views', '')
            }
        return None
    
    async def slider(self, query, query_type=0):
        """
        Get multiple results and return specific index
        
        Args:
            query (str): Search query
            query_type (int): Index of result to return (0-9)
            
        Returns:
            dict: Track details for specific index
        """
        try:
            videos_search = VideosSearch(query, limit=10)
            results = videos_search.result()
            
            if results and results.get('result') and len(results['result']) > query_type:
                video = results['result'][query_type]
                clean_title = self._clean_title_for_music_search(video.get('title', ''))
                
                return {
                    "title": clean_title,
                    "youtube_title": video.get('title', ''),
                    "link": video.get('link', ''),
                    "vidid": video.get('id', ''),
                    "duration_min": video.get('duration', ''),
                    "thumb": video.get('thumbnails', [{}])[0].get('url', ''),
                    "channel": video.get('channel', {}).get('name', ''),
                    "views": video.get('viewCount', {}).get('text', '')
                }
                
        except Exception as e:
            logging.error(f"YouTube slider search error: {str(e)}")
        
        return None