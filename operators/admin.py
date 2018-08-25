from django.contrib import admin
from .models import UserProfile, CourseInfo, RegisterInfo
from .models import UserProfile, CourseInfo, Oplog

# Register your models here.

admin.site.register(UserProfile)
# admin.site.register(CourseInfoTrash)
admin.site.register(CourseInfo)
admin.site.register(RegisterInfo)
admin.site.register(Oplog)

