from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.db.models import Q, Case, When


User = get_user_model() 

# Discussions

class Discussion(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    # profile_link = models.URLField(max_length=250, blank=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        abstract = True


class Course(Discussion):
    pass


class Job(Discussion):
    pass


class Professor(Discussion):
    profile_link = models.URLField(max_length=250, blank=True)
    courses = models.ManyToManyField(Course)
    image = models.ImageField(
        'Image',
        upload_to='discussions/',
        blank=True
    )


# User Records

class Record(models.Model):
    title = models.CharField(max_length=200, blank=True)
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.title + '|' + self.author.username


class Post(Record):
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=Case(
    #                 When(Q(professor__isnull=False), then=1),
    #                 When(Q(course__isnull=False), then=1),
    #                 When(Q(job__isnull=False), then=1),
    #                 output_field=models.IntegerField(),
    #             ) == 1,
    #             name='only_one_field_filled'
    #         )
    #     ]

    def clean(self):
        cleaned_data = super().clean()
        if (self.professor and self.course) or (
            self.course and self.job) or (self.job and self.professor):
            raise ValidationError('A post can only belong to one discussion.')
        if not self.professor and not self.course and not self.job:
            raise ValidationError('A post must belong to a discussion.')
        return cleaned_data
        
    def average_rating(self):
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"]


class Comment(Record):
    post = models.ForeignKey(
        Post, 
        on_delete=models.SET_NULL, 
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class Vacancy(Record):
    company = models.CharField(max_length=100)
    link = models.URLField(max_length=250,
        null=True,
        blank=True)
    job = models.ForeignKey(Job, 
        on_delete=models.CASCADE,
        related_name='vacancies',
        null=True,
        blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vacancies'
    )
# Ratings and approvals

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    def __str__(self):
        return f"{self.post.title}: {self.rating}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'], name='unique_follow'
            )
        ]

class Approval(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='approves'
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='approved',
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'professor'], name='unique_approval'
            )
        ]