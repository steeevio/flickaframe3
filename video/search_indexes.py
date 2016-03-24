import datetime
from haystack import indexes
from video.models import Vid, Tag, UserProfile, SocialGroup

class VidIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	#author = indexes.CharField(model_attr='user')
	#pub_date = indexes.DateTimeField(model_attr='pub_date')

	def get_model(self):
		return Vid

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()



class TagIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)


	def get_model(self):
		return Tag

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()


class SocialGroupIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)


	def get_model(self):
		return SocialGroup

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()				