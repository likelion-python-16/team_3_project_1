from django.db import models

class Author(models.Model):                                     
    author_id = models.AutoField(primary_key=True) # 직접 PK 지정
    author_name = models.CharField(max_length=200)  # 저자 이름

    def str(self):
        return self.author_name
    
    class Meta:
        verbose_name = "저자"
        verbose_name_plural = "저자 목록"
        ordering = ["-author_id"]