import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _


@csrf_exempt
@login_required
def custom_upload_file(request):
    """
    Custom CKEditor 5 image upload handler with CSRF exemption.
    This fixes the "cannot upload image" error in CKEditor.
    """
    if request.method == "POST" and request.FILES.get("upload"):
        uploaded_file = request.FILES["upload"]
        
        # Validate file size (2MB limit)
        if uploaded_file.size > 2 * 1024 * 1024:
            return JsonResponse({
                "error": {"message": _("File too large. Maximum size is 2MB.")}
            }, status=400)
        
        # Define upload path for blog images
        upload_path = os.path.join("blog_uploads", uploaded_file.name)
        
        # Save file using Django's storage (Cloudinary in production)
        file_path = default_storage.save(upload_path, uploaded_file)
        file_url = default_storage.url(file_path)
        
        # Return response in format CKEditor 5 expects
        return JsonResponse({"url": file_url})
    
    return JsonResponse({
        "error": {"message": _("Invalid request or no file uploaded.")}
    }, status=400)
