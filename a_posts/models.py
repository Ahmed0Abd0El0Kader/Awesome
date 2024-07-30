from django.db import models
import uuid

class Post(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=500,null=True)
    url = models.URLField(max_length=500,null=True)
    image = models.URLField(max_length=500)
    body = models.TextField()
    tags = models.ManyToManyField('Tag')
    created = models.DateTimeField(auto_now_add=True)
    id  = models.CharField(max_length=100,default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']
        
        
class Tag(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='icons/',null=True,blank=True)
    slug = models.SlugField(max_length=100,unique=True)
    order = models.IntegerField(null=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name       
    
        