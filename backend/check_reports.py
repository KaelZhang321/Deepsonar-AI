#!/usr/bin/env python
"""
验证报告用户关联的脚本。
在 Django shell 中运行：python manage.py shell < check_reports.py
"""
import os
import sys
import django

# 设置 Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.reports.models import Report
from apps.users.models import User

print("=" * 60)
print("📊 报告用户关联检查")
print("=" * 60)

# 统计报告
total_reports = Report.objects.count()
reports_with_user = Report.objects.exclude(user__isnull=True).count()
reports_without_user = Report.objects.filter(user__isnull=True).count()

print(f"\n总报告数: {total_reports}")
print(f"有用户关联的报告: {reports_with_user}")
print(f"无用户关联的报告: {reports_without_user}")

# 按用户统计
print("\n" + "-" * 60)
print("按用户统计报告数:")
print("-" * 60)

for user in User.objects.all():
    user_reports = Report.objects.filter(user=user, status=Report.Status.COMPLETED).count()
    print(f"  用户 {user.username} (ID: {user.id}): {user_reports} 份已完成报告")

# 显示无用户关联的报告
if reports_without_user > 0:
    print("\n" + "-" * 60)
    print("⚠️ 无用户关联的报告 (最近10个):")
    print("-" * 60)
    for report in Report.objects.filter(user__isnull=True).order_by('-created_at')[:10]:
        print(f"  Report #{report.id}: {report.query[:40]}... ({report.created_at.strftime('%Y-%m-%d %H:%M')})")

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)
