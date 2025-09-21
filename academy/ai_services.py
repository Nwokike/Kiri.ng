import os
import json
import requests
from googleapiclient.discovery import build

def fetch_youtube_video(search_query, used_ids):
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key: return None, None
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(q=search_query, part="snippet", type="video", maxResults=5)
        response = request.execute()
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            if video_id not in used_ids:
                return f"https://www.youtube.com/watch?v={video_id}", video_id
    except Exception as e:
        print(f"YouTube API Error: {e}")
    return None, None

def generate_module_content(module_title, previous_module_title=None):
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
        
        context_prompt = f"The student is learning about '{module_title}'."
        if previous_module_title:
            context_prompt = f"The student just finished a module on '{previous_module_title}' and is now starting a new module on '{module_title}'."

        # --- THIS IS THE NEW, SIMPLER PROMPT ---
        prompt = f"""
        You are an expert teacher creating a lesson for a Nigerian entrepreneur. {context_prompt}
        Your task is to write a complete, cohesive lesson that flows logically and uses markdown for formatting.
        End the entire lesson with a single, thought-provoking question based on the content.
        """
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        result_json = response.json()
        
        return result_json['candidates'][0]['content']['parts'][0]['text']
        
    except Exception as e:
        print(f"Error writing lesson content for '{module_title}': {e}")
        return "Content could not be generated for this step."

def generate_pathway_outline(goal, location):
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
        prompt = f"""
        You are an expert curriculum designer for Nigerian entrepreneurs in {location}, Nigeria. A user's goal is: "{goal}"
        Design a 5-module curriculum. For each module, provide a "title" and a single, concise "youtube_search_query". For each module, also create a list of 2-3 step objects, each with a "title" key.
        Return ONLY a valid JSON object.
        """
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generation_config": {"response_mime_type": "application/json"}}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result_json = response.json()
        json_response_text = result_json['candidates'][0]['content']['parts'][0]['text']
        pathway_data = json.loads(json_response_text)
        return pathway_data
    except Exception as e:
        print(f"An error occurred in generate_pathway_outline: {e}")
        return None