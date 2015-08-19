from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save

class Profile(BaseModel):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to = 'profile_pics', max_length = 100, default='profile_pics/default_user.jpg')
	institute = models.CharField(max_length=200, blank=True)
	course = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return self.user.username

	def delete(self, *args, **kwargs):
		self.user.delete()
		return super(Profile, self).delete(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender = User)
