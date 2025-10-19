#!/usr/bin/env python3
"""
أدوات مساعدة مخصصة لـ Replit
"""

import os
import sys
import asyncio
import aiohttp
import logging
from pathlib import Path

class ReplitEnvironment:
    """مدير بيئة Replit"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_dir = Path(__file__).parent.parent
        self.setup_environment()
    
    def setup_environment(self):
        """إعداد بيئة Replit"""
        # إعداد مسارات Replit
        self.ensure_directories()
        self.setup_logging()
        self.check_resources()
    
    def ensure_directories(self):
        """التأكد من وجود الدلائل الضرورية"""
        directories = [
            'cache',
            'data',
            'logs', 
            'reports',
            'exports'
        ]
        
        for dir_name in directories:
            dir_path = self.base_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            self.logger.info(f"📁 إنشاء مجلد: {dir_name}")
    
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        log_dir = self.base_dir / 'logs'
        log_file = log_dir / 'quantum_osint.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def check_resources(self):
        """فحص موارد Replit المتاحة"""
        import psutil
        
        # معلومات الذاكرة
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        resource_info = {
            'memory_total_gb': round(memory.total / (1024**3), 2),
            'memory_available_gb': round(memory.available / (1024**3), 2),
            'disk_free_gb': round(disk.free / (1024**3), 2),
            'cpu_cores': psutil.cpu_count()
        }
        
        self.logger.info(f"💾 موارد النظام: {resource_info}")
        return resource_info
    
    async def check_internet(self):
        """فحص اتصال الإنترنت"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.github.com', timeout=10) as response:
                    return response.status == 200
        except:
            return False

class ReplitSecurity:
    """إجراءات أمان مخصصة لـ Replit"""
    
    @staticmethod
    def safe_path(path):
        """تأمين المسارات لمنع الهجمات"""
        base_dir = Path(__file__).parent.parent
        target_path = (base_dir / path).resolve()
        
        # التأكد أن المسار ضمن المجلد الأساسي
        if base_dir in target_path.parents:
            return target_path
        else:
            raise SecurityError("مسار غير آمن")
    
    @staticmethod
    def validate_target(target):
        """التحقق من صحة الهدف"""
        import re
        
        # قائمة الأنماط المسموحة
        allowed_patterns = [
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',  # إيميل
            r'^@?[a-zA-Z0-9_]{1,15}$',  # اسم مستخدم
            r'^\+?[1-9]\d{1,14}$',  # رقم هاتف
            r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'  # نطاق
        ]
        
        for pattern in allowed_patterns:
            if re.match(pattern, target):
                return True
        
        return False

class SecurityError(Exception):
    """خطأ أمان مخصص"""
    pass
