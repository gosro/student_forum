from django.views.generic import TemplateView, ListView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post,Comment, Professor, Approval,Rating, Course, Job, Vacancy
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .forms import PostForm, RatingForm, VacancyForm, CommentForm
from django.contrib.auth.decorators import login_required

POSTS_PER_PAGE = 12

# Объединить write functions 

def get_page_object(request, post_list, POSTS_PER_PAGE):
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

class SearchResultsView(ListView):
    model = Post
    template_name = 'discussions/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )
        return object_list

def index(request):
    post_list = Post.objects.all()[:10]
    most_discussed_professors = Professor.objects.annotate(
        num_posts=Count("posts")).order_by("-num_posts")[:3]
    most_approved_professors = Professor.objects.annotate(
       num_approvals=Count('approved')
    ).order_by("-num_approvals")[:3]
    last_vacancy = Vacancy.objects.latest('pub_date')
    rating_form = RatingForm()

    context = {
        'post_list': post_list,
        'most_discussed_professors': most_discussed_professors,
        'most_approved_professors':most_approved_professors,
        'vacancy': last_vacancy,
        'rating_form':rating_form
    }

    template = 'discussions/index.html'
    return render(request,template,context)

# Posts
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post_id)
    comment_form = CommentForm()
    rating_form = RatingForm()
    context = {
        'post': post,
        'comments': comments,
        'form': comment_form,
        'rating_form':rating_form
    }
    return render(request, 'discussions/post_detail.html', context)
# Comments

@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = Post.objects.get(id=post_id)
        comment.save()
    return redirect('discussions:post_detail', post_id=post_id)

# Professor related views

def professor_discussion(request, slug):
    professor = get_object_or_404(Professor, slug=slug)
    template = 'discussions/professor.html'
    post_list = professor.posts.all()
    page_obj = get_page_object(request, post_list, POSTS_PER_PAGE)
    post_form = PostForm()
    rating_form = RatingForm()
    courses = professor.courses.all()
    approve = (
        request.user.is_authenticated and not Approval.objects.filter(
            user=request.user,professor=professor).exists()
    )
    if request.user.is_authenticated:
        user_ratings = Rating.objects.filter(
            user=request.user,
        )
    else:
        user_ratings = None

    context = {
        'professor': professor,
        'page_obj': page_obj,
        'form': post_form,
        'rating_form': rating_form,
        'approve': approve,
        'user_ratings': user_ratings,
        'courses': courses
    }

    return render(request, template, context)


def professors_list(request):
    professor_list = Professor.objects.all()
    page_obj = get_page_object(request, professor_list, POSTS_PER_PAGE)

    context = {
        'page_obj': page_obj,
    }

    template = 'discussions/professor_list.html'

    return render(request,template,context)

def professors_search(request):
    query = request.GET.get("q")
    professor_list = Professor.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    page_obj = get_page_object(request, professor_list, POSTS_PER_PAGE)
    context = {
        'page_obj': page_obj,
    }

    template = 'discussions/professor_list.html'

    return render(request,template,context)


def professors_rating(request,slug):

    if slug == 'postnum':
        professor_list = Professor.objects.annotate(
            num_posts=Count("posts"),
        ).order_by("-num_posts")
        rating_parameter = 'количество постов'

    if slug == 'approvalsnum':
        professor_list = Professor.objects.annotate(
            num_approvals=Count('approved')
        ).order_by("-num_approvals")
        rating_parameter = 'количество одобрений'


    context = {
        'professor_list': professor_list,
        'rating_parameter':rating_parameter
    }
    
    template = 'discussions/professor_rating.html'
    return render(request,template,context)

@login_required
def professor_write(request,slug):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.professor = Professor.objects.get(slug=slug)
        post.save()
    return redirect('discussions:professor', slug=slug)

@login_required
def professor_approve(request,slug):
    user = request.user
    professor = Professor.objects.get(slug=slug)
    if not user.approves.filter(professor=professor).exists():
        Approval.objects.create(
            professor=professor,
            user=user
        )
    return redirect('discussions:professor', slug=slug)

@login_required
def professor_disapprove(request,slug):
    user = request.user
    professor = Professor.objects.get(slug=slug)
    approval = professor.approved.filter(user=user)
    approval.delete()
    return redirect('discussions:professor', slug=slug)

