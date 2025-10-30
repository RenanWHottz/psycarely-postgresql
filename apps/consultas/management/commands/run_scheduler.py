# apps/consultas/management/commands/run_scheduler.py
from django.core.management.base import BaseCommand
import schedule
import time
from django.utils import timezone
from apps.consultas.tasks import gerar_consultas_recorrentes

class Command(BaseCommand):
    help = "Executa o agendador de consultas recorrentes"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            f"[SCHEDULER] Iniciando agendador em {timezone.localtime(timezone.now())}"
        ))

        # rotina: diariamente gerar/garantir buffer de consultas até 6 meses
        # (pode ajustar para every().day.at("00:01") se preferir)
        schedule.every().day.at("00:01").do(gerar_consultas_recorrentes, horizon_months=6)

        # também roda na inicialização para não esperar até a meia-noite
        gerar_consultas_recorrentes(horizon_months=6)

        while True:
            schedule.run_pending()
            time.sleep(30)
