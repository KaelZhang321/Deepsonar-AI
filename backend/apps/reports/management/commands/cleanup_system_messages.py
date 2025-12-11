"""
Django Management Command: Clean up system messages from chat history.

This command removes "Previous conversation" and other system messages
that were incorrectly saved to the database.

Usage:
    docker exec -it deepsonar-django python manage.py cleanup_system_messages --check
    docker exec -it deepsonar-django python manage.py cleanup_system_messages --fix
"""
from django.core.management.base import BaseCommand
from django.db.models import Q

from apps.reports.models import ChatMessage


class Command(BaseCommand):
    help = '清理聊天历史中的系统消息'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check',
            action='store_true',
            help='仅检查，不做修改',
        )
        parser.add_argument(
            '--fix',
            action='store_true',
            help='删除系统消息',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('=' * 60))
        self.stdout.write(self.style.NOTICE('🧹 清理聊天历史中的系统消息'))
        self.stdout.write(self.style.NOTICE('=' * 60))

        # Define patterns to match system messages
        system_patterns = [
            'Previous conversation',
            '会话已恢复',
            '欢迎回来',
            'Continue the conversation',
        ]

        # Build query
        query = Q()
        for pattern in system_patterns:
            query |= Q(content__icontains=pattern)

        # Find system messages
        system_messages = ChatMessage.objects.filter(query)
        count = system_messages.count()

        self.stdout.write(f'\n找到 {count} 条系统消息需要清理')

        if count > 0:
            self.stdout.write('\n示例消息:')
            for msg in system_messages[:10]:
                preview = msg.content[:60].replace('\n', ' ')
                self.stdout.write(f'  - [{msg.sender}] {preview}...')
            
            if count > 10:
                self.stdout.write(f'  ... 还有 {count - 10} 条')

        if options['fix']:
            if count > 0:
                deleted, _ = system_messages.delete()
                self.stdout.write(self.style.SUCCESS(f'\n✅ 已删除 {deleted} 条系统消息'))
            else:
                self.stdout.write(self.style.SUCCESS('\n✅ 无需清理'))
        else:
            if count > 0:
                self.stdout.write(self.style.WARNING('\n⚠️ 使用 --fix 参数来删除这些消息'))

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('检查完成'))
        self.stdout.write('=' * 60)
