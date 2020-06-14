from django.contrib import admin
from vadetisweb.models import *

# Register your models here.
admin.site.register(UserSetting)
admin.site.register(DataSet)
admin.site.register(TimeSeries)
admin.site.register(Location)
admin.site.register(UserTasks)
admin.site.register(ModelTaskMeta)
admin.site.register(Category)
admin.site.register(FrequentlyAskedQuestion)