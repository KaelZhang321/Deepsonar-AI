"""
Django Management Command: Fix Report User Association

This command helps diagnose and fix reports that are not properly associated with users.

Usage (run inside Docker container):
    docker exec -it deepsonar-django python manage.py fix_report_users --check
    docker exec -it deepsonar-django python manage.py fix_report_users --fix --target-user kaelzhang
"""
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Q

from apps.reports.models import Report
from apps.users.models import User


class Command(BaseCommand):
    help = '检查并修复报告的用户关联'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check',
            action='store_true',
            help='仅检查，不做修改',
        )
        parser.add_argument(
            '--fix',
            action='store_true',
            help='修复无用户关联的报告',
        )
        parser.add_argument(
            '--target-user',
            type=str,
            help='将无关联报告分配给指定用户名的用户',
        )
        parser.add_argument(
            '--reassign-all',
            action='store_true',
            help='将所有报告重新分配给目标用户（危险操作）',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('=' * 60))
        self.stdout.write(self.style.NOTICE('📊 报告用户关联检查与修复'))
        self.stdout.write(self.style.NOTICE('=' * 60))

        # 统计数据
        total_reports = Report.objects.count()
        reports_with_user = Report.objects.exclude(user__isnull=True).count()
        reports_without_user = Report.objects.filter(user__isnull=True).count()
        completed_reports = Report.objects.filter(status=Report.Status.COMPLETED).count()

        self.stdout.write(f'\n总报告数: {total_reports}')
        self.stdout.write(f'已完成报告: {completed_reports}')
        self.stdout.write(f'有用户关联的报告: {reports_with_user}')
        self.stdout.write(self.style.WARNING(f'无用户关联的报告: {reports_without_user}'))

        # 显示用户统计
        self.stdout.write('\n' + '-' * 60)
        self.stdout.write('按用户统计:')
        self.stdout.write('-' * 60)
        
        for user in User.objects.all():
            user_reports = Report.objects.filter(user=user).count()
            user_completed = Report.objects.filter(user=user, status=Report.Status.COMPLETED).count()
            self.stdout.write(
                f'  用户 {user.username} (ID: {user.id}): 总共 {user_reports} 份，已完成 {user_completed} 份'
            )

        # 显示无用户关联的报告
        if reports_without_user > 0:
            self.stdout.write('\n' + '-' * 60)
            self.stdout.write(self.style.WARNING('⚠️ 无用户关联的报告:'))
            self.stdout.write('-' * 60)
            
            orphan_reports = Report.objects.filter(user__isnull=True).order_by('-created_at')[:20]
            for report in orphan_reports:
                self.stdout.write(
                    f'  Report #{report.id}: {report.query[:40]}... '
                    f'({report.status}, {report.created_at.strftime("%Y-%m-%d %H:%M")})'
                )
            
            if reports_without_user > 20:
                self.stdout.write(f'  ... 还有 {reports_without_user - 20} 条未显示')

        # 修复操作
        if options['fix']:
            if not options['target_user']:
                raise CommandError('必须使用 --target-user 指定目标用户')
            
            try:
                target_user = User.objects.get(username=options['target_user'])
            except User.DoesNotExist:
                raise CommandError(f'用户 "{options["target_user"]}" 不存在')
            
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write(self.style.NOTICE(f'🔧 开始修复，目标用户: {target_user.username}'))
            self.stdout.write('=' * 60)
            
            if options['reassign_all']:
                # 重新分配所有报告
                affected = Report.objects.all().update(user=target_user)
                self.stdout.write(self.style.SUCCESS(f'✅ 已将所有 {affected} 份报告分配给用户 {target_user.username}'))
            else:
                # 仅分配无用户关联的报告
                affected = Report.objects.filter(user__isnull=True).update(user=target_user)
                self.stdout.write(self.style.SUCCESS(f'✅ 已将 {affected} 份无关联报告分配给用户 {target_user.username}'))

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('检查完成'))
        self.stdout.write('=' * 60)
