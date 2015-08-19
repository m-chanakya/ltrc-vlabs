import urllib2
import json
from django.core.files.base import ContentFile

def update_avatar(backend, response, is_new=False, user=None, *args, **kwargs):
	if user and is_new:
		if backend.name == 'facebook':
			url = "https://graph.facebook.com/%s/picture?redirect=false" % response['id']
			avatar = urllib2.urlopen(url)
			is_silhouette = json.loads(avatar.read()).get('data')['is_silhouette']
			if not is_silhouette:
				url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
				avatar = urllib2.urlopen(url)
				profile = user.profile
				profile.avatar.save(str(user.id) + '.jpg', ContentFile(avatar.read()))
				profile.save()
