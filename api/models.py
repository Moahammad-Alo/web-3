from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from typing import Optional


class User(AbstractUser):
    """Custom user model extending AbstractUser with additional profile fields."""
    
    profile_image: models.ImageField = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        help_text="User's profile picture"
    )
    date_of_birth: models.DateField = models.DateField(
        blank=True,
        null=True,
        help_text="User's date of birth"
    )
    # email is already included in AbstractUser but we ensure it's required
    email: models.EmailField = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return self.username


class Item(models.Model):
    """Auction item that can be bid on."""
    
    title: models.CharField = models.CharField(max_length=200)
    description: models.TextField = models.TextField()
    starting_price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Starting price for the auction"
    )
    image: models.ImageField = models.ImageField(
        upload_to='items/',
        help_text="Image of the item"
    )
    end_datetime: models.DateTimeField = models.DateTimeField(
        help_text="Date and time when the auction ends"
    )
    owner: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="User who created the auction"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    winner_notified: models.BooleanField = models.BooleanField(
        default=False,
        help_text="Whether the winner has been notified via email"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self) -> str:
        return self.title

    @property
    def is_active(self) -> bool:
        """Check if the auction is still active."""
        return timezone.now() < self.end_datetime

    @property
    def current_price(self) -> models.DecimalField:
        """Get the current highest bid or starting price."""
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            return highest_bid.amount
        return self.starting_price

    @property
    def highest_bidder(self) -> Optional['User']:
        """Get the user with the highest bid."""
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            return highest_bid.bidder
        return None


class Bid(models.Model):
    """A bid placed on an auction item."""
    
    item: models.ForeignKey = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='bids'
    )
    bidder: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bids'
    )
    amount: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount']
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'

    def __str__(self) -> str:
        return f"{self.bidder.username} bid £{self.amount} on {self.item.title}"


class Question(models.Model):
    """A question asked about an auction item."""
    
    item: models.ForeignKey = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    asker: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text: models.TextField = models.TextField(help_text="The question text")
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self) -> str:
        return f"Question by {self.asker.username} on {self.item.title}"


class Answer(models.Model):
    """An answer to a question about an auction item."""
    
    question: models.ForeignKey = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    responder: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    text: models.TextField = models.TextField(help_text="The answer text")
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self) -> str:
        return f"Answer by {self.responder.username}"
