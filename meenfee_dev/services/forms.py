from django import forms
from django.forms import ValidationError
from django.core.exceptions import ValidationError

from tinymce import TinyMCE
from .models import ContentMaster

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)


class BannerImageUploadForm(forms.Form):
    """Banner Image upload form."""
    banner_image = forms.ImageField(required=False)


class CategoryImageUploadForm(forms.Form):
    """Category Image upload form."""
    bannerimage = forms.ImageField()
    
    
class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False



class ContentFormNew(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control ', }
    ), required=True,max_length=40)

    title_in_arabic = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control ', }
    ), required=False,max_length=40)

    # main_content = forms.CharField(widget=TinyMCEWidget(
    #         attrs={'required': True, 'cols': 30, 'rows': 10}
    #     ), required=True)

    # main_content_arabic = forms.CharField(widget=TinyMCEWidget(
    #         attrs={'required': True, 'cols': 30, 'rows': 10}
    #     ), required=True)

    content = forms.CharField(widget=TinyMCEWidget(
            attrs={'required': True, 'cols': 30, 'rows': 10}
        ), required=True,max_length=30000)

    content_in_arabic = forms.CharField(widget=TinyMCEWidget(
            attrs={'required': True, 'cols': 30, 'rows': 10}
        ), required=True,max_length=30000)

    class Meta:
        model = ContentMaster
        fields = [
            'title',
            'title_in_arabic',
            # 'main_content',
            # 'main_content_arabic',
            'content',
            'content_in_arabic'
            ]





# class ContentForm(forms.ModelForm):
#     content = forms.CharField(
#         widget=TinyMCEWidget(
#             attrs={'required': False, 'cols': 30, 'rows': 10}
#         ), 
#     )
#     description = forms.CharField(widget=forms.Textarea(
#         attrs={'rows': 3,'cols':5,'class': 'form-control ', }
#     ),required=True, max_length=100)
    
#     title = forms.CharField(widget=forms.TextInput(
#         attrs={'class': 'form-control ', }
#     ), required=True,max_length=40)
    
    
    
#     content_in_arabic = forms.CharField(
#         widget=TinyMCEWidget(
#             attrs={'required': False, 'cols': 30, 'rows': 10}
#         ), required=False,
#     )
#     description_in_arabic = forms.CharField(widget=forms.Textarea(
#         attrs={'rows': 3,'cols':5,'class': 'form-control ', }
#     ), required=False, max_length=100)
    
#     title_in_arabic = forms.CharField(widget=forms.TextInput(
#         attrs={'class': 'form-control ', }
#     ), required=False,max_length=40)
    
#     class Meta:
#         model = ContentMaster
#         fields = '__all__'
        
        
   
    
    