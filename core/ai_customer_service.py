import google.generativeai as genai
from django.conf import settings
from django.contrib.auth.models import User
from marketplace.models import Service, Booking, Category
from academy.models import LearningPathway
from users.models import Profile
from django.utils import timezone
from datetime import timedelta

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)

class AICustomerService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def get_system_context(self, user=None):
        """Get context about the platform and user for better AI responses"""
        context = """
        You are Kiri AI, an intelligent customer service assistant for Kiri.ng - a Nigerian artisan marketplace and learning platform.
        
        Platform Features:
        - Marketplace: Artisans can list services, customers can book them
        - Academy: AI-powered learning pathways for skill development
        - Blog: Community blogging for knowledge sharing
        - Referral System: Users can refer others to grow the community
        
        You can help users with:
        1. Finding and booking artisan services
        2. Creating learning pathways for skill development
        3. Managing their profile and account
        4. Understanding how to use platform features
        5. Troubleshooting common issues
        6. Navigating the referral system
        
        Always be helpful, professional, and provide specific actionable guidance.
        When suggesting actions, provide clear step-by-step instructions.
        """
        
        if user and user.is_authenticated:
            context += f"\n\nCurrent User: {user.username}"
            context += f"\nUser Type: {'Artisan' if hasattr(user, 'profile') and user.profile.is_verified_artisan else 'Customer'}"
            
            # Add user-specific stats
            if hasattr(user, 'profile'):
                context += f"\nReferrals: {user.profile.successful_referrals_count}"
                
        return context
    
    def get_chat_response(self, user_message, user=None, conversation_history=None):
        """Get AI response to user query"""
        try:
            # Build conversation with context
            system_context = self.get_system_context(user)
            
            # Prepare messages
            messages = [system_context]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append(f"User: {user_message}")
            
            # Generate response
            response = self.model.generate_content(
                "\n".join(messages),
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1000,
                }
            )
            
            return response.text
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Please try again or contact support at nwokikeonyeka@gmail.com. Error: {str(e)}"
    
    def help_with_task(self, task_type, user=None):
        """Provide specific help for common tasks"""
        task_guides = {
            "find_service": """
            To find an artisan service:
            1. Go to the Services tab at the bottom
            2. Browse by category or use the search
            3. Click on a service to see details
            4. Click "Book This Service" to make a booking request
            5. The artisan will contact you via your provided email/phone
            """,
            
            "create_pathway": """
            To create a learning pathway:
            1. Go to Academy > My Dashboard
            2. Click "Create New Pathway" (or "Get Started Now" if first time)
            3. Enter your business goal or skill you want to learn
            4. Our AI will generate a personalized learning pathway
            5. Complete modules to track your progress
            6. Earn a certificate when you finish!
            """,
            
            "list_service": """
            To list your service as an artisan:
            1. Make sure you're verified (complete your profile with location)
            2. Go to Services > My Services (if verified artisan)
            3. Click "Add New Service"
            4. Fill in service details, price, and upload images
            5. Submit and your service will be live!
            """,
            
            "refer_friend": """
            To refer friends and earn benefits:
            1. Go to Academy > My Dashboard
            2. Click "Generate Referral URL"
            3. Copy your unique referral link
            4. Share it with friends
            5. When they sign up, you both benefit!
            6. Get 1 referral to unlock creating additional learning pathways
            """,
            
            "edit_profile": """
            To edit your profile:
            1. Click your profile picture (top right)
            2. Select "Edit Profile"
            3. Update your information, bio, social media links
            4. Upload a profile picture
            5. Add certificates to showcase your skills
            6. Save changes
            """
        }
        
        return task_guides.get(task_type, "Please specify what you need help with and I'll guide you through it.")
    
    def get_platform_stats(self):
        """Get platform statistics for informational responses"""
        try:
            stats = {
                "total_services": Service.objects.count(),
                "total_artisans": Profile.objects.filter(is_verified_artisan=True).count(),
                "total_pathways": LearningPathway.objects.count(),
                "total_users": User.objects.count(),
                "categories": Category.objects.count(),
            }
            return stats
        except:
            return {}
    
    def admin_query(self, query, user):
        """Handle admin-specific queries with elevated permissions"""
        if not user or not user.is_staff:
            return "This feature requires admin privileges."
        
        try:
            context = f"""
            You are assisting an admin user of Kiri.ng platform.
            
            Admin Query: {query}
            
            Available admin capabilities:
            - View all users, services, bookings
            - Manage content moderation
            - View platform analytics
            - Assist with user support issues
            - System configuration guidance
            
            Provide detailed admin-level assistance.
            """
            
            stats = self.get_platform_stats()
            context += f"\n\nCurrent Platform Stats: {stats}"
            
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return f"Error processing admin query: {str(e)}"
