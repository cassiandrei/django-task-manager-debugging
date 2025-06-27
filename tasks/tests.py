from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task


class TaskModelTests(TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_task_creation(self):
        """Testa se uma tarefa pode ser criada corretamente."""
        task = Task.objects.create(
            title="Tarefa de Teste",
            description="Descrição da tarefa de teste",
            priority="high",
            assigned_to=self.user,
        )

        self.assertEqual(task.title, "Tarefa de Teste")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.assigned_to, self.user)
        self.assertEqual(str(task), "Tarefa de Teste")

    def test_is_overdue_for_completed_task(self):
        """
        TESTE FALHA: Testa se tarefas concluídas não são consideradas atrasadas.
        BUG: O método is_overdue() não verifica se a tarefa já foi concluída.
        """
        # Cria uma tarefa com data de vencimento no passado
        past_date = timezone.now() - timedelta(days=1)
        task = Task.objects.create(
            title="Tarefa Atrasada mas Concluída",
            priority="medium",
            due_date=past_date,
            status="completed",  # Tarefa já concluída
            assigned_to=self.user,
        )

        # Uma tarefa concluída NÃO deveria ser considerada atrasada
        self.assertFalse(
            task.is_overdue(),
            "Tarefas concluídas não deveriam ser consideradas atrasadas",
        )

    def test_priority_score_order(self):
        """
        TESTE FALHA: Testa se os scores de prioridade estão corretos.
        BUG: Os valores de score estão invertidos - alta prioridade tem score baixo.
        """
        task_high = Task.objects.create(
            title="Alta Prioridade", priority="high", assigned_to=self.user
        )

        task_medium = Task.objects.create(
            title="Média Prioridade", priority="medium", assigned_to=self.user
        )

        task_low = Task.objects.create(
            title="Baixa Prioridade", priority="low", assigned_to=self.user
        )

        # Alta prioridade deveria ter o MAIOR score
        self.assertGreater(
            task_high.get_priority_score(),
            task_medium.get_priority_score(),
            "Tarefa de alta prioridade deveria ter score maior que média",
        )
        self.assertGreater(
            task_medium.get_priority_score(),
            task_low.get_priority_score(),
            "Tarefa de média prioridade deveria ter score maior que baixa",
        )

        # Valores esperados
        self.assertEqual(
            task_high.get_priority_score(), 3, "Alta prioridade deveria ter score 3"
        )
        self.assertEqual(
            task_medium.get_priority_score(), 2, "Média prioridade deveria ter score 2"
        )
        self.assertEqual(
            task_low.get_priority_score(), 1, "Baixa prioridade deveria ter score 1"
        )

    def test_complete_task_saves_to_database(self):
        """
        TESTE FALHA: Testa se o método complete_task() salva a alteração no banco.
        BUG: O método complete_task() não chama save(), então a mudança não persiste.
        """
        task = Task.objects.create(
            title="Tarefa para Completar", priority="medium", assigned_to=self.user
        )

        # Estado inicial
        self.assertEqual(task.status, "pending")

        # Chama o método para completar
        task.complete_task()

        # Recarrega do banco de dados
        task.refresh_from_db()

        # Deveria estar marcada como concluída no banco
        self.assertEqual(
            task.status,
            "completed",
            "Tarefa deveria estar marcada como concluída no banco de dados",
        )

    def test_get_days_until_due(self):
        """Testa o cálculo de dias até o vencimento (este método está correto)."""
        # Tarefa com vencimento em 5 dias
        future_date = timezone.now() + timedelta(days=5)
        task = Task.objects.create(
            title="Tarefa Futura", due_date=future_date, assigned_to=self.user
        )

        self.assertEqual(task.get_days_until_due(), 5)

        # Tarefa sem data de vencimento
        task_no_due = Task.objects.create(title="Sem Vencimento", assigned_to=self.user)

        self.assertIsNone(task_no_due.get_days_until_due())


