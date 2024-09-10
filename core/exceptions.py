from django.core.exceptions import ValidationError

class ErrorSavingModel(ValidationError):
    pass
