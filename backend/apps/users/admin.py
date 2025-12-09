"""Admin configuration for the users app."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count

from .models import User
from apps.reports.models import Report


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with membership management."""

    list_display = (
        "username",
        "email",
        "membership_level",
        "get_total_reports",
        "daily_reports_count",
        "get_remaining_reports_display",
        "membership_expires_at",
        "is_staff",
        "date_joined",
    )
    list_filter = ("membership_level", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "company")
    list_editable = ("membership_level",)
    
    # Add custom fields to the fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ("公司信息", {"fields": ("company",)}),
        ("会员信息", {
            "fields": (
                "membership_level",
                "membership_expires_at",
                "daily_reports_count",
                "last_report_date",
            ),
            "description": "用户会员等级和报告使用情况"
        }),
        ("API使用", {"fields": ("api_calls_count",)}),
    )
    
    readonly_fields = ("daily_reports_count", "last_report_date", "api_calls_count")
    
    def get_queryset(self, request):
        """Annotate queryset with total reports count."""
        queryset = super().get_queryset(request)
        return queryset.annotate(total_reports=Count('reports'))
    
    @admin.display(description='报告总数')
    def get_total_reports(self, obj):
        """显示用户的报告总数"""
        return getattr(obj, 'total_reports', Report.objects.filter(user=obj).count())
    
    @admin.display(description='今日剩余')
    def get_remaining_reports_display(self, obj):
        """显示今日剩余可生成报告数"""
        remaining = obj.get_remaining_reports()
        limit = obj.get_daily_report_limit()
        return f"{remaining}/{limit}"


# TrialApplication Admin
from .trial_models import TrialApplication
from django.utils import timezone
from datetime import timedelta
import secrets
import string

@admin.register(TrialApplication)
class TrialApplicationAdmin(admin.ModelAdmin):
    """试用申请管理"""
    
    list_display = (
        "name",
        "email",
        "organization",
        "title",
        "use_case",
        "status",
        "created_at",
    )
    list_filter = ("status", "use_case", "created_at")
    search_fields = ("name", "email", "organization", "message")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        ("申请人信息", {
            "fields": ("name", "email", "organization", "title")
        }),
        ("申请详情", {
            "fields": ("use_case", "message")
        }),
        ("处理状态", {
            "fields": ("status", "admin_notes")
        }),
        ("时间信息", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    
    def save_model(self, request, obj, form, change):
        """Override save to create trial user when status changes to approved."""
        # Get the old status if this is an update
        old_status = None
        if change and obj.pk:
            old_obj = TrialApplication.objects.get(pk=obj.pk)
            old_status = old_obj.status
        
        # Save the object first
        super().save_model(request, obj, form, change)
        
        # Check if status changed to 'approved'
        if obj.status == 'approved' and old_status != 'approved':
            # Create trial user account
            user, password = self._create_trial_user(obj)
            if user:
                # Send email with credentials
                self._send_approval_email(obj, user, password)
                # Update admin notes
                obj.admin_notes = f"{obj.admin_notes}\n\n[系统] 已创建试用账号: {user.username}"
                obj.save()
    
    def _generate_password(self, length=12):
        """Generate a random password."""
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    def _create_trial_user(self, application):
        """Create a trial user account from application."""
        # Generate username from email
        base_username = application.email.split('@')[0]
        username = base_username
        counter = 1
        
        # Ensure unique username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Generate password
        password = self._generate_password()
        
        # Calculate expiration (3 days from now)
        expires_at = timezone.now() + timedelta(days=3)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=application.email,
            password=password,
            first_name=application.name,
            company=application.organization,
            membership_level='trial',
            membership_expires_at=expires_at,
        )
        
        return user, password
    
    def _send_approval_email(self, application, user, password):
        """Send approval email with login credentials using redmail."""
        import os
        from redmail import outlook
        
        # Configure Outlook
        outlook.username = os.getenv('EMAIL_HOST_USER', 'deepsonar-service@outlook.com')
        outlook.password = os.getenv('EMAIL_HOST_PASSWORD', '')
        
        expires_date = user.membership_expires_at.strftime('%Y年%m月%d日 %H:%M')
        
        html_content = f"""
<div style="font-family: 'Microsoft YaHei', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #f5f5f5;">
    <div style="background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
        <h2 style="color: #6366f1; margin-top: 0;">🎉 DeepSonar 试用申请已通过</h2>
        
        <p>尊敬的 <strong>{application.name}</strong>，</p>
        
        <p>恭喜！您的 DeepSonar AI 试用申请已通过审核。</p>
        
        <div style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: white; padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: white;">您的试用账号信息</h3>
            <p style="margin: 8px 0;"><strong>账号：</strong>{user.username}</p>
            <p style="margin: 8px 0;"><strong>密码：</strong>{password}</p>
            <p style="margin: 8px 0;"><strong>有效期至：</strong>{expires_date}</p>
        </div>
        
        <p><a href="http://localhost:8001" style="display: inline-block; background: #6366f1; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">立即登录 →</a></p>
        
        <h4>试用期间，您可以：</h4>
        <ul>
            <li>每天生成 1 份深度分析报告</li>
            <li>体验全域情报捕获功能</li>
            <li>使用 AI 深度清洗与结构化决策报告</li>
        </ul>
        
        <p>如需升级为正式会员，请联系我们的销售团队。</p>
        
        <p style="color: #666; margin-top: 30px;">
            祝您使用愉快！<br/>
            <strong>DeepSonar AI 团队</strong>
        </p>
    </div>
</div>
"""
        
        try:
            outlook.send(
                subject="🎉 DeepSonar 试用申请已通过",
                receivers=[application.email],
                html=html_content,
            )
            print(f"邮件发送成功: {application.email}")
        except Exception as e:
            print(f"邮件发送失败: {e}")



