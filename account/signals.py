from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from account.models import Profile


# 유저가 회원가입할 때마다 실행되는 함수
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 유저가 DB에 저장될 때마다 프로필 사진을 default로 설정
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

