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
        MONTHLY = 'monthly', '月度会员'
        QUARTERLY = 'quarterly', '季度会员'
        YEARLY = 'yearly', '年度会员'
    
    # Daily report limits per membership level
    DAILY_REPORT_LIMITS = {
        'trial': 1,
        'monthly': 5,
        'quarterly': 10,
        'yearly': 15,
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
    
    # Daily report tracking
    daily_reports_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        verbose_name="今日报告数",
        help_text="当天已生成的报告数量"
    )
    last_report_date: models.DateField = models.DateField(
        null=True,
        blank=True,
        verbose_name="最后报告日期",
        help_text="最后生成报告的日期"
    )

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = "用户管理"

    def __str__(self) -> str:
        return self.username
    
    def get_daily_report_limit(self) -> int:
        """获取当前会员等级的每日报告限制"""
        return self.DAILY_REPORT_LIMITS.get(self.membership_level, 1)
    
    def can_generate_report(self) -> bool:
        """检查用户今天是否还能生成报告"""
        today = timezone.now().date()
        
        # Reset counter if it's a new day
        if self.last_report_date != today:
            return True
        
        return self.daily_reports_count < self.get_daily_report_limit()
    
    def increment_report_count(self) -> None:
        """增加今日报告计数"""
        today = timezone.now().date()
        
        # Reset counter if it's a new day
        if self.last_report_date != today:
            self.daily_reports_count = 1
            self.last_report_date = today
        else:
            self.daily_reports_count += 1
        
        self.save(update_fields=['daily_reports_count', 'last_report_date'])
    
    def get_remaining_reports(self) -> int:
        """获取今天剩余可生成的报告数量"""
        today = timezone.now().date()
        
        if self.last_report_date != today:
            return self.get_daily_report_limit()
        
        return max(0, self.get_daily_report_limit() - self.daily_reports_count)

