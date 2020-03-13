from django.contrib import admin

from ddnsbroker.models import Host, UpdateService, Record
from django.contrib import messages


class HostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('fqdn', 'secret', ('ipv4_enabled', 'ipv6_enabled'))
        }),
        ('Manual IPs', {
            'classes': ('collapse',),
            'fields': ('ipv4', 'ipv6')
        })
    )

    list_display = ('fqdn', 'ipv4_enabled', 'ipv6_enabled', 'ipv4', 'ipv6')

    list_editable = ('ipv4_enabled', 'ipv6_enabled', 'ipv4', 'ipv6')

    list_filter = ('ipv4_enabled', 'ipv6_enabled')

    search_fields = ('fqdn',)


class RecordAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('host', 'fqdn', ('ipv4_enabled', 'ipv6_enabled'))
        }),
        ('Record composition', {
            'fields': ('ipv4_netmask', 'ipv4_host_id', 'ipv6_netmask', 'ipv6_host_id')
        }),
        ('Update service', {
            'fields': ('service', 'username', 'password')
        })
    )

    list_display = ('fqdn', 'host', 'ipv4_enabled', 'ipv6_enabled', 'effective_ipv4', 'effective_ipv6', 'service')

    list_editable = ('ipv4_enabled', 'ipv6_enabled')

    list_filter = (
        ('host', admin.RelatedOnlyFieldListFilter),
        'ipv4_enabled',
        'ipv6_enabled',
        ('service', admin.RelatedOnlyFieldListFilter)
    )

    save_as = True

    save_as_continue = False

    search_fields = ('fqdn', 'host__fqdn')

    actions = ['update_records']

    def update_records(self, request, queryset):  # TODO: maybe with intermediate page because it could take long
        for record in queryset:
            pass
        self.message_user(request, "This function is not yet implemented", level=messages.WARNING)

    update_records.short_description = "Force update selected records"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['updateServices'] = UpdateService.objects.all()
        return super(RecordAdmin, self).change_view(request, object_id, form_url, extra_context)


class UpdateServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

    search_fields = ('name', 'url')


admin.site.register(Host, HostAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(UpdateService, UpdateServiceAdmin)
