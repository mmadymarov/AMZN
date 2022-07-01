
class Wrapit():

    "Wrapit class to hold decorator functions"
    def _exceptionHandler(f):
        "Decorator to handle exceptions"
        def inner(*args,**kwargs):
            try:
                return f(*args,**kwargs)
            except Exception as e:
                args[0].write('You have this exception')
                args[0].write('Exception in method: %s'%str(f.__name__))
                args[0].write('PYTHON SAYS: %s'%str(e))
                #we denote None as failure case
                return None

        return inner
    
    _exceptionHandler = staticmethod(_exceptionHandler)
