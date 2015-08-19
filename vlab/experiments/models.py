from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel


class Experiment(BaseModel):
	name = models.CharField(max_length=200, unique = True)
	lang = models.CharField(max_length=200)
	visit_count = models.IntegerField(default=0)
	completed_count = models.IntegerField(default=0)
	prescribed_time = models.IntegerField(default=0)
	max_score = models.IntegerField(default=0)

	def __unicode__(self):
		return '%s, %s, %s' %(self.lab_category, self.lang, self.name)


class ExperimentStage(BaseModel):
	experiment = models.ForeignKey(Experiment)
	name = models.CharField(max_length=200)
	visit_count = models.IntegerField(default=0)
	completed_count = models.IntegerField(default=0)
	prescribed_time = models.IntegerField(default=0)
	max_score = models.IntegerField()

	def __unicode__(self):
		return '%s, %s' %(self.experiment.name, self.name)

	def save(self, *args, **kwargs):
		if not self.id:
			experiment = self.experiment
			experiment.prescribed_time += self.prescribed_time
			experiment.max_score += self.max_score
		return super(Profile, self).save(*args, **kwargs)


class Participant(BaseModel):
	MODE = (('free style','test mode'),)

	user = models.ForeignKey(User)
	experiment = models.ForeignKey(Experiment)
	time = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	mode =  models.CharField(max_length=10, choices=MODE)

	def __unicode__(self):
		return '%s, %s, %s' %(self.user.username, self.experiment.name, self.mode)


class ParticipantStage(BaseModel):
	participant = models.ForeignKey(Participant)
	stage = models.ForeignKey(ExperimentStage)
	time = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	attempts = models.IntegerField(default=0)

	def __unicode__(self):
		return '%s, %s, %s' %(self.participant.user.username, self.stage.experiment.name, self.stage.name)
