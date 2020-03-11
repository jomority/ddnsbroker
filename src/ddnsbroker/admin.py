from django.contrib import admin

from ddnsbroker.models import Host, UpdateService, Record


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

    class Media:
        js = ('js/admin_record.js',)


admin.site.register(Host, HostAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(UpdateService)
