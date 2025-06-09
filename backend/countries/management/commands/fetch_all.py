from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = '모든 fetch 커맨드를 한 번에 실행합니다.'

    def handle(self, *args, **kwargs):
        fetch_commands = [
            "fetch_embassy_data",
            "fetch_safety_data",
            "fetch_safety_notice",
        ]

        for cmd in fetch_commands:
            self.stdout.write(self.style.NOTICE(f"→ 실행 중: {cmd}"))
            call_command(cmd)
            self.stdout.write(self.style.SUCCESS(f"✅ 완료: {cmd}"))