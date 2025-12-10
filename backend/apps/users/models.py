"""
Custom User model for AI Business Data Analysis Platform.

Extends Django's AbstractUser to allow future customization.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Import TrialApplication for easier access
from .trial_models import TrialApplication



class User(AbstractUser):
    """
    Custom User model.

    Extends AbstractUser to enable future customization such as:
    - API key storage
    - Usage tracking
    - Organization/team membership
    - Membership levels
    """

    class MembershipLevel(models.TextChoices):
        TRIAL = 'trial', '试用会员'
        STARTER = 'starter', '入门版'
        PRO = 'pro', '专业版'
        ENTERPRISE = 'enterprise', '企业版'
    
    # Monthly report limits per membership level (matching pricing page)
    MONTHLY_REPORT_LIMITS = {
        'trial': 3,        # 试用会员：3次
        'starter': 30,     # 入门版：每月30次
        'pro': 100,        # 专业版：每月100次
        'enterprise': 600, # 企业版：每月600次
    }

    # Optional: Add custom fields here
    company: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        help_text="用户公司或组织名称"
    )
    api_calls_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        help_text="用户的API调用次数"
    )
    
    # Membership fields
    membership_level: models.CharField = models.CharField(
        max_length=20,
        choices=MembershipLevel.choices,
        default=MembershipLevel.TRIAL,
        verbose_name="会员等级",
        help_text="用户的会员等级"
    )
    membership_expires_at: models.DateTimeField = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="会员到期时间",
        help_text="会员有效期截止日期"
    )
    
    # Monthly report tracking
    monthly_reports_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        verbose_name="本月报告数",
        help_text="当月已生成的报告数量"
    )
    last_report_month: models.DateField = models.DateField(
        null=True,
        blank=True,
        verbose_name="最后报告月份",
        help_text="最后生成报告的月份"
    )

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = "用户管理"

    def __str__(self) -> str:
        return self.username
    
    def get_monthly_report_limit(self) -> int:
        """获取当前会员等级的每月报告限制"""
        return self.MONTHLY_REPORT_LIMITS.get(self.membership_level, 3)
    
    # Legacy compatibility - map to monthly methods
    def get_daily_report_limit(self) -> int:
        """Legacy: 返回每月限额（兼容旧代码）"""
        return self.get_monthly_report_limit()
    
    def is_membership_active(self) -> bool:
        """检查会员是否有效（未过期）"""
        if self.membership_expires_at is None:
            return False
        return timezone.now() < self.membership_expires_at
    
    def can_generate_report(self) -> bool:
        """检查用户是否可以生成报告（会员有效且未超限额）"""
        # Check if membership is expired
        if not self.is_membership_active():
            return False
        
        today = timezone.now().date()
        current_month = today.replace(day=1)
        
        # Reset counter if it's a new month
        if self.last_report_month is None or self.last_report_month.replace(day=1) != current_month:
            return True
        
        return self.monthly_reports_count < self.get_monthly_report_limit()
    
    def increment_report_count(self) -> None:
        """增加本月报告计数"""
        today = timezone.now().date()
        current_month = today.replace(day=1)
        
        # Reset counter if it's a new month
        if self.last_report_month is None or self.last_report_month.replace(day=1) != current_month:
            self.monthly_reports_count = 1
            self.last_report_month = today
        else:
            self.monthly_reports_count += 1
        
        self.save(update_fields=['monthly_reports_count', 'last_report_month'])
    
    def get_remaining_reports(self) -> int:
        """获取本月剩余可生成的报告数量"""
        today = timezone.now().date()
        current_month = today.replace(day=1)
        
        if self.last_report_month is None or self.last_report_month.replace(day=1) != current_month:
            return self.get_monthly_report_limit()
        
        return max(0, self.get_monthly_report_limit() - self.monthly_reports_count)

