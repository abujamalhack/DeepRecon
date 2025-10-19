here#!/usr/bin/env python3
"""
إعدادات النظام المعدلة لـ Replit
"""

import os
from typing import Dict, Any

class ReplitSettings:
    """إعدادات مخصصة لبيئة Replit"""
    
    # إعدادات Replit المحددة
    IS_REPLIT = True
    REPLIT_HOME = "/home/runner/" + os.getenv('REPL_SLUG', 'QuantumOSINT')
    
    # إعدادات النظام
    APP_NAME = "QuantumOSINT - Replit Edition"
    VERSION = "1.0.0-replit"
    
    # إعدادات الأداء لـ Replit
    MAX_CONCURRENT_REQUESTS = 10  # أقل بسبب قيود Replit
    REQUEST_TIMEOUT = 20
    MAX_RETRY_ATTEMPTS = 3
    
    # إعدادات التخزين
    DATABASE_URL = "sqlite:///./quantum_osint.db"
    CACHE_DIR = "./cache"
    
    # إعدادات المنصات المدعومة
    PLATFORMS = {
        'facebook': {'enabled': True, 'method': 'public_api'},
        'instagram': {'enabled': True, 'method': 'public_scraping'},
        'twitter': {'enabled': True, 'method': 'public_api'},
        'github': {'enabled': True, 'method': 'official_api'}
    }
    
    # إعدادات الأمان
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'replit-quantum-secure-key-2024')
    ENABLE_ENCRYPTION = True
    
    @classmethod
    def get_replit_info(cls):
        """الحصول على معلومات Replit"""
        return {
            'repl_slug': os.getenv('REPL_SLUG'),
            'repl_owner': os.getenv('REPL_OWNER'),
            'repl_id': os.getenv('REPL_ID')
        }

# كائن الإعدادات العام
settings = ReplitSettings()
