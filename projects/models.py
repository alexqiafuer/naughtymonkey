import uuid

from django.db import models
from users.models import Profile


class Project(models.Model):
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title', '-created']

    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, upload_to='projects/', default='projects/default.JPG', )
    demo_link = models.CharField(max_length=250, null=True, blank=True)
    source_link = models.CharField(max_length=250, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title


    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url


    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)

        return set(queryset)


    @property
    def updateVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up')
        vote_total = reviews.count()
        vote_ratio = (upVotes.count() / vote_total) * 100 if vote_total > 0 else 0

        self.vote_total = vote_total
        self.vote_ratio = vote_ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    class Meta:
        unique_together = [['owner', 'project']]


    def __str__(self) -> str:
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.name
