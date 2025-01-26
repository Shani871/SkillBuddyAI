from django.contrib import admin


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'completed')
    list_filter = ('completed', 'due_date')
