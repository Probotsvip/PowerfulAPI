import aiohttp
import asyncio
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class JioSaavnService:
    """JioSaavn service for music search and 320kbps streaming"""
    
    def __init__(self):
        self.base_url = "https://saavn.dev/api"
        self.search_url = "https://saavn.dev/api/search/songs"
        self.song_details_url = "https://saavn.dev/api/songs"
        
    async def search_songs(self, query: str) -> List[Dict]:
        """Search for songs on JioSaavn using proxy API"""
        try:
            params = {
                'query': query,
                'page': 1,
                'limit': 5
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.search_url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Extract songs from response
                        songs = []
                        results = data.get('data', {}).get('results', [])
                        
                        for song in results:
                            songs.append({
                                'id': song.get('id', ''),
                                'title': song.get('name', ''),
                                'subtitle': song.get('artists', {}).get('primary', [{}])[0].get('name', '') if song.get('artists', {}).get('primary') else '',
                                'image': song.get('image', [{}])[-1].get('url', '') if song.get('image') else '',
                                'download_url': song.get('downloadUrl', [{}])[-1].get('url', '') if song.get('downloadUrl') else ''
                            })
                        
                        logger.debug(f"Found {len(songs)} songs on JioSaavn for: {query}")
                        return songs
                    else:
                        logger.warning(f"JioSaavn search failed with status: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"JioSaavn search error: {str(e)}")
            return []
    
    async def get_song_details(self, song_id: str) -> Optional[Dict]:
        """Get detailed song information with download URLs"""
        try:
            url = f"{self.song_details_url}/{song_id}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'data' in data and len(data['data']) > 0:
                            song_data = data['data'][0]
                            
                            # Get highest quality download URL
                            download_urls = song_data.get('downloadUrl', [])
                            stream_url = ''
                            
                            # Look for 320kbps first
                            for url_obj in download_urls:
                                if url_obj.get('quality') == '320kbps':
                                    stream_url = url_obj.get('url', '')
                                    break
                            
                            # Fallback to highest quality
                            if not stream_url and download_urls:
                                stream_url = download_urls[-1].get('url', '')
                            
                            return {
                                'stream_url': stream_url,
                                'title': song_data.get('name', ''),
                                'album': song_data.get('album', {}).get('name', '') if song_data.get('album') else '',
                                'artists': song_data.get('artists', {}).get('primary', [{}])[0].get('name', '') if song_data.get('artists', {}).get('primary') else '',
                                'duration': song_data.get('duration', ''),
                                'image': song_data.get('image', [{}])[-1].get('url', '') if song_data.get('image') else ''
                            }
                            
        except Exception as e:
            logger.error(f"Error getting JioSaavn song details for {song_id}: {str(e)}")
            return None
    
    async def search_and_get_stream(self, query: str, max_attempts: int = 3) -> Optional[Dict]:
        """Search for a song and get its streaming URL"""
        for attempt in range(max_attempts):
            try:
                logger.debug(f"JioSaavn attempt {attempt + 1}/{max_attempts} for: {query}")
                
                # Search for songs
                songs = await self.search_songs(query)
                
                if not songs:
                    logger.debug(f"No songs found on attempt {attempt + 1}")
                    continue
                
                # Try to get stream URL for the first few results
                for song in songs[:3]:  # Try first 3 results
                    # Check if we already have download_url from search
                    if song.get('download_url'):
                        return {
                            'stream_url': song['download_url'],
                            'title': song['title'],
                            'artists': song['subtitle'],
                            'image': song['image']
                        }
                    
                    # Fallback to detailed API call
                    song_details = await self.get_song_details(song['id'])
                    
                    if song_details and song_details.get('stream_url'):
                        logger.info(f"JioSaavn stream found via details API on attempt {attempt + 1}")
                        return song_details
                
                # Wait before retry
                if attempt < max_attempts - 1:
                    await asyncio.sleep(2)
                    
            except Exception as e:
                logger.error(f"JioSaavn attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(2)
        
        logger.warning(f"All JioSaavn attempts failed for: {query}")
        return None