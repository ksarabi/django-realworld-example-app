from django.db import models

# Create your models here.class Bucketlist(models.Model):
class Template(models.Model):
    """This class represents the bucketlist model."""
    name = models.CharField(max_length=25, blank=False, null=True)
    values = models.TextField(null=False,blank=False)
    yaml = models.TextField(null=True)
    url = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
