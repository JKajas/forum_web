import os

from django.core.exceptions import ValidationError

"""
Validators checking NIP and domain
"""


def validate_NIP(NIP):
    NIP_list = list(map(int, NIP))
    ctr_w = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    if len(NIP) < 10:
        raise ValidationError("NIP is too short!")
    elif len(NIP) > 10:
        raise ValidationError("NIP is too long!")
    elif sum([x * y for x, y in zip(NIP_list, ctr_w)]) % 11 != NIP_list[9]:
        raise ValidationError("Wrong number!")


def validate_domain(domain):
    if not "www." or not ".com" or not ".pl" in domain:
        raise ValidationError("Wrong domain!")


def len_title_valid(object):
    if len(object) < 10:
        raise ValidationError("Your title should have at least 10 characters!")


def password_validator(password):
    if len(password) < 8:
        raise ValidationError(
            "Your password should have at least 8 characters"
        )
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password should have at least one digit")
