"""
Representa as aplicações em taxas e descontos
"""

NOT_FINISHED = 0
AUTHORIZED = 1
PAYMENT_CONFIRMED = 2
DENIED = 3
VOIDED = 10
REFUNDED = 11
PENDING = 12
ABORTED = 13
SCHEDULED = 20

CHOICES = (
    (NOT_FINISHED, 'NOT_FINISHED'),
    (AUTHORIZED, 'AUTHORIZED'),
    (PAYMENT_CONFIRMED, 'PAYMENT_CONFIRMED'),
    (DENIED, 'DENIED'),
    (VOIDED, 'VOIDED'),
    (REFUNDED, 'REFUNDED'),
    (PENDING, 'PENDING'),
    (ABORTED, 'ABORTED'),
    (SCHEDULED, 'SCHEDULED')
)
