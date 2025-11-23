from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import InformacoesAdicionais, ContatosEmergencia

def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':

        # Verifica se o usuário é válido
        email_form = request.POST.get('email')
        senha_form = request.POST.get('senha')
        usuario = authenticate(request, username=email_form, password=senha_form)

        if usuario is not None:
            login(request, usuario)
            return redirect('visualizar')
        else: # Cai aqui quando o usuário ou senha estão incorretos / não estão registrados no Banco de dados
            messages.error(request, "E-mail ou senha incorreta!")
            return render(request, 'login.html', { 'email_form' : email_form })

def cadastrar(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':

        # Validação para aceitar somente campos preenchidos(o strip garante que não será enganado com espaços antes e depois)
        nomeCompleto_form = request.POST.get('nomeCompleto', '').strip()
        email_form = request.POST.get('email', '').strip()
        senha_form = request.POST.get('senha', '').strip()
        if not nomeCompleto_form or not email_form or not senha_form:
            messages.error(request, "Preencha todos os campos corretamente!")
            return render(request, "cadastro.html", { "nomeCompleto_form" : nomeCompleto_form, "email_form" : email_form, "senha_form" : senha_form })

        # Verifica se o email digitado já existe no banco, caso exista irá aparecer uma mensagem de erro
        if User.objects.filter(username=email_form).exists():
            messages.error(request, "Este e-mail já está em uso. Tente outro.")
            return render(request, 'cadastro.html')

        User.objects.create_user(
            first_name = nomeCompleto_form,
            username = email_form,
            password = senha_form,
        )

        return redirect('login')

@login_required(login_url='login')
def visualizar(request):
    return render(request, 'visualizarInformacoes.html')

@login_required(login_url='login')
def editar(request):
    if request.method == 'GET':
        return render(request, 'informacoesAdicionais.html')
    elif request.method == 'POST':
        usuario = request.user
        info, created = InformacoesAdicionais.objects.get_or_create(user=usuario)
        contato, created = ContatosEmergencia.objects.get_or_create(informacoes=info)
        acao = request.POST.get('acao')

        if acao == "excluir":

            # Exclui os dados vinculados de InformacoesAdicionais (se houver)
            if hasattr(usuario, "informacoesadicionais"):

                # Caso tenha ContatosEmergencia vinculado será excluído
                if hasattr(usuario.informacoesadicionais, "contatosemergencia"):
                    usuario.informacoesadicionais.contatosemergencia.delete()

                usuario.informacoesadicionais.delete()

            # Exclui o próprio usuário
            usuario.delete()

            # Desloga
            logout(request)

            # Volta para a página de login
            return redirect('login')
            
        elif acao == "salvar":

            # Atualiza auth_user
            usuario.first_name = request.POST.get('nomeCompleto')
            usuario.username = request.POST.get('email')
            usuario.save()

            # Atualiza InformacoesAdicionais
            info.cpf = request.POST.get('cpf')
            info.telefone = request.POST.get('telefone')
            if request.POST.get('dataNascimento'):
                info.dataNascimento = request.POST.get('dataNascimento')
            else:
                info.dataNascimento = None
            info.tipoSanguineo = request.POST.get('tipoSanguineo')
            info.alergiasMedicamentos = request.POST.get('alergias')
            info.restricoes = request.POST.get('restricoes')
            info.endereco = request.POST.get('endereco')
            info.save()

            contato.nomeEmergencia = request.POST.get('nomeEmergencia')
            contato.telefoneEmergencia = request.POST.get('telefoneEmergencia')
            contato.save()

            #Atualiza ContatosEmergencia
            return redirect('visualizar')

@login_required(login_url='login')
def deslogar(request):
    logout(request)
    request.session.flush()
    return redirect('login')