import requests
import hashlib
import os
from django.conf import settings
from django.contrib.sites.models import Site
import logging

logger = logging.getLogger(__name__)


def get_indexnow_key():
    """Get or generate IndexNow API key"""
    from .models import SEOSettings
    
    try:
        seo_settings = SEOSettings.objects.first()
        if seo_settings and seo_settings.indexnow_key:
            return seo_settings.indexnow_key
    except:
        pass
    
    key = getattr(settings, 'INDEXNOW_KEY', None)
    if not key:
        key = hashlib.md5(settings.SECRET_KEY.encode()).hexdigest()
    
    try:
        seo_settings, created = SEOSettings.objects.get_or_create(id=1)
        if not seo_settings.indexnow_key:
            seo_settings.indexnow_key = key
            seo_settings.save()
    except:
        pass
    
    return key


def submit_to_indexnow(urls):
    """
    Submit URLs to IndexNow for instant indexing
    Supported search engines: Bing, Yandex, Naver
    """
    from .models import IndexNowSubmission, SEOSettings
    from django.utils import timezone
    
    if not urls:
        return False
    
    if isinstance(urls, str):
        urls = [urls]
    
    key = get_indexnow_key()
    site = Site.objects.get_current()
    host = f"https://{site.domain}"
    
    if settings.DEBUG and 'REPLIT_DEV_DOMAIN' in os.environ:
        host = f"https://{os.environ['REPLIT_DEV_DOMAIN']}"
    
    full_urls = []
    for url in urls:
        if not url.startswith('http'):
            url = f"{host}{url}"
        full_urls.append(url)
    
    data = {
        "host": host.replace('https://', '').replace('http://', ''),
        "key": key,
        "keyLocation": f"{host}/{key}.txt",
        "urlList": full_urls
    }
    
    indexnow_endpoints = [
        'https://api.indexnow.org/indexnow',
        'https://www.bing.com/indexnow',
    ]
    
    success = False
    response_code = None
    error_message = ""
    
    for endpoint in indexnow_endpoints:
        try:
            response = requests.post(
                endpoint,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response_code = response.status_code
            if response.status_code in [200, 202]:
                logger.info(f"Successfully submitted {len(full_urls)} URLs to {endpoint}")
                success = True
                break
            else:
                error_message = f"Failed with status {response.status_code}"
                logger.warning(f"IndexNow submission to {endpoint} failed: {response.status_code}")
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error submitting to IndexNow ({endpoint}): {e}")
    
    for url in full_urls:
        try:
            IndexNowSubmission.objects.create(
                url=url,
                success=success,
                response_code=response_code,
                error_message=error_message
            )
        except:
            pass
    
    try:
        seo_settings = SEOSettings.objects.first()
        if seo_settings:
            seo_settings.last_indexnow_submission = timezone.now()
            seo_settings.save()
    except:
        pass
    
    return success


def ping_search_engines():
    """Ping search engines about sitemap updates"""
    site = Site.objects.get_current()
    host = f"https://{site.domain}"
    
    if settings.DEBUG and 'REPLIT_DEV_DOMAIN' in os.environ:
        host = f"https://{os.environ['REPLIT_DEV_DOMAIN']}"
    
    sitemap_url = f"{host}/sitemap.xml"
    
    ping_urls = [
        f"https://www.google.com/ping?sitemap={sitemap_url}",
        f"https://www.bing.com/ping?sitemap={sitemap_url}",
    ]
    
    for ping_url in ping_urls:
        try:
            response = requests.get(ping_url, timeout=10)
            if response.status_code == 200:
                logger.info(f"Successfully pinged {ping_url}")
        except Exception as e:
            logger.error(f"Error pinging {ping_url}: {e}")
