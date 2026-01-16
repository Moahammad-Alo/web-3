from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal, InvalidOperation
import json
from typing import Any

from .models import User, Item, Bid, Question, Answer
from .forms import SignupForm, LoginForm
from .serializers import (
    serialize_user, serialize_item, serialize_items_list,
    serialize_bid, serialize_question, serialize_answer
)


# ============================================================================
# Template Views (Django templates for auth)
# ============================================================================

def signup_view(request: HttpRequest) -> HttpResponse:
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    
    return render(request, 'api/auth/signup.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()
    
    return render(request, 'api/auth/login.html', {'form': form})


def logout_view(request: HttpRequest) -> HttpResponse:
    """Handle user logout."""
    logout(request)
    return redirect('/login/')


@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    """Render the main Vue SPA (only for authenticated users)."""
    return render(request, 'api/spa/index.html', {})


@ensure_csrf_cookie
def get_csrf_token(request: HttpRequest) -> JsonResponse:
    """Return CSRF token for frontend to use in API requests."""
    return JsonResponse({'csrfToken': 'set'})


# ============================================================================
# API Views (JSON responses for Vue frontend)
# ============================================================================

@login_required
@require_http_methods(["GET"])
def api_user_status(request: HttpRequest) -> JsonResponse:
    """Get current user authentication status and info."""
    return JsonResponse({
        'authenticated': True,
        'user': serialize_user(request.user)
    })


@login_required
@require_http_methods(["GET", "PUT"])
def api_profile(request: HttpRequest) -> JsonResponse:
    """Get or update the current user's profile."""
    user: User = request.user
    
    if request.method == 'GET':
        return JsonResponse(serialize_user(user))
    
    # PUT - Update profile
    if request.content_type == 'application/json':
        try:
            data: dict[str, Any] = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        # Handle multipart form data (for file uploads)
        data = request.POST.dict()
    
    # Update allowed fields
    if 'email' in data:
        user.email = data['email']
    if 'date_of_birth' in data and data['date_of_birth']:
        user.date_of_birth = data['date_of_birth']
    
    # Handle profile image upload
    if 'profile_image' in request.FILES:
        user.profile_image = request.FILES['profile_image']
    
    try:
        user.save()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse(serialize_user(user))


@login_required
@require_http_methods(["GET", "POST"])
def api_items(request: HttpRequest) -> JsonResponse:
    """List all active items or create a new item."""
    if request.method == 'GET':
        # Get query parameters
        search_query: str = request.GET.get('q', '').strip()
        show_all: bool = request.GET.get('all', 'false').lower() == 'true'
        my_items: bool = request.GET.get('my', 'false').lower() == 'true'
        
        # Base queryset
        items = Item.objects.select_related('owner').prefetch_related('bids')
        
        # Filter by owner if requested
        if my_items:
            items = items.filter(owner=request.user)
        
        # Filter active items only (unless show_all)
        if not show_all:
            items = items.filter(end_datetime__gt=timezone.now())
        
        # Search by title or description
        if search_query:
            items = items.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return JsonResponse({
            'items': serialize_items_list(list(items)),
            'count': items.count()
        })
    
    # POST - Create new item
    if request.content_type and 'multipart' in request.content_type:
        data = request.POST.dict()
        image = request.FILES.get('image')
    else:
        try:
            data = json.loads(request.body)
            image = None
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validate required fields
    required_fields = ['title', 'description', 'starting_price', 'end_datetime']
    for field in required_fields:
        if field not in data or not data[field]:
            return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
    
    try:
        item = Item.objects.create(
            title=data['title'],
            description=data['description'],
            starting_price=Decimal(data['starting_price']),
            end_datetime=data['end_datetime'],
            owner=request.user,
            image=image if image else None
        )
    except (InvalidOperation, ValueError) as e:
        return JsonResponse({'error': f'Invalid data: {e}'}, status=400)
    
    return JsonResponse(serialize_item(item), status=201)


@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def api_item_detail(request: HttpRequest, item_id: int) -> JsonResponse:
    """Get, update, or delete a specific item."""
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'GET':
        return JsonResponse(serialize_item(item, include_details=True))
    
    # Only owner can update/delete
    if item.owner != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'DELETE':
        item.delete()
        return JsonResponse({'success': True})
    
    # PUT - Update item
    if request.content_type and 'multipart' in request.content_type:
        data = request.POST.dict()
        if 'image' in request.FILES:
            item.image = request.FILES['image']
    else:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Update fields
    if 'title' in data:
        item.title = data['title']
    if 'description' in data:
        item.description = data['description']
    if 'starting_price' in data:
        item.starting_price = Decimal(data['starting_price'])
    if 'end_datetime' in data:
        item.end_datetime = data['end_datetime']
    
    item.save()
    return JsonResponse(serialize_item(item, include_details=True))


@login_required
@require_http_methods(["GET", "POST"])
def api_item_bids(request: HttpRequest, item_id: int) -> JsonResponse:
    """Get bids for an item or place a new bid."""
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'GET':
        bids = item.bids.select_related('bidder').all()
        return JsonResponse({
            'bids': [serialize_bid(b) for b in bids],
            'count': bids.count()
        })
    
    # POST - Place a bid
    # Check if auction is still active
    if not item.is_active:
        return JsonResponse({'error': 'This auction has ended'}, status=400)
    
    # Can't bid on own item
    if item.owner == request.user:
        return JsonResponse({'error': 'You cannot bid on your own item'}, status=400)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if 'amount' not in data:
        return JsonResponse({'error': 'Missing amount'}, status=400)
    
    try:
        amount = Decimal(data['amount'])
    except InvalidOperation:
        return JsonResponse({'error': 'Invalid amount'}, status=400)
    
    # Validate bid is higher than current price
    current_price = item.current_price
    if amount <= current_price:
        return JsonResponse({
            'error': f'Bid must be higher than current price (£{current_price})'
        }, status=400)
    
    bid = Bid.objects.create(
        item=item,
        bidder=request.user,
        amount=amount
    )
    
    return JsonResponse(serialize_bid(bid), status=201)


@login_required
@require_http_methods(["GET", "POST"])
def api_item_questions(request: HttpRequest, item_id: int) -> JsonResponse:
    """Get questions for an item or ask a new question."""
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'GET':
        questions = item.questions.select_related('asker').prefetch_related('answers', 'answers__responder').all()
        return JsonResponse({
            'questions': [serialize_question(q) for q in questions],
            'count': questions.count()
        })
    
    # POST - Ask a question
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if 'text' not in data or not data['text'].strip():
        return JsonResponse({'error': 'Question text is required'}, status=400)
    
    question = Question.objects.create(
        item=item,
        asker=request.user,
        text=data['text'].strip()
    )
    
    return JsonResponse(serialize_question(question), status=201)


@login_required
@require_http_methods(["POST"])
def api_question_answer(request: HttpRequest, question_id: int) -> JsonResponse:
    """Post an answer to a question (only item owner can answer)."""
    question = get_object_or_404(Question, id=question_id)
    
    # Only item owner can answer
    if question.item.owner != request.user:
        return JsonResponse({'error': 'Only the item owner can answer questions'}, status=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if 'text' not in data or not data['text'].strip():
        return JsonResponse({'error': 'Answer text is required'}, status=400)
    
    answer = Answer.objects.create(
        question=question,
        responder=request.user,
        text=data['text'].strip()
    )
    
    return JsonResponse(serialize_answer(answer), status=201)
