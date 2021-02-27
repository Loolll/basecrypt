ALPHABET = set('QAZXSWEDCVFRTGBNHYUJMKIOLPqazxswedcvfrtgbnhyujmkiolp1234567890!@#$%^&*()_+=-')


def pass_correct(password):
    """ Returns true if password is correct"""
    return type(password) is str and all([symbol in ALPHABET for symbol in password])


def wrapper_over(password):
    """ Check README (own modules) """
    return password
