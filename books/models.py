from django.db import models

# Create your models here.

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    author_id = models.ForeignKey(
        'authors.Author', 
        related_name="books", 
        on_delete=models.CASCADE, 
        db_column="author_id"
    )
    title = models.CharField(null=False, max_length=200)
    description = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title   
    
    class Meta:
        verbose_name = "책"
        verbose_name_plural = "책 목록"
        ordering = ["-created_at"]