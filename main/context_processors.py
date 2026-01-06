"""
Context processor untuk main app
Menyediakan data yang dapat diakses di semua template
"""

import os

IS_VERCEL = os.environ.get('VERCEL', False)


def site_settings(request):
    """
    Menyediakan pengaturan website di semua template
    """
    settings = None
    if not IS_VERCEL:
        try:
            from .models import SiteSettings
            settings = SiteSettings.get_settings()
        except Exception:
            pass
    
    return {
        'site_settings': settings,
    }
