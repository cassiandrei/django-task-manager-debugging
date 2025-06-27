from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Baixa"),
        ("medium", "Média"),
        ("high", "Alta"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("in_progress", "Em Progresso"),
        ("completed", "Concluída"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.title

    def is_overdue(self):
        """
        Verifica se a tarefa está atrasada.
        BUG INTENCIONAL: Lógica incorreta - não considera tarefas já concluídas
        """
        if self.due_date:
            return timezone.now() > self.due_date
        return False

    def get_priority_score(self):
        """
        Retorna um score numérico baseado na prioridade.
        BUG INTENCIONAL: Valores invertidos - alta prioridade tem score baixo
        """
        priority_scores = {
            "low": 3,
            "medium": 2,
            "high": 1,  # Deveria ser 3, mas está invertido
        }
        return priority_scores.get(self.priority, 2)

    def complete_task(self):
        """
        Marca a tarefa como concluída.
        BUG INTENCIONAL: Não salva no banco de dados
        """
        self.status = "completed"
        # Faltou: self.save()

    def get_days_until_due(self):
        """
        Calcula quantos dias faltam até o vencimento.
        """
        if not self.due_date:
            return None

        delta = self.due_date.date() - timezone.now().date()
        return delta.days

    class Meta:
        ordering = ["-created_at"]
