#!/usr/bin/env python3
"""
أدوات مساعدة للتشغيل على Replit
"""

import re
import json
from typing import Any, Dict

class ReplitHelpers:
    @staticmethod
    def validate_email(email: str) -> bool:
        """التحقق من صحة الإيميل"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """التحقق من صحة الهاتف"""
        cleaned = re.sub(r'\D', '', phone)
        return len(cleaned) >= 10
    
    @staticmethod
    def save_results(results: Dict[str, Any], filename: str = "results.json"):
        """حفظ النتائج في ملف"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"فشل حفظ النتائج: {e}")
            return False
