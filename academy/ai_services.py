import os
import json
import logging
import requests
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

def fetch_multiple_youtube_videos(search_query, num_videos=5, used_ids=None):
    """Fetch multiple YouTube videos for a module."""
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        return []
    
    if used_ids is None:
        used_ids = set()
    
    videos = []
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            q=search_query,
            part="snippet",
            type="video",
            maxResults=min(num_videos + 5, 10),
            relevanceLanguage='en',
            videoDefinition='high'
        )
        response = request.execute()
        
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            if video_id not in used_ids and len(videos) < num_videos:
                video_info = {
                    'video_id': video_id,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:200]
                }
                videos.append(video_info)
                used_ids.add(video_id)
    except Exception as e:
        logger.error(f"YouTube API Error: {e}")
    
    return videos


def fetch_youtube_video(search_query, used_ids):
    """Legacy function - fetch single video."""
    videos = fetch_multiple_youtube_videos(search_query, num_videos=1, used_ids=used_ids)
    if videos:
        return videos[0]['url'], videos[0]['video_id']
    return None, None


def generate_module_content(module_title, previous_module_title=None, video_titles=None):
    """Generate module content with references to YouTube videos."""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_api_key}"
        
        context_prompt = f"The student is learning about '{module_title}'."
        if previous_module_title:
            context_prompt = f"The student just finished a module on '{previous_module_title}' and is now starting a new module on '{module_title}'."
        
        video_context = ""
        if video_titles:
            video_list = "\n".join([f"- {title}" for title in video_titles])
            video_context = f"\n\nThe student has access to these video resources:\n{video_list}\n\nReference these videos naturally in your lesson where appropriate."

        prompt = f"""
        You are an expert teacher creating a comprehensive lesson for a Nigerian artisan/entrepreneur. {context_prompt}
        {video_context}
        
        Your task:
        1. Write a complete, practical lesson that helps them build their business
        2. Include real-world examples relevant to Nigeria
        3. Use markdown formatting for better readability
        4. Focus on actionable steps they can implement immediately
        5. End with 2-3 thought-provoking questions to deepen their understanding
        6. Keep the tone encouraging and motivational
        
        Make the lesson comprehensive (500-800 words) but easy to understand.
        """
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        result_json = response.json()
        
        return result_json['candidates'][0]['content']['parts'][0]['text']
        
    except Exception as e:
        logger.error(f"Error generating lesson content for '{module_title}': {e}")
        return "Content could not be generated. Please try refreshing the page."


def answer_module_question(question, module_title, module_content=None):
    """Generate AI answer to a student's question about a module."""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_api_key}"
        
        context = f"The student is studying '{module_title}'."
        if module_content:
            context += f"\n\nModule content:\n{module_content[:1000]}"
        
        prompt = f"""
        You are an expert instructor helping a Nigerian artisan/entrepreneur learn business skills.
        {context}
        
        The student asked: "{question}"
        
        Provide a clear, practical answer that:
        1. Directly addresses their question
        2. Uses simple language
        3. Includes Nigerian-specific examples where relevant
        4. Encourages them to apply what they learn
        5. Keeps the answer concise (150-300 words)
        
        Be supportive and motivating in your response.
        """
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result_json = response.json()
        
        return result_json['candidates'][0]['content']['parts'][0]['text']
        
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return "I'm sorry, I couldn't generate an answer. Please try again later."


def generate_pathway_outline(goal, location, category=None):
    """Generate a comprehensive 6-module pathway for artisan business development."""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_api_key}"
        
        goal_descriptions = {
            'start_small_business': 'starting a small business from scratch',
            'grow_existing_business': 'growing an existing business',
            'learn_marketing': 'learning marketing and customer acquisition',
            'improve_service_quality': 'improving service quality and skills',
            'manage_finances': 'managing business finances and pricing',
            'build_online_presence': 'building an online presence',
            'customer_service': 'improving customer service and retention',
            'scale_operations': 'scaling operations and hiring helpers',
        }
        
        goal_description = goal_descriptions.get(goal, goal)
        category_name = category if category else "general artisan business"
        
        prompt = f"""
        You are an expert curriculum designer for Nigerian artisan entrepreneurs.
        
        Student Profile:
        - Location: {location}, Nigeria
        - Trade/Skill: {category_name}
        - Business Goal: {goal_description}
        
        Design a comprehensive 6-module curriculum that will help them become a successful artisan entrepreneur.
        Each module should build on the previous one, starting from basics and progressing to advanced topics.
        
        For each module, provide:
        1. "title": Clear, actionable module title
        2. "youtube_search_query": Specific search term to find relevant tutorial videos (focus on practical skills)
        3. "steps": List of 3-4 specific learning objectives/steps
        
        Focus areas:
        - Module 1: Foundation & Mindset
        - Module 2: Core Skill Development
        - Module 3: Business Setup & Legalization
        - Module 4: Marketing & Customer Acquisition
        - Module 5: Financial Management & Pricing
        - Module 6: Growth & Scaling
        
        Return ONLY a valid JSON object with a "modules" array.
        Example structure:
        {{
            "modules": [
                {{
                    "title": "Building Your Artisan Mindset",
                    "youtube_search_query": "{category_name} business success Nigeria",
                    "steps": ["Understanding the market", "Setting clear goals", "Building confidence"]
                }}
            ]
        }}
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generation_config": {"response_mime_type": "application/json"}
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result_json = response.json()
        json_response_text = result_json['candidates'][0]['content']['parts'][0]['text']
        pathway_data = json.loads(json_response_text)
        return pathway_data
    except Exception as e:
        logger.error(f"Error generating pathway outline: {e}")
        return None


def validate_module_answer(answer, module_title, module_content):
    """Validate if the user's answer demonstrates actual understanding of the module."""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_api_key}"
        
        prompt = f"""
        You are an expert instructor evaluating a student's learning reflection.
        
        Module: "{module_title}"
        Module Content Summary: {module_content[:800] if module_content else "N/A"}
        
        Student's Answer: "{answer}"
        
        Evaluate if the student's answer demonstrates:
        1. Actual understanding of the module concepts (not just generic statements)
        2. Specific learning takeaways or insights from the module
        3. Genuine engagement with the material (not random text or gibberish)
        
        Return ONLY a JSON object with:
        {{
            "is_valid": true/false,
            "reason": "Brief explanation"
        }}
        
        Be fair but ensure the answer shows real understanding. Generic answers like "I learned a lot" or nonsense text should be marked invalid.
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generation_config": {"response_mime_type": "application/json"}
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result_json = response.json()
        
        validation_text = result_json['candidates'][0]['content']['parts'][0]['text']
        validation_data = json.loads(validation_text)
        
        return validation_data.get('is_valid', False), validation_data.get('reason', '')
        
    except Exception as e:
        logger.error(f"Error validating answer: {e}")
        # If validation fails, allow the answer (fail open)
        return True, "Validation service unavailable"