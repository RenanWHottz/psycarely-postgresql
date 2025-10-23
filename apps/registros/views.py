#apps/registros/views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.usuarios.decorators import profissional_required, paciente_required
from django.contrib.auth.decorators import login_required
from .models import RPD, RegistroHumor, AnotacaoGeral, AnotacaoConsulta
from .forms import RPDForm, RegistroHumorForm, AnotacaoGeralForm, AnotacaoConsultaForm
from django.utils import timezone


@login_required
@paciente_required
def tarefas_paciente(request):
    return render(request, 'registros/tarefas_paciente.html')

@login_required
@paciente_required
def novo_rpd(request):
    if request.method == 'POST':
        form = RPDForm(request.POST)
        if form.is_valid():
            rpd = form.save(commit=False)
            rpd.paciente = request.user
            if hasattr(request.user, 'vinculo') and request.user.vinculo.ativo:
                rpd.profissional = request.user.vinculo.profissional
            rpd.save()
            return redirect('listar_rpds')
    else:
        form = RPDForm()
    return render(request, 'registros/novo_rpd.html', {'form': form})

@login_required
@paciente_required
def listar_rpds(request):
    rpds = RPD.objects.filter(paciente=request.user).order_by('-data_criacao')
    return render(request, 'registros/listar_rpds.html', {'rpds': rpds})

@login_required
@paciente_required
def detalhar_rpd(request, rpd_id):
    rpd = get_object_or_404(RPD, id=rpd_id, paciente=request.user)
    return render(request, 'registros/detalhar_rpd.html', {'rpd': rpd})

@login_required
@paciente_required
def editar_rpd(request, rpd_id):
    rpd = get_object_or_404(RPD, id=rpd_id, paciente=request.user)
    if request.method == 'POST':
        form = RPDForm(request.POST, instance=rpd)
        if form.is_valid():
            form.save()
            return redirect('listar_rpds')
    else:
        form = RPDForm(instance=rpd)
    return render(request, 'registros/editar_rpd.html', {'form': form})

@login_required
@paciente_required
def excluir_rpd(request, rpd_id):
    rpd = get_object_or_404(RPD, id=rpd_id, paciente=request.user)
    if request.method == 'POST':
        rpd.delete()
        return redirect('listar_rpds')
    return render(request, 'registros/listar_rpds.html', {'rpd': rpd})

@login_required
@profissional_required
def listar_rpds_paciente(request, paciente_id):
    from apps.pacientes.models import Vinculo
    vinculo = get_object_or_404(Vinculo, paciente__id=paciente_id, profissional=request.user, ativo=True)
    paciente = vinculo.paciente

    rpds = RPD.objects.filter(paciente=paciente).order_by('-data_criacao')

    context = {
        'rpds': rpds,
        'paciente': paciente,
    }
    return render(request, 'registros/listar_rpds_profissional.html', context)

@login_required
@profissional_required
def detalhar_rpd_profissional(request, rpd_id):
    from apps.pacientes.models import Vinculo
    rpd = get_object_or_404(RPD, id=rpd_id)
    if not Vinculo.objects.filter(paciente=rpd.paciente, profissional=request.user, ativo=True).exists():
        return redirect('lista_pacientes')
    return render(request, 'registros/detalhar_rpd_profissional.html', {'rpd': rpd})

@login_required
@paciente_required
def registrar_humor(request):
    if request.method == 'POST':
        form = RegistroHumorForm(request.POST)
        if form.is_valid():
            humor = form.save(commit=False)
            humor.paciente = request.user
            humor.save()
            return redirect('tarefas_paciente')
    else:
        form = RegistroHumorForm(initial={'data_humor': timezone.now()})
    return render(request, 'registros/registrar_humor.html', {'form': form})


@login_required
@paciente_required
def listar_humores(request):
    humores = RegistroHumor.objects.filter(paciente=request.user).order_by('-data_humor')
    return render(request, 'registros/listar_humores.html', {'humores': humores})

