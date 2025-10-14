#apps/pacientes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.usuarios.models import Usuario
from .models import Vinculo, SolicitacaoConexao
from apps.usuarios.decorators import profissional_required, paciente_required


@login_required
@profissional_required
def lista_pacientes(request):
    if not request.user.is_profissional():
        return redirect('dashboard_paciente')

    vinculos = Vinculo.objects.filter(profissional=request.user, ativo=True)
    pacientes = [v.paciente for v in vinculos]

    return render(request, 'pacientes/lista_pacientes.html', {'pacientes': pacientes})

@login_required
@profissional_required
def perfil_paciente(request, paciente_id):
    if not request.user.is_profissional():
        return redirect('dashboard_paciente')

    vinculo = get_object_or_404(
        Vinculo,
        paciente__id=paciente_id,
        profissional=request.user,
        ativo=True
    )

    paciente = vinculo.paciente
    return render(request, 'pacientes/perfil_paciente.html', {'paciente': paciente})

@login_required
@profissional_required
def enviar_solicitacao(request):
    if request.method == "POST":
        cpf_paciente = request.POST.get('cpf')
        try:
            paciente_usuario = Usuario.objects.get(cpf=cpf_paciente, tipo='paciente')
        except Usuario.DoesNotExist:
            messages.error(request, "Paciente não encontrado")
            return redirect('dashboard_profissional')

        # Verifica se já existe solicitação
        solicitacao, created = SolicitacaoConexao.objects.get_or_create(
            paciente=paciente_usuario,
            profissional=request.user
        )
        if not created:
            messages.warning(request, "Solicitação já enviada.")
        else:
            messages.success(request, "Solicitação enviada com sucesso!")
        return redirect('dashboard_profissional')

    return render(request, 'pacientes/enviar_solicitacao.html')

@login_required
@paciente_required
def lista_solicitacoes(request):
    solicitacoes = SolicitacaoConexao.objects.filter(paciente=request.user, aprovado=False)
    return render(request, 'pacientes/lista_solicitacoes.html', {'solicitacoes': solicitacoes})

@login_required
@paciente_required
def aprovar_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoConexao, id=solicitacao_id, paciente=request.user)
    solicitacao.aprovado = True
    solicitacao.save()

    # Cria ou atualiza o vínculo
    Vinculo.objects.update_or_create(
        paciente=request.user,
        defaults={'profissional': solicitacao.profissional, 'ativo': True}
    )

    messages.success(request, f"Profissional {solicitacao.profissional.get_full_name()} aprovado com sucesso!")
    return redirect('lista_solicitacoes')