#!/usr/bin/env python3
"""
أدوات مساعدة إضافية
"""

import json
import csv
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class DataSaver:
    """حفظ البيانات بأنواع مختلفة"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_dir = Path(__file__).parent.parent
    
    async def save_json(self, data: Dict, filename: str) -> str:
        """حفظ البيانات كـ JSON"""
        try:
            exports_dir = self.base_dir / 'exports'
            exports_dir.mkdir(exist_ok=True)
            
            file_path = exports_dir / f"{filename}_{int(datetime.now().timestamp())}.json"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 تم حفظ JSON: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"❌ فشل حفظ JSON: {e}")
            return ""
    
    async def save_csv(self, data: List[Dict], filename: str) -> str:
        """حفظ البيانات كـ CSV"""
        try:
            if not data:
                return ""
            
            exports_dir = self.base_dir / 'exports'
            exports_dir.mkdir(exist_ok=True)
            
            file_path = exports_dir / f"{filename}_{int(datetime.now().timestamp())}.csv"
            
            # استخراج العناوين
            fieldnames = data[0].keys()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.info(f"💾 تم حفظ CSV: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"❌ فشل حفظ CSV: {e}")
            return ""

class PerformanceMonitor:
    """مراقب أداء النظام"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.operations_count = 0
    
    def start_operation(self):
        """بدء عملية جديدة"""
        self.operations_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الأداء"""
        current_time = datetime.now()
        elapsed = (current_time - self.start_time).total_seconds()
        
        return {
            'operations_count': self.operations_count,
            'elapsed_seconds': elapsed,
            'operations_per_second': self.operations_count / elapsed if elapsed > 0 else 0,
            'start_time': self.start_time.isoformat(),
            'current_time': current_time.isoformat()
            }
