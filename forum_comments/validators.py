from django.core.exceptions import ValidationError

'''
Validators checking NIP and domain
'''

def validate_NIP(NIP):
    NIP_list = list(map(int, NIP))
    ctr_w = [6,5,7,2,3,4,5,6,7]
    if len(NIP)<10:
        raise ValidationError("NIP is too short!")
    elif len(NIP)>10:
        raise ValidationError("NIP is too long!")
    elif sum([x*y for x, y in zip(NIP_list, ctr_w)])%11 != NIP_list[9]:
        raise ValidationError('Wrong number!')
    else: print('its ok')


def validate_domain(domain):
    if not 'www.' or not '.com' or not '.pl' in domain:
        raise ValidationError('Wrong domain!')

