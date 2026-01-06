"""
Context processor untuk main app
Menyediakan data yang dapat diakses di semua template
"""

from .models import SiteSettings


def site_settings(request):
    """
    Menyediakan pengaturan website di semua template
    """
    try:
        settings = SiteSettings.get_settings()
    except:
        settings = None
    
    return {
        'site_settings': settings,
    }
