#apps/consultas/tasks.py:
from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError
from apps.consultas.models import Recorrencia, Consulta


def gerar_proximas_consultas():
    """
    Gera automaticamente as próximas consultas com base nas recorrências ativas.
    Cada consulta tem duração de 1 hora e não pode haver conflito de horário.
    """
    agora = timezone.localtime(timezone.now())
    hoje = agora.date()

    recorrencias = Recorrencia.objects.filter(ativa=True)

    for r in recorrencias:
        # Pega a última consulta já gerada para essa recorrência
        ultima_consulta = r.consultas_geradas.order_by('-data', '-horario').first()

        # Se nunca houve consulta, ignora (será criada manualmente ao marcar a primeira)
        if not ultima_consulta:
            continue

        # Calcula a próxima data conforme unidade e valor de recorrência
        if r.recorrencia_unidade == 'semanas':
            proxima_data = ultima_consulta.data + timedelta(weeks=r.recorrencia_valor)
        elif r.recorrencia_unidade == 'meses':
            proxima_data = ultima_consulta.data + timedelta(days=30 * r.recorrencia_valor)
        elif r.recorrencia_unidade == 'anos':
            proxima_data = ultima_consulta.data + timedelta(days=365 * r.recorrencia_valor)
        else:
            continue

        # Só cria consultas futuras
        if proxima_data <= hoje:
            continue

        # Verifica se já existe consulta nesse horário
        conflito = Consulta.objects.filter(
            profissional=r.profissional,
            data=proxima_data,
            horario=r.horario_padrao
        ).exists()

        if conflito:
            continue  # pula, já existe uma consulta no mesmo horário

        # Cria a nova consulta
        try:
            Consulta.objects.create(
                vinculo=r.vinculo,
                profissional=r.profissional,
                paciente=r.paciente,
                data=proxima_data,
                horario=r.horario_padrao,
                recorrencia=r
            )
            print(f"[OK] Próxima consulta criada: {r.paciente} em {proxima_data} ({r.horario_padrao})")

        except IntegrityError:
            print(f"[ERRO] Conflito ao criar consulta para {r.paciente} em {proxima_data} ({r.horario_padrao})")

    print(f"[{timezone.localtime(timezone.now())}] Geração de consultas recorrentes concluída.")
