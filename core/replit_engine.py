#!/usr/bin/env python3
"""
المحرك الرئيسي المعدل لبيئة Replit
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from config.settings import settings
from utils.replit_helper import ReplitEnvironment, ReplitSecurity

class QuantumReplitEngine:
    """محرك QuantumOSINT مخصص لـ Replit"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.environment = ReplitEnvironment()
        self.security = ReplitSecurity()
        
        # إعدادات المحرك
        self.session = None
        self.active_tasks = []
        self.scan_results = {}
        
        # إعداد المكونات
        self.setup_components()
    
    def setup_components(self):
        """إعداد مكونات النظام"""
        self.logger.info("🔧 إعداد مكونات QuantumOSINT لـ Replit...")
        
        # استيراد المكونات الديناميكي
        try:
            from plugins.social_media.facebook_light import FacebookLightAnalyzer
            self.facebook_analyzer = FacebookLightAnalyzer()
            self.logger.info("✅ Facebook analyzer loaded")
        except ImportError as e:
            self.logger.warning(f"Facebook analyzer not available: {e}")
        
        try:
            from plugins.data_sources.email_analyzer import EmailIntelligence
            self.email_analyzer = EmailIntelligence()
            self.logger.info("✅ Email analyzer loaded")
        except ImportError as e:
            self.logger.warning(f"Email analyzer not available: {e}")
    
    async def initialize(self):
        """تهيئة المحرك"""
        self.logger.info("🚀 تهيئة محرك QuantumOSINT...")
        
        # فحص اتصال الإنترنت
        if not await self.environment.check_internet():
            self.logger.error("❌ لا يوجد اتصال بالإنترنت")
            return False
        
        # إعداد جلسة HTTP
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=settings.REQUEST_TIMEOUT)
        )
        
        self.logger.info("✅ اكتملت التهيئة بنجاح")
        return True
    
    async def comprehensive_scan(self, targets: List[str]) -> Dict[str, Any]:
        """مسح شامل للأهداف"""
        self.logger.info(f"🎯 بدء المسح الشامل لـ {len(targets)} هدف")
        
        if not await self.initialize():
            return {'error': 'فشل تهيئة النظام'}
        
        try:
            scan_id = f"scan_{int(datetime.now().timestamp())}"
            results = {
                'scan_id': scan_id,
                'start_time': datetime.now().isoformat(),
                'targets': targets,
                'results': {}
            }
            
            # معالجة كل هدف
            for target in targets:
                if not self.security.validate_target(target):
                    self.logger.warning(f"هدف غير صالح تم تخطيه: {target}")
                    continue
                
                target_results = await self.process_target(target)
                results['results'][target] = target_results
            
            # إضافة التحليلات النهائية
            results['end_time'] = datetime.now().isoformat()
            results['summary'] = self.generate_summary(results['results'])
            
            # حفظ النتائج
            await self.save_results(results)
            
            self.logger.info("✅ اكتمل المسح الشامل بنجاح")
            return results
            
        except Exception as e:
            self.logger.error(f"❌ فشل المسح الشامل: {e}")
            return {'error': str(e)}
        
        finally:
            await self.cleanup()
    
    async def process_target(self, target: str) -> Dict[str, Any]:
        """معالجة هدف فردي"""
        target_results = {
            'target': target,
            'type': self.detect_target_type(target),
            'analysis': {},
            'contacts': {},
            'timeline': []
        }
        
        try:
            # التحليل حسب نوع الهدف
            if target_results['type'] == 'email':
                email_analysis = await self.email_analyzer.analyze(target)
                target_results['analysis']['email'] = email_analysis
            
            elif target_results['type'] == 'username':
                # تحليل اسم المستخدم عبر المنصات
                platform_analysis = await self.analyze_username_across_platforms(target)
                target_results['analysis']['platforms'] = platform_analysis
            
            elif target_results['type'] == 'phone':
                phone_analysis = await self.analyze_phone_number(target)
                target_results['analysis']['phone'] = phone_analysis
            
            # استخراج جهات الاتصال
            target_results['contacts'] = await self.extract_contacts(target_results)
            
            # تسجيل الجدول الزمني
            target_results['timeline'].append({
                'timestamp': datetime.now().isoformat(),
                'action': 'analysis_completed',
                'details': f'تم تحليل {target}'
            })
            
        except Exception as e:
            self.logger.error(f"❌ فشل معالجة الهدف {target}: {e}")
            target_results['error'] = str(e)
        
        return target_results
    
    def detect_target_type(self, target: str) -> str:
        """كشف نوع الهدف"""
        import re
        
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', target):
            return 'email'
        elif re.match(r'^\+?[1-9]\d{1,14}$', target):
            return 'phone'
        elif re.match(r'^@?[a-zA-Z0-9_]{1,30}$', target):
            return 'username'
        else:
            return 'unknown'
    
    async def analyze_username_across_platforms(self, username: str) -> Dict[str, Any]:
        """تحليل اسم المستخدم عبر منصات متعددة"""
        platform_results = {}
        
        # إزالة @ إذا موجودة
        clean_username = username.lstrip('@')
        
        # منصات للتحقق
        platforms = {
            'github': f'https://api.github.com/users/{clean_username}',
            'twitter': f'https://api.twitter.com/2/users/by/username/{clean_username}',
        }
        
        for platform, url in platforms.items():
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        platform_results[platform] = {
                            'exists': True,
                            'data': data
                        }
                    else:
                        platform_results[platform] = {
                            'exists': False,
                            'status': response.status
                        }
            except Exception as e:
                platform_results[platform] = {
                    'exists': False,
                    'error': str(e)
                }
        
        return platform_results
    
    async def extract_contacts(self, target_data: Dict) -> Dict[str, List]:
        """استخراج جهات الاتصال من البيانات"""
        contacts = {
            'emails': [],
            'phones': [],
            'social_links': []
        }
        
        try:
            # تحليل البيانات لاكتشاف جهات الاتصال
            data_str = json.dumps(target_data).lower()
            
            # البحث عن إيميلات
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, data_str)
            contacts['emails'] = list(set(emails))
            
            # البحث عن هواتف
            phone_patterns = [
                r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
                r'\d{3}[-.]?\d{3}[-.]?\d{4}'
            ]
            for pattern in phone_patterns:
                phones = re.findall(pattern, data_str)
                contacts['phones'].extend(phones)
            
            # إزالة التكرارات
            contacts['phones'] = list(set(contacts['phones']))
            
        except Exception as e:
            self.logger.warning(f"استخراج جهات الاتصال فشل: {e}")
        
        return contacts
    
    def generate_summary(self, results: Dict) -> Dict[str, Any]:
        """توليد ملخص النتائج"""
        total_targets = len(results)
        successful_scans = sum(1 for r in results.values() if 'error' not in r)
        total_contacts = sum(len(r.get('contacts', {}).get('emails', [])) + 
                           len(r.get('contacts', {}).get('phones', [])) 
                           for r in results.values() if 'contacts' in r)
        
        return {
            'total_targets': total_targets,
            'successful_scans': successful_scans,
            'success_rate': (successful_scans / total_targets * 100) if total_targets > 0 else 0,
            'total_contacts_found': total_contacts,
            'scan_quality': 'high' if successful_scans > 0 else 'low'
        }
    
    async def save_results(self, results: Dict):
        """حفظ النتائج"""
        try:
            from utils.helpers import DataSaver
            saver = DataSaver()
            
            # حفظ كـ JSON
            json_path = await saver.save_json(results, 'scan_results')
            
            # حفظ كـ HTML report
            html_path = await self.generate_html_report(results)
            
            self.logger.info(f"💾 النتائج محفوظة: {json_path}, {html_path}")
            
        except Exception as e:
            self.logger.error(f"❌ فشل حفظ النتائج: {e}")
    
    async def generate_html_report(self, results: Dict) -> str:
        """توليد تقرير HTML"""
        try:
            report_template = """
            <!DOCTYPE html>
            <html dir="rtl">
            <head>
                <meta charset="UTF-8">
                <title>تقرير QuantumOSINT</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; direction: rtl; }
                    .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
                    .result { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
                    .contact { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 3px; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>تقرير QuantumOSINT</h1>
                    <p>تم إنشاء التقرير في: {timestamp}</p>
                </div>
                
                <div class="summary">
                    <h2>ملخص النتائج</h2>
                    <p>عدد الأهداف: {total_targets}</p>
                    <p>نسبة النجاح: {success_rate}%</p>
                    <p>جهات اتصال مكتشفة: {total_contacts}</p>
                </div>
                
                {results_html}
            </body>
            </html>
            """
            
            # توليد HTML للنتائج
            results_html = ""
            for target, data in results.get('results', {}).items():
                results_html += f"""
                <div class="result">
                    <h3>الهدف: {target}</h3>
                    <p>النوع: {data.get('type', 'غير معروف')}</p>
                    <div class="contacts">
                        <h4>جهات الاتصال:</h4>
                        {''.join(f'<div class="contact">📧 {email}</div>' for email in data.get('contacts', {}).get('emails', []))}
                        {''.join(f'<div class="contact">📞 {phone}</div>' for phone in data.get('contacts', {}).get('phones', []))}
                    </div>
                </div>
                """
            
            final_html = report_template.format(
                timestamp=datetime.now().isoformat(),
                total_targets=len(results.get('results', {})),
                success_rate=results.get('summary', {}).get('success_rate', 0),
                total_contacts=results.get('summary', {}).get('total_contacts_found', 0),
                results_html=results_html
            )
            
            # حفظ الملف
            reports_dir = self.environment.base_dir / 'reports'
            reports_dir.mkdir(exist_ok=True)
            
            report_path = reports_dir / f"report_{int(datetime.now().timestamp())}.html"
            report_path.write_text(final_html, encoding='utf-8')
            
            return str(report_path)
            
        except Exception as e:
            self.logger.error(f"❌ فشل توليد تقرير HTML: {e}")
            return ""
    
    async def cleanup(self):
        """تنظيف الموارد"""
        if self.session:
            await self.session.close()
        
        # إلغاء أي مهام نشطة
        for task in self.active_tasks:
            if not task.done():
                task.cancel()
        
        self.logger.info("🧹 تم تنظيف الموارد")
