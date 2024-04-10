from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users_photo/', blank=True)

    def __str__(self) -> str:
        return f'Profile of {self.user.username}'
    

class Subscribe(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rel_from')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rel_to')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=('-created',)),
        ]
        ordering = ['-created']

    def __str__(self) -> str:
        return f'{self.user_from} following on {self.user_to}'

user = get_user_model()

user.add_to_class('following',  models.ManyToManyField(
                                            'self', 
                                            through=Subscribe, 
                                            related_name='followers',
                                            symmetrical=False
                                        )
)