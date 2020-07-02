from django.db import models
from django.utils.text import slugify
from tinymce import HTMLField


COLOR_CHOICES = (
    ('green','GREEN'),
    ('blue', 'BLUE'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('black','BLACK'),
)
 

class ContentMaster(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=250,null=True)
    content = HTMLField('Content')
    
    title_in_arabic = models.CharField(max_length=120)
    description_in_arabic = models.TextField(max_length=250,null=True)
    content_in_arabic = HTMLField('Content in Arabic')
    
    legal_text = models.TextField(blank=True,null=True)
    
    # main_content = models.TextField(blank=True,null=True)
    # main_content_arabic = models.TextField(blank=True,null=True)

    # main_content = HTMLField('Content')
    # main_content_arabic = HTMLField('Content in Arabic')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'meenfee_content_master'




class CategoryMaster(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    description= models.CharField(max_length=500)

   # color = models.CharField(max_length=6, choices=COLOR_CHOICES, default='green')
    #uom_id = models.IntegerField(default=1)
   # uom_id = models.CharField(default="--Select--",max_length=255)
    #company_id = models.IntegerField(default=1)
    
    user_id = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    inactive_date= models.CharField(max_length=500)
    created_by= models.IntegerField(default=1)
    created_date = models.CharField(max_length=500)
    updated_by= models.IntegerField(default=1)
    updated_date= models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.code


    class Meta:
        db_table = 'meenfee_category_master'
        
        
        
class SubCategoryMaster(models.Model):
    category_id= models.IntegerField(default=1)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    description= models.CharField(max_length=500)

   # color = models.CharField(max_length=6, choices=COLOR_CHOICES, default='green')
    #uom_id = models.IntegerField(default=1)
   # uom_id = models.CharField(default="--Select--",max_length=255)
    #company_id = models.IntegerField(default=1)
    
    user_id = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    inactive_date= models.CharField(max_length=500)
    created_by= models.IntegerField(default=1)
    created_date = models.CharField(max_length=500)
    updated_by= models.IntegerField(default=1)
    updated_date= models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.code


    class Meta:
        db_table = 'meenfee_sub_category_master'


