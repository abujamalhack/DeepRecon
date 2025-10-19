#!/usr/bin/env python3
"""
ملف التشغيل الرئيسي النهائي لـ Replit
"""

import asyncio
import sys
import os
from pathlib import Path

# إعداد مسارات الاستيراد
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))

from core.replit_engine import QuantumReplitEngine
from utils.replit_helper import ReplitEnvironment

async def main():
    """الدالة الرئيسية المحسنة"""
    
    # إعداد البيئة
    env = ReplitEnvironment()
    
    # عرض الشعار
    display_welcome_banner()
    
    try:
        # إنشاء وتهيئة المحرك
        engine = QuantumReplitEngine()
        
        print("\n🔍 نظام QuantumOSINT جاهز للتشغيل على Replit!")
        print("=" * 50)
        
        # عرض قائمة الأوامر
        while True:
            print("\n📋 قائمة الأوامر المتاحة:")
            print("1. 🔍 مسح أهداف")
            print("2. 📊 عرض الإحصائيات")
            print("3. ⚙️  إعدادات النظام")
            print("4. 🚪 خروج")
            
            choice = input("\nاختر رقم الأمر: ").strip()
            
            if choice == "1":
                await run_scan(engine)
            elif choice == "2":
                await show_stats(engine)
            elif choice == "3":
                show_settings()
            elif choice == "4":
                print("👋 مع السلامة!")
                break
            else:
                print("❌ اختيار غير صحيح")
                
    except Exception as e:
        print(f"❌ خطأ في النظام: {e}")
        return 1
    
    return 0

async def run_scan(engine):
    """تشغيل مسح للأهداف"""
    print("\n🎯 إدخال الأهداف للمسح")
    print("ملاحظة: أدخل الأهداف مفصولة بفاصلة")
    
    targets_input = input("الأهداف: ").strip()
    
    if not targets_input:
        print("❌ لم تدخل أي أهداف")
        return
    
    targets = [t.strip() for t in targets_input.split(',')]
    
    print(f"\n🚀 بدء المسح لـ {len(targets)} هدف...")
    
    results = await engine.comprehensive_scan(targets)
    
    if 'error' in results:
        print(f"❌ فشل المسح: {results['error']}")
    else:
        print(f"✅ اكتمل المسح بنجاح!")
        print(f"📊 النتائج: {results['summary']}")

async def show_stats(engine):
    """عرض إحصائيات النظام"""
    stats = engine.environment.check_resources()
    print("\n📈 إحصائيات النظام:")
    for key, value in stats.items():
        print(f"   {key}: {value}")

def show_settings():
    """عرض إعدادات النظام"""
    from config.settings import settings
    print("\n⚙️  إعدادات النظام:")
    print(f"   الإصدار: {settings.VERSION}")
    print(f"   بيئة Replit: {settings.IS_REPLIT}")
    print(f"   طلبات متزامنة: {settings.MAX_CONCURRENT_REQUESTS}")

def display_welcome_banner():
    """عرض شعار الترحيب"""
    banner = r"""
    
  ██████  ██    ██  █████  ███    ██ ████████ ██    ██ ██   ██      ██████  ███████ ███    ██ ██ ████████ 
 ██       ██    ██ ██   ██ ████   ██    ██    ██    ██ ██  ██      ██    ██ ██      ████   ██ ██    ██    
 ██   ███ ██    ██ ███████ ██ ██  ██    ██    ██    ██ █████       ██    ██ █████   ██ ██  ██ ██    ██    
 ██    ██ ██    ██ ██   ██ ██  ██ ██    ██    ██    ██ ██  ██      ██    ██ ██      ██  ██ ██ ██    ██    
  ██████   ██████  ██   ██ ██   ████    ██     ██████  ██   ██      ██████  ███████ ██   ████ ██    ██    
 
        🤖 نظام OSINT المتقدم | الإصدار الكمي | تشغيل على Replit
        👨‍💻 المطور: أبو جمال عبد الناصر الشوكي
        📧 abujamalhack@mail2tor.com
        🌐 https://github.com/AbuJamilAlShawki/QuantumOSINT
        
    """
    print(banner)

if __name__ == "__main__":
    # تشغيل التطبيق
    exit_code = asyncio.run(main())
    exit(exit_code)
