def xsrf_exempt():

    def decorator(func):
        func._dont_enforce_csrf_checks = True
        return func

    return decorator
