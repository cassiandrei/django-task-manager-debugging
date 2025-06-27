from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Task


def task_list(request):
    """Lista todas as tarefas do usuário atual."""
    if request.user.is_authenticated:
        tasks = Task.objects.filter(assigned_to=request.user)
    else:
        tasks = Task.objects.none()

    context = {
        "tasks": tasks,
        "pending_count": tasks.filter(status="pending").count(),
        "completed_count": tasks.filter(status="completed").count(),
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def create_task(request):
    """Cria uma nova tarefa."""
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        priority = request.POST.get("priority", "medium")
        due_date = request.POST.get("due_date")

        if not title:
            messages.error(request, "Título é obrigatório.")
            return render(request, "tasks/create_task.html")

        task = Task.objects.create(
            title=title,
            description=description,
            priority=priority,
            assigned_to=request.user,
        )

        if due_date:
            task.due_date = due_date
            task.save()

        messages.success(request, "Tarefa criada com sucesso!")
        return redirect("task_list")

    return render(request, "tasks/create_task.html")


@login_required
def complete_task(request, task_id):
    """
    Marca uma tarefa como concluída.
    BUG INTENCIONAL: Usa o método bugado do modelo
    """
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    # Este método tem um bug - não salva no banco
    task.complete_task()

    messages.success(request, f'Tarefa "{task.title}" concluída!')
    return redirect("task_list")


def get_overdue_tasks(request):
    """
    Retorna tarefas em atraso em formato JSON.
    Esta função será testada e revelará o bug no método is_overdue()
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Usuário não autenticado"}, status=401)

    # Pegará tarefas que não deveriam estar em atraso (concluídas)
    overdue_tasks = []
    for task in Task.objects.filter(assigned_to=request.user):
        if task.is_overdue():  # Este método tem bug
            overdue_tasks.append(
                {
                    "id": task.id,
                    "title": task.title,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "status": task.status,
                    "priority": task.priority,
                }
            )

    return JsonResponse({"overdue_tasks": overdue_tasks})


def get_tasks_by_priority(request):
    """
    Lista tarefas ordenadas por prioridade (score).
    BUG será revelado: ordenação incorreta devido ao score invertido
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Usuário não autenticado"}, status=401)

    tasks = Task.objects.filter(assigned_to=request.user)

    # Ordena por priority_score (que tem valores invertidos)
    sorted_tasks = sorted(tasks, key=lambda t: t.get_priority_score(), reverse=True)

    task_list = []
    for task in sorted_tasks:
        task_list.append(
            {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "priority_score": task.get_priority_score(),
                "status": task.status,
            }
        )

    return JsonResponse({"tasks": task_list})


def login_view(request):
    """View de login simples."""
    if request.user.is_authenticated:
        return redirect("task_list")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Bem-vindo, {user.get_full_name() or user.username}!"
                )
                return redirect("task_list")
            else:
                messages.error(request, "Usuário ou senha incorretos.")
        else:
            messages.error(request, "Por favor, preencha todos os campos.")

    return render(request, "tasks/login.html")


def logout_view(request):
    """View de logout."""
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect("login")
