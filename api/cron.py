"""
Cron job for checking ended auctions and notifying winners.
"""

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Item, Bid


def check_ended_auctions() -> None:
    """
    Check for auctions that have ended and notify the winners via email.
    
    This function is called by django-crontab every 5 minutes.
    """
    # Find all items where auction has ended but winner hasn't been notified
    ended_items = Item.objects.filter(
        end_datetime__lte=timezone.now(),
        winner_notified=False
    ).select_related('owner')
    
    for item in ended_items:
        # Get the highest bid
        highest_bid: Bid | None = item.bids.select_related('bidder').order_by('-amount').first()
        
        if highest_bid:
            # Send email to the winner
            winner = highest_bid.bidder
            try:
                send_mail(
                    subject=f'🎉 Congratulations! You won the auction for "{item.title}"',
                    message=f'''
Dear {winner.username},

Congratulations! You have won the auction for "{item.title}" with your bid of £{highest_bid.amount}.

Please contact the seller ({item.owner.username}) to arrange payment and delivery.

Seller's email: {item.owner.email}

Thank you for using our auction platform!

Best regards,
The Auction Team
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[winner.email],
                    fail_silently=False,
                )
                print(f"[CRON] Sent winner notification to {winner.email} for item '{item.title}'")
            except Exception as e:
                print(f"[CRON] Failed to send email to {winner.email}: {e}")
                continue  # Don't mark as notified if email failed
            
            # Also notify the seller
            try:
                send_mail(
                    subject=f'Your auction for "{item.title}" has ended',
                    message=f'''
Dear {item.owner.username},

Your auction for "{item.title}" has ended.

The winning bid was £{highest_bid.amount} by {winner.username}.

Winner's email: {winner.email}

Please contact the winner to arrange payment and delivery.

Thank you for using our auction platform!

Best regards,
The Auction Team
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[item.owner.email],
                    fail_silently=False,
                )
                print(f"[CRON] Sent seller notification to {item.owner.email} for item '{item.title}'")
            except Exception as e:
                print(f"[CRON] Failed to send seller email to {item.owner.email}: {e}")
        else:
            print(f"[CRON] No bids for item '{item.title}' - no winner to notify")
        
        # Mark as notified (even if no bids, to avoid re-processing)
        item.winner_notified = True
        item.save()
