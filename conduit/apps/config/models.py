from django.db import models
#from jsonfield import JSONField,JSONCharField
#from django.contrib.postgres.fields import JSONField

# Create your models here.class Bucketlist(models.Model):
class Config(models.Model):
    """This class represents the bucketlist model."""
    name = models.CharField(max_length=25, blank=False, null=False,unique=True)
    content = models.JSONField(null=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
