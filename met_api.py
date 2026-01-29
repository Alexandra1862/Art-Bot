

import requests
import random

class MetMuseumAPI:
    def __init__(self):
        self.base_url = "https://collectionapi.metmuseum.org/public/collection/v1"
    
    def search_artworks(self, query, max_results=5):
        """Search artworks by query"""
        try:
            # Search for object IDs
            search_url = f"{self.base_url}/search"
            params = {'q': query, 'hasImages': 'true'}
            
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            object_ids = data.get('objectIDs', [])
            
            if not object_ids:
                return []
            
            # Get details for first N objects
            artworks = []
            for obj_id in object_ids[:max_results]:
                artwork_data = self._get_object_details(obj_id)
                if artwork_data:
                    artworks.append(artwork_data)
            
            return artworks
            
        except Exception as e:
            print(f"API Error: {e}")
            return []
    
    def search_by_artist(self, artist_name, max_results=5):
        """Search by artist name"""
        return self.search_artworks(artist_name, max_results)
    
    def get_random_artwork(self):
        """Get random artwork"""
        try:
            # Get random object from a large department
            search_url = f"{self.base_url}/search"
            params = {'q': 'art', 'hasImages': 'true'}
            
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            object_ids = data.get('objectIDs', [])
            
            if not object_ids:
                return None
            
            # Pick random ID
            random_id = random.choice(object_ids[:1000])  # From first 1000
            return self._get_object_details(random_id)
            
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    def _get_object_details(self, object_id):
        """Get details for specific object"""
        try:
            object_url = f"{self.base_url}/objects/{object_id}"
            response = requests.get(object_url)
            response.raise_for_status()
            obj = response.json()
            
            # Only return if has image
            if not obj.get('primaryImage'):
                return None
            
            return {
                'title': obj.get('title', 'Untitled'),
                'artist': obj.get('artistDisplayName', 'Unknown Artist'),
                'image_url': obj.get('primaryImage'),
                'date': obj.get('objectDate', 'Unknown'),
                'culture': obj.get('culture', ''),
            }
            
        except Exception as e:
            print(f"Error getting object {object_id}: {e}")
            return None