class TaskViewTests(TestCase):
    def setUp(self):
        """Configuração inicial para os testes de views."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_complete_task_view_persistence(self):
        """
        TESTE RELACIONADO: Testa se a view de completar tarefa funciona corretamente.
        Este teste vai falhar porque usa o método complete_task() bugado.
        """
        task = Task.objects.create(
            title="Tarefa para Completar via View",
            priority="low",
            assigned_to=self.user,
        )

        # Chama a view para completar a tarefa
        response = self.client.get(reverse("complete_task", args=[task.id]))

        # Deveria redirecionar
        self.assertEqual(response.status_code, 302)

        # Recarrega a tarefa do banco
        task.refresh_from_db()

        # Tarefa deveria estar concluída
        self.assertEqual(
            task.status,
            "completed",
            "Tarefa deveria estar concluída após chamar a view",
        )

    def test_overdue_tasks_api_excludes_completed(self):
        """
        TESTE RELACIONADO: Testa se a API de tarefas atrasadas não inclui concluídas.
        """
        # Tarefa atrasada mas concluída
        past_date = timezone.now() - timedelta(days=2)
        completed_task = Task.objects.create(
            title="Atrasada mas Concluída",
            due_date=past_date,
            status="completed",
            assigned_to=self.user,
        )

        # Tarefa atrasada e pendente
        pending_task = Task.objects.create(
            title="Atrasada e Pendente",
            due_date=past_date,
            status="pending",
            assigned_to=self.user,
        )

        response = self.client.get(reverse("get_overdue_tasks"))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        overdue_tasks = data["overdue_tasks"]

        # Deveria ter apenas 1 tarefa (a pendente)
        self.assertEqual(
            len(overdue_tasks),
            1,
            "Apenas tarefas pendentes deveriam aparecer como atrasadas",
        )
        self.assertEqual(overdue_tasks[0]["title"], "Atrasada e Pendente")

    def test_tasks_by_priority_correct_order(self):
        """
        TESTE RELACIONADO: Testa se a ordenação por prioridade está correta.
        """
        # Cria tarefas com diferentes prioridades
        Task.objects.create(title="Alta", priority="high", assigned_to=self.user)
        Task.objects.create(title="Baixa", priority="low", assigned_to=self.user)
        Task.objects.create(title="Média", priority="medium", assigned_to=self.user)

        response = self.client.get(reverse("get_tasks_by_priority"))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        tasks = data["tasks"]

        # Primeira tarefa deveria ser de alta prioridade
        self.assertEqual(
            tasks[0]["priority"],
            "high",
            "Primeira tarefa deveria ser de alta prioridade",
        )

        # Verificar se está ordenado corretamente por score
        scores = [task["priority_score"] for task in tasks]
        self.assertEqual(
            scores,
            sorted(scores, reverse=True),
            "Tarefas deveriam estar ordenadas por score decrescente",
        )


class TaskIntegrationTests(TestCase):
    """Testes de integração que verificam o comportamento completo."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="integrationuser", password="testpass123"
        )
        self.client.login(username="integrationuser", password="testpass123")

    def test_workflow_create_and_complete_task(self):
        """
        Testa o fluxo completo: criar → completar → verificar persistência.
        Este teste vai detectar o bug de persistência na conclusão.
        """
        # 1. Criar tarefa via POST
        response = self.client.post(
            reverse("create_task"),
            {
                "title": "Tarefa de Integração",
                "description": "Teste completo",
                "priority": "high",
            },
        )

        self.assertEqual(response.status_code, 302)  # Redirect após criar

        # 2. Verificar se foi criada
        task = Task.objects.get(title="Tarefa de Integração")
        self.assertEqual(task.status, "pending")

        # 3. Completar via view
        response = self.client.get(reverse("complete_task", args=[task.id]))
        self.assertEqual(response.status_code, 302)  # Redirect após completar

        # 4. Verificar se persiste como concluída
        task.refresh_from_db()
        self.assertEqual(
            task.status,
            "completed",
            "Tarefa deveria permanecer concluída após reload da página",
        )
