import google.generativeai as genai
from django.conf import settings
from django.contrib.auth.models import User
from marketplace.models import Service, Booking, Category
from academy.models import LearningPathway
from users.models import Profile
from django.utils import timezone
from datetime import timedelta
import json

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)

class AICustomerService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def get_system_context(self, user=None):
        """Get context about the platform and user for better AI responses"""
        context = """
        You are Kiri AI, an intelligent customer service assistant for Kiri.ng - Nigeria's leading artisan marketplace and learning platform.
        
        Platform Overview:
        Kiri.ng connects skilled artisans with customers across Nigeria, providing:
        - A marketplace for booking artisan services (plumbing, electrical, carpentry, etc.)
        - AI-powered learning academy for skill development
        - Community blog for knowledge sharing
        - Referral rewards system
        - PWA (Progressive Web App) for seamless mobile experience
        
        What I Can Help You With:
        1. 🔍 Finding and booking artisan services
        2. 📚 Creating personalized learning pathways
        3. 👤 Managing your profile and verification
        4. 🎨 Listing your services as an artisan
        5. 🔄 Using the referral system
        6. 📝 Writing blog posts (verified artisans only)
        7. ✉️ Creating support tickets for complex issues
        
        How to Get Verified as an Artisan:
        - Complete your profile with accurate location (street address and city)
        - Location verification is automatic once you provide valid address
        - Verified artisans can list services and write blog posts
        
        For issues I cannot resolve directly, I can create a support ticket for our team.
        
        Always be helpful, professional, and provide clear step-by-step guidance.
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
    
    def create_support_ticket(self, user, email, category, subject, description):
        """Create a support ticket for issues AI cannot handle and send email notifications"""
        try:
            from .models import SupportTicket
            from django.core.mail import send_mail
            from notifications.models import Notification
            
            ticket = SupportTicket.objects.create(
                user=user if user and user.is_authenticated else None,
                email=email,
                category=category,
                subject=subject,
                description=description
            )
            
            try:
                send_mail(
                    subject=f'Support Ticket #{ticket.pk} Created - {subject}',
                    message=f'''Hello,

Your support ticket has been created successfully.

Ticket ID: #{ticket.pk}
Subject: {subject}
Category: {ticket.get_category_display()}
Status: {ticket.get_status_display()}

Description:
{description}

Our team will review your request and contact you at {email} within 24-48 hours.

Thank you for contacting Kiri.ng support!

Best regards,
The Kiri.ng Team''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                
                send_mail(
                    subject=f'New Support Ticket #{ticket.pk} - Action Required',
                    message=f'''New support ticket created:

Ticket ID: #{ticket.pk}
User: {user.username if user and user.is_authenticated else "Anonymous"}
Email: {email}
Category: {ticket.get_category_display()}
Subject: {subject}

Description:
{description}

Please review and respond within 24-48 hours.''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                
                if user and user.is_authenticated:
                    Notification.objects.create(
                        recipient=user,
                        message=f'Your support ticket #{ticket.pk} has been created. We will contact you at {email} within 24-48 hours.',
                        link=None
                    )
            except Exception as email_error:
                pass
            
            return {
                'success': True,
                'ticket_id': ticket.pk,
                'message': f'Support ticket #{ticket.pk} has been created successfully. A confirmation email has been sent to {email}. Our team will contact you within 24-48 hours.'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to create support ticket: {str(e)}'
            }
    
    def get_user_services(self, user):
        """Get user's services (for artisans)"""
        if not user or not user.is_authenticated:
            return []
        
        try:
            services = Service.objects.filter(artisan=user)
            return [{'id': s.id, 'title': s.title, 'price': str(s.price), 'category': s.get_category_display()} for s in services]
        except:
            return []
    
    def get_user_bookings(self, user):
        """Get user's bookings"""
        if not user or not user.is_authenticated:
            return []
        
        try:
            bookings = Booking.objects.filter(user=user)[:5]
            return [{'id': b.id, 'service': b.service.title, 'status': b.status, 'date': b.created_at.strftime('%Y-%m-%d')} for b in bookings]
        except:
            return []
    
    def get_user_learning_pathways(self, user):
        """Get user's learning pathways"""
        if not user or not user.is_authenticated:
            return []
        
        try:
            pathways = LearningPathway.objects.filter(user=user)
            return [{'id': p.id, 'title': p.title, 'progress': p.completion_percentage, 'completed': p.is_completed} for p in pathways]
        except:
            return []
    
    def get_available_categories(self):
        """Get all service categories"""
        try:
            categories = Category.objects.all()
            return [{'id': c.id, 'name': c.name} for c in categories]
        except:
            return []
    
    def search_services(self, query='', category=None, limit=5):
        """Search for services"""
        try:
            services = Service.objects.filter(is_active=True)
            if query:
                services = services.filter(title__icontains=query)
            if category:
                services = services.filter(category_id=category)
            services = services[:limit]
            return [{'id': s.id, 'title': s.title, 'artisan': s.artisan.username, 'price': str(s.price)} for s in services]
        except:
            return []
