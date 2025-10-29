#apps/consultas/management/commands/run_scheduler.py
import time
import schedule
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.consultas.tasks import gerar_proximas_consultas


class Command(BaseCommand):
    help = "Executa o agendador de consultas recorrentes (use em produção com supervisão do sistema)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            f"[SCHEDULER] Iniciando agendador em {timezone.localtime(timezone.now())}"
        ))

        # Executa a verificação a cada hora
        schedule.every(1).hour.do(gerar_proximas_consultas)

        while True:
            schedule.run_pending()
            time.sleep(30)  # checa a cada 30 segundos se há tarefas pendentes
