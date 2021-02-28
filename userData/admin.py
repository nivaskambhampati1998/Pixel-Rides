from django.contrib import admin
from userData.models import   UserDetailsInfo, CloseContacts, WalletMapping, WalletHistory, Scheduled_Rides

# Register your models here.

admin.site.register(UserDetailsInfo)
admin.site.register(CloseContacts)
admin.site.register(WalletMapping)
admin.site.register(WalletHistory)
admin.site.register(Scheduled_Rides)