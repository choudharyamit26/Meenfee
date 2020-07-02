from modeltranslation.translator import register, TranslationOptions
from .models import User

@register(User)

class UserTranslationOptions(TranslationOptions):
	fields = ('first_name','last_name')

@register(QuestionFilledByAdmin)

class QuestionFilledByAdminTranslationOptions(TranslationOptions):
	fields = ('question_for_provider','question_for_requestor')
