"""Trial application model for storing form submissions."""
from django.db import models


class TrialApplication(models.Model):
    """存储试用申请表单提交"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', '待处理'
        CONTACTED = 'contacted', '已联系'
        APPROVED = 'approved', '已通过'
        REJECTED = 'rejected', '已拒绝'
    
    class UseCase(models.TextChoices):
        MARKET_ANALYSIS = 'market_analysis', '市场宏观分析'
        COMPETITOR_TRACKING = 'competitor_tracking', '竞争对手追踪'
        RISK_MONITORING = 'risk_monitoring', '舆情风险监测'
        INVESTMENT_RESEARCH = 'investment_research', '投资决策研报'
        OTHER = 'other', '其他定制需求'
    
    # 申请人信息
    name = models.CharField(
        max_length=100,
        verbose_name="姓名"
    )
    email = models.EmailField(
        verbose_name="邮箱"
    )
    organization = models.CharField(
        max_length=200,
        verbose_name="公司/机构"
    )
    title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="职位"
    )
    
    # 使用场景
    use_case = models.CharField(
        max_length=50,
        choices=UseCase.choices,
        default=UseCase.MARKET_ANALYSIS,
        verbose_name="主要用途"
    )
    
    # 留言
    message = models.TextField(
        blank=True,
        verbose_name="留言"
    )
    
    # 处理状态
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="处理状态"
    )
    
    # 管理员备注
    admin_notes = models.TextField(
        blank=True,
        verbose_name="管理员备注"
    )
    
    # 时间戳
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="申请时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )
    
    class Meta:
        db_table = "trial_applications"
        verbose_name = "试用申请"
        verbose_name_plural = "试用申请管理"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.organization} ({self.get_status_display()})"
