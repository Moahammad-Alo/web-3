"""
Serialization helpers for converting Django models to JSON-compatible dictionaries.
"""

from typing import Any, Optional
from decimal import Decimal
from django.conf import settings
from .models import User, Item, Bid, Question, Answer


def get_image_url(image_field) -> Optional[str]:
    """Helper to get absolute URL for image fields."""
    if not image_field:
        return None
    try:
        # If image has a URL (properly uploaded file)
        return f"http://localhost:8000{image_field.url}"
    except (ValueError, AttributeError):
        # Fallback for string paths
        if isinstance(image_field, str):
            return f"http://localhost:8000{settings.MEDIA_URL}{image_field}"
        return None


def serialize_user(user: User) -> dict[str, Any]:
    """Serialize a User model instance to a dictionary."""
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
        'profile_image': get_image_url(user.profile_image),
    }


def serialize_user_minimal(user: User) -> dict[str, Any]:
    """Serialize minimal user info for embedding in other objects."""
    return {
        'id': user.id,
        'username': user.username,
        'profile_image': get_image_url(user.profile_image),
    }


def serialize_bid(bid: Bid) -> dict[str, Any]:
    """Serialize a Bid model instance to a dictionary."""
    return {
        'id': bid.id,
        'item_id': bid.item.id,
        'bidder': serialize_user_minimal(bid.bidder),
        'amount': str(bid.amount),
        'timestamp': bid.timestamp.isoformat(),
    }


def serialize_answer(answer: Answer) -> dict[str, Any]:
    """Serialize an Answer model instance to a dictionary."""
    return {
        'id': answer.id,
        'question_id': answer.question.id,
        'responder': serialize_user_minimal(answer.responder),
        'text': answer.text,
        'timestamp': answer.timestamp.isoformat(),
    }


def serialize_question(question: Question, include_answers: bool = True) -> dict[str, Any]:
    """Serialize a Question model instance to a dictionary."""
    data: dict[str, Any] = {
        'id': question.id,
        'item_id': question.item.id,
        'asker': serialize_user_minimal(question.asker),
        'text': question.text,
        'timestamp': question.timestamp.isoformat(),
    }
    if include_answers:
        data['answers'] = [serialize_answer(a) for a in question.answers.all()]
    return data


def serialize_item(item: Item, include_details: bool = False) -> dict[str, Any]:
    """
    Serialize an Item model instance to a dictionary.
    
    Args:
        item: The Item instance to serialize
        include_details: If True, include bids and questions (for detail view)
    """
    highest_bid = item.bids.order_by('-amount').first()
    
    data: dict[str, Any] = {
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'starting_price': str(item.starting_price),
        'current_price': str(highest_bid.amount if highest_bid else item.starting_price),
        'image': get_image_url(item.image),
        'end_datetime': item.end_datetime.isoformat(),
        'owner': serialize_user_minimal(item.owner),
        'bid_count': item.bids.count(),
        'is_active': item.is_active,
        'created_at': item.created_at.isoformat(),
    }
    
    if include_details:
        data['bids'] = [serialize_bid(b) for b in item.bids.all()[:10]]  # Latest 10 bids
        data['questions'] = [serialize_question(q) for q in item.questions.all()]
        data['highest_bidder'] = serialize_user_minimal(highest_bid.bidder) if highest_bid else None
    
    return data


def serialize_items_list(items: list[Item]) -> list[dict[str, Any]]:
    """Serialize a list of Item instances."""
    return [serialize_item(item) for item in items]
