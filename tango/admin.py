from django.contrib import admin
from tango.models import *

class VideoAdmin(admin.StackedInline):
    model = Video

class AnswersAdmin(admin.StackedInline):
    model = Answers

class ChapterAdmin(admin.StackedInline):
    model = Chapter

class LearningAdmin(admin.TabularInline):
    model = Learning

class CourseAdmin(admin.ModelAdmin):
    inlines = [LearningAdmin,ChapterAdmin]

class ChapterAdmin(admin.ModelAdmin):
    inlines = [VideoAdmin]

class QuestionsAdmin(admin.ModelAdmin):
    inlines = [AnswersAdmin]

admin.site.register(Course,CourseAdmin)
admin.site.register(Video)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(UserCourse)
admin.site.register(Payment)
admin.site.register(ContactDetail)
admin.site.register(UserProfile)
admin.site.register(CouponCode)
admin.site.register(IpTrack)
admin.site.register(Questions,QuestionsAdmin)
admin.site.register(Answers)
admin.site.register(CSVFile)
admin.site.register(UpcomingCourse)