# Post related views
@login_required
def post_rate(request,post_id):
    form = RatingForm(request.POST)

    if form.is_valid() and not Rating.objects.filter(
        user=request.user, post=Post.objects.get(id=post_id)
    ).exists():
        rating = form.save(commit=False)
        rating.user = request.user
        rating.post = Post.objects.get(id=post_id)
        rating.save()

    elif form.is_valid() and Rating.objects.filter(
        user=request.user, post=Post.objects.get(id=post_id)
    ).exists():
        Rating.objects.get(
            user=request.user, post=Post.objects.get(id=post_id)
        ).delete()
        rating = form.save(commit=False)
        rating.user = request.user
        rating.post = Post.objects.get(id=post_id)
        rating.save()
    return redirect('discussions:post_detail', post_id=rating.post.id)

# Course related views

def course_discussion(request, slug):
    course = get_object_or_404(Course, slug=slug)
    template = 'discussions/course.html'
    post_list = course.posts.all()
    page_obj = get_page_object(request, post_list, POSTS_PER_PAGE)
    post_form = PostForm()
    rating_form = RatingForm()
    professors =  course.professor_set.all()
    if request.user.is_authenticated:
        user_ratings = Rating.objects.filter(
            user=request.user,
        )
    else:
        user_ratings = None

    context = {
        'course': course,
        'page_obj': page_obj,
        'form': post_form,
        'rating_form': rating_form,
        'user_ratings': user_ratings,
        'professors': professors
    }

    return render(request, template, context)

@login_required
def course_write(request,slug):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.course = Course.objects.get(slug=slug)
        post.save()
    return redirect('discussions:course', slug=slug)

def courses_list(request):
    courses_list = Course.objects.all()
    page_obj = get_page_object(request, courses_list, POSTS_PER_PAGE)

    context = {
        'page_obj': page_obj,
    }

    template = 'discussions/course_list.html'

    return render(request,template,context)

def courses_search(request):
    query = request.GET.get("q")
    course_list = Course.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    page_obj = get_page_object(request, course_list, POSTS_PER_PAGE)
    context = {
        'page_obj': page_obj,
    }

    template = 'discussions/course_list.html'

    return render(request,template,context)

# Jobs
def job_discussion(request,slug):
    job = get_object_or_404(Job, slug=slug)
    template = 'discussions/job.html'
    post_list = job.posts.all()
    page_obj = get_page_object(request, post_list, POSTS_PER_PAGE)
    post_form = PostForm()
    rating_form = RatingForm()
    if request.user.is_authenticated:
        user_ratings = Rating.objects.filter(
            user=request.user,
        )
    else:
        user_ratings = None

    context = {
        'job': job,
        'page_obj': page_obj,
        'form': post_form,
        'rating_form': rating_form,
        'user_ratings': user_ratings,
    }

    return render(request, template, context)

def job_vacancies(request,slug):
    job = get_object_or_404(Job, slug=slug)
    template = 'discussions/job.html'
    vacancy_list = job.vacancies.all()
    page_obj = get_page_object(request, vacancy_list, POSTS_PER_PAGE)
    context = {
        'job': job,
        'page_obj': page_obj,
    }

    return render(request, template, context)

@login_required
def job_write(request,slug):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.job = Job.objects.get(slug=slug)
        post.save()
    return redirect('discussions:job', slug=slug)

def jobs_list(request):
    jobs_list = Job.objects.all()
    page_obj = get_page_object(request, jobs_list, POSTS_PER_PAGE)

    context = {
        'page_obj': page_obj,
    }

    template = 'discussions/jobs_list.html'

    return render(request,template,context)

# Vacancies

def vacancy_list(request):
    vacancy_list = Vacancy.objects.all()
    page_obj = get_page_object(request, vacancy_list, POSTS_PER_PAGE)
    context = {
        'page_obj': page_obj,
    }
    template = 'discussions/vacancy_list.html'

    return render(request,template,context)

@login_required
def create_vacancy(request):
    form = VacancyForm(request.POST or None)
    if form.is_valid():
        vacancy = form.save(commit=False)
        vacancy.author = request.user
        vacancy.save()
        return redirect('discussions:vacancy_list')
    return render(request, 'discussions/vacancy_create.html', {'form': form})
