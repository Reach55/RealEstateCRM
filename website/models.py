from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    photo = models.ImageField(upload_to='team/')
    bio = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('display_order', 'name')

    def __str__(self):
        return f'{self.name} — {self.role}'