@login_required
@profissional_required
def listar_humores_paciente(request, paciente_id):
    from apps.pacientes.models import Vinculo
    vinculo = get_object_or_404(Vinculo, paciente__id=paciente_id, profissional=request.user, ativo=True)
    paciente = vinculo.paciente

    humores = RegistroHumor.objects.filter(paciente=paciente).order_by('-data_humor')

    context = {
        'humores': humores,
        'paciente': paciente,
    }
    return render(request, 'registros/listar_humores_profissional.html', context)

@login_required
@profissional_required
def editar_anotacao_geral(request, paciente_id):
    from apps.pacientes.models import Vinculo
    paciente_vinculado = get_object_or_404(Vinculo, paciente__id=paciente_id, profissional=request.user, ativo=True)
    paciente = paciente_vinculado.paciente

    anotacao, _ = AnotacaoGeral.objects.get_or_create(
        paciente=paciente,
        defaults={'profissional': request.user}
    )

    if request.method == 'POST':
        form = AnotacaoGeralForm(request.POST, instance=anotacao)
        if form.is_valid():
            form.save()
            return redirect('editar_anotacao_geral', paciente_id=paciente.id)
    else:
        form = AnotacaoGeralForm(instance=anotacao)

    return render(request, 'registros/anotacao_geral.html', {
        'form': form,
        'paciente': paciente,
    })

@login_required
@profissional_required
def nova_anotacao_consulta(request, paciente_id):
    from apps.pacientes.models import Vinculo
    vinculo = get_object_or_404(Vinculo, paciente__id=paciente_id, profissional=request.user, ativo=True)
    paciente = vinculo.paciente

    if request.method == 'POST':
        form = AnotacaoConsultaForm(request.POST)
        if form.is_valid():
            anotacao = form.save(commit=False)
            anotacao.paciente = paciente
            anotacao.profissional = request.user
            anotacao.save()
            return redirect('listar_anotacoes_paciente', paciente_id=paciente.id)
    else:
        form = AnotacaoConsultaForm()

    return render(request, 'registros/nova_anotacao_consulta.html', {
        'form': form,
        'paciente': paciente
    })


@login_required
@profissional_required
def listar_anotacoes_paciente(request, paciente_id):
    from apps.pacientes.models import Vinculo
    vinculo = get_object_or_404(Vinculo, paciente__id=paciente_id, profissional=request.user, ativo=True)
    paciente = vinculo.paciente

    query = request.GET.get('q', '')

    anotacao_geral = getattr(paciente, 'anotacao_geral', None)
    if query and anotacao_geral and query.lower() not in anotacao_geral.conteudo.lower():
        anotacao_geral = None

    anotacoes_consulta = paciente.anotacoes_consulta_paciente.all().order_by('-data_consulta')
    if query:
        anotacoes_consulta = anotacoes_consulta.filter(conteudo__icontains=query)

    contexto = {
        'paciente': paciente,
        'anotacao_geral': anotacao_geral,
        'anotacoes_consulta': anotacoes_consulta,
    }

    return render(request, 'registros/listar_anotacoes.html', contexto)


@login_required
@profissional_required
def editar_anotacao_consulta(request, anotacao_id):
    from apps.pacientes.models import Vinculo
    anotacao = get_object_or_404(AnotacaoConsulta, id=anotacao_id)
    vinculo = get_object_or_404(Vinculo, paciente=anotacao.paciente, profissional=request.user, ativo=True)
    paciente = vinculo.paciente

    if request.method == 'POST':
        form = AnotacaoConsultaForm(request.POST, instance=anotacao)
        if form.is_valid():
            form.save()
            return redirect('listar_anotacoes_paciente', paciente_id=paciente.id)
    else:
        form = AnotacaoConsultaForm(instance=anotacao)

    return render(request, 'registros/editar_anotacao_consulta.html', {
        'form': form,
        'anotacao': anotacao,
        'paciente': paciente,
        'somente_leitura': False 
    })
