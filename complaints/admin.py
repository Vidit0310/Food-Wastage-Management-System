from django.contrib import admin
from .models import area_master,FoodCollectionRequests,feedbacks_master_byUsers,feedbacks_master_byFC

class AreaMasterAdmin(admin.ModelAdmin):
    list_display = ['area_id', 'area_name', 'status_id']
    search_fields = ['area_name']
    list_filter = ['status_id']

class FoodCollectionRequestsAdmin(admin.ModelAdmin):
    # list_display = ['complaint_id', 'complainant_name', 'complainant_contact_no','complainant_email', 'area', 'complainant_address', 'detailed_description']
    # search_fields = ['area']

    # list_display = ('complaint_id', 'complainant_name', 'complainant_contact_no', 'complainant_email', 'area', 'complainant_address', 'detailed_description', 'status', 'changed_by')

    def complaint_id(self, obj):
        return obj.complaint_id
    complaint_id.short_description = 'Complaint ID'

    def complainant_name(self, obj):
        return obj.complainant_name
    complainant_name.short_description = 'Name'

    def complainant_contact_no(self, obj):
        return obj.complainant_contact_no
    complainant_contact_no.short_description = 'Contact No'

    def complainant_email(self, obj):
        return obj.complainant_email
    complainant_email.short_description = 'Email'

    def area(self, obj):
        return obj.area
    area.short_description = 'Area'

    def complainant_address(self, obj):
        return obj.complainant_address
    complainant_address.short_description = 'Address'

    def detailed_description(self, obj):
        return obj.detailed_description
    detailed_description.short_description = 'Description'

    def status(self, obj):
        return obj.status
    status.short_description = 'Status'

    def changed_by(self, obj):
        return obj.changed_by
    changed_by.short_description = 'Changed By'



admin.site.register(area_master,AreaMasterAdmin)
admin.site.register(FoodCollectionRequests,FoodCollectionRequestsAdmin)
admin.site.register(feedbacks_master_byUsers)
admin.site.register(feedbacks_master_byFC)

