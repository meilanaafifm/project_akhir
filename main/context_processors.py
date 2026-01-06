"""
Context processor untuk main app
"""

from .models import SiteSettings


def site_settings(request):
    """Menyediakan pengaturan website di semua template"""
    try:
        settings = SiteSettings.get_settings()
    except:
        settings = None
    
    return {
        'site_settings': settings,
    }
