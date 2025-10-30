# apps/consultas/tasks.py
from datetime import date, datetime, timedelta, time as dtime
from django.utils import timezone
from django.db import IntegrityError
from apps.consultas.models import Recorrencia, Consulta

def _add_months(orig_date, months):
    """Adiciona meses a uma date (cuidando de fim do mês)."""
    month = orig_date.month - 1 + months
    year = orig_date.year + month // 12
    month = month % 12 + 1
    day = min(orig_date.day, (date(year, month + 1, 1) - timedelta(days=1)).day)
    return date(year, month, day)

def _add_years(orig_date, years):
    try:
        return orig_date.replace(year=orig_date.year + years)
    except ValueError:
        # 29/02 -> 28/02 em anos não bissextos
        return orig_date.replace(month=2, day=28, year=orig_date.year + years)

def _next_by_recorrencia(start_date, recorrencia):
    """Dado uma data/recorrencia, retorna próxima data baseada em unidade/valor."""
    unit = recorrencia.recorrencia_unidade
    val = recorrencia.recorrencia_valor or 1
    if unit == 'semanas':
        return start_date + timedelta(weeks=val)
    if unit == 'meses':
        return _add_months(start_date, val)
    if unit == 'anos':
        return _add_years(start_date, val)
    return None

def _time_conflict_exists(profissional, target_date, target_time):
    """
    Verifica se existe consulta do profissional em target_date que conflite em 1h.
    Retorna True se conflito.
    """
    # pega todas consultas do profissional naquela data
    consultas = Consulta.objects.filter(profissional=profissional, data=target_date)
    target_dt = datetime.combine(target_date, target_time)
    for c in consultas:
        existing_dt = datetime.combine(c.data, c.horario)
        diff = abs((existing_dt - target_dt).total_seconds())
        if diff < 3600:  # menos de 1 hora => conflito
            return True
    return False

def gerar_consultas_recorrentes(horizon_months=6):
    """
    Gera consultas futuras para cada Recorrencia ativa até horizon_months a partir de hoje.
    - Mantém um buffer de consultas geradas até horizon.
    - Evita duplicação / respeita regra de 1h de duração.
    """
    now = timezone.localtime(timezone.now())
    hoje = now.date()
    horizon_date = _add_months(hoje, horizon_months)

    recorrencias = Recorrencia.objects.filter(ativa=True)

    created = 0
    for r in recorrencias:
        # Pega última consulta gerada para essa recorrência (mais recente)
        ultima = r.consultas_geradas.order_by('-data', '-horario').first()

        # Se não existe nenhuma consulta gerada, buscamos a próxima data a partir de hoje
        if ultima:
            cursor = ultima.data
        else:
            # encontrar próximo dia da semana >= hoje baseado em r.dia_semana
            # se dia_semana não estiver definido, ignora (defina no form)
            try:
                target_weekday = int(r.dia_semana)
            except Exception:
                # se não tiver dia_semana, pula (não temos como calcular)
                continue

            cursor = hoje
            # avança até achar o weekday desejado (pode ser hoje)
            days_ahead = (target_weekday - cursor.weekday() + 7) % 7
            cursor = cursor + timedelta(days=days_ahead)

            # Se a data inicial for no passado por alguma razão: assegure >= hoje
            if cursor < hoje:
                cursor = hoje

            # não vamos criar a consulta inicial aqui: assumimos que a primeira consulta
            # foi criada manualmente quando o usuário marcou pela primeira vez.
            # porém com cursor definido podemos gerar próximas a partir desse ponto.
            # A lógica abaixo sempre começa gerando a próxima a partir de cursor.

        # agora gera iterativamente próximas datas até o horizon_date
        next_date = _next_by_recorrencia(cursor, r)
        while next_date and next_date <= horizon_date:
            # só cria se for futura (>= hoje)
            if next_date <= hoje:
                next_date = _next_by_recorrencia(next_date, r)
                continue

            # verifica conflito de horário (1h)
            if _time_conflict_exists(r.profissional, next_date, r.horario_padrao):
                # pula e tenta próxima ocorrência
                next_date = _next_by_recorrencia(next_date, r)
                continue

            # cria
            try:
                Consulta.objects.create(
                    vinculo=r.vinculo,
                    profissional=r.profissional,
                    paciente=r.paciente,
                    data=next_date,
                    horario=r.horario_padrao,
                    recorrencia=r
                )
                created += 1
            except IntegrityError:
                # já existia por unique_together ou condição de corrida
                pass

            # avança
            next_date = _next_by_recorrencia(next_date, r)

    print(f"[{timezone.localtime(timezone.now())}] Geração concluída. Consultas criadas: {created}")
