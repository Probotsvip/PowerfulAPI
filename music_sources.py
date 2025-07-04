import requests
import json
import logging
import time
from urllib.parse import quote
import re

class MusicSources:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_music(self, query, source="auto"):
        """Search for music from multiple sources"""
        start_time = time.time()
        
        try:
            # Try JioSaavn first (fastest and most reliable)
            if source in ["auto", "jiosaavn"]:
                result = self._search_jiosaavn(query)
                if result:
                    result['response_time'] = time.time() - start_time
                    return result
            
            # Try Spotify scraping
            if source in ["auto", "spotify"]:
                result = self._search_spotify_alternative(query)
                if result:
                    result['response_time'] = time.time() - start_time
                    return result
            
            # Try YouTube alternative
            if source in ["auto", "youtube"]:
                result = self._search_youtube_alternative(query)
                if result:
                    result['response_time'] = time.time() - start_time
                    return result
                    
        except Exception as e:
            logging.error(f"Error searching music: {str(e)}")
        
        return None
    
    def _search_jiosaavn(self, query):
        """Search JioSaavn using unofficial API"""
        try:
            # JioSaavn unofficial API endpoint
            search_url = f"https://www.jiosaavn.com/api.php?__call=autocomplete.get&_format=json&_marker=0&cc=in&includeMetaTags=1&query={quote(query)}"
            
            response = self.session.get(search_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('songs') and data['songs'].get('data'):
                    song = data['songs']['data'][0]
                    
                    # Get direct download link
                    song_id = song.get('id')
                    if song_id:
                        download_url = self._get_jiosaavn_download_url(song_id)
                        if download_url:
                            return {
                                'title': song.get('title', query),
                                'artist': song.get('more_info', {}).get('artistMap', {}).get('primary_artists', [{}])[0].get('name', 'Unknown'),
                                'duration': song.get('more_info', {}).get('duration', '0'),
                                'stream_url': download_url,
                                'source': 'jiosaavn',
                                'quality': '320kbps'
                            }
        except Exception as e:
            logging.error(f"JioSaavn search error: {str(e)}")
        
        return None
    
    def _get_jiosaavn_download_url(self, song_id):
        """Get direct download URL from JioSaavn"""
        try:
            download_url = f"https://www.jiosaavn.com/api.php?__call=song.generateAuthToken&url=false&bitrate=320&api_version=4&_format=json&ctx=web6dot0&_marker=0&cc=in&id={song_id}"
            
            response = self.session.get(download_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get('auth_url')
                if auth_url:
                    # Clean up the URL
                    return auth_url.replace('_96.mp4', '_320.mp4')
        except Exception as e:
            logging.error(f"JioSaavn download URL error: {str(e)}")
        
        return None
    
    def _search_spotify_alternative(self, query):
        """Search Spotify using web scraping (no official API)"""
        try:
            # Use a Spotify web player alternative or scraping method
            # This is a simplified example - implement actual scraping logic
            search_url = f"https://open.spotify.com/search/{quote(query)}"
            
            # For demo purposes, we'll return a mock response
            # In production, implement actual Spotify web scraping
            return {
                'title': f"Spotify: {query}",
                'artist': 'Various Artists',
                'duration': '180',
                'stream_url': f"https://example.com/spotify_stream/{quote(query)}.mp3",
                'source': 'spotify',
                'quality': '320kbps'
            }
        except Exception as e:
            logging.error(f"Spotify search error: {str(e)}")
        
        return None
    
    def _search_youtube_alternative(self, query):
        """Search YouTube using alternative methods (no yt-dlp)"""
        try:
            # Use YouTube's internal API or alternative scraping
            # This is a simplified example - implement actual YouTube scraping
            search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
            
            # For demo purposes, we'll return a mock response
            # In production, implement actual YouTube scraping without yt-dlp
            return {
                'title': f"YouTube: {query}",
                'artist': 'YouTube',
                'duration': '200',
                'stream_url': f"https://example.com/youtube_stream/{quote(query)}.mp3",
                'source': 'youtube',
                'quality': '256kbps'
            }
        except Exception as e:
            logging.error(f"YouTube search error: {str(e)}")
        
        return None
    
    def get_trending_music(self, source="jiosaavn", limit=10):
        """Get trending music from sources"""
        try:
            if source == "jiosaavn":
                # JioSaavn trending API
                trending_url = "https://www.jiosaavn.com/api.php?__call=content.getTrending&api_version=4&_format=json&ctx=web6dot0&_marker=0&cc=in"
                
                response = self.session.get(trending_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    songs = []
                    
                    for item in data.get('list', [])[:limit]:
                        if item.get('type') == 'song':
                            songs.append({
                                'title': item.get('title', ''),
                                'artist': item.get('more_info', {}).get('artistMap', {}).get('primary_artists', [{}])[0].get('name', 'Unknown'),
                                'image': item.get('image', ''),
                                'id': item.get('id', '')
                            })
                    
                    return songs
        except Exception as e:
            logging.error(f"Trending music error: {str(e)}")
        
        return []
