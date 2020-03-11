(function ($) {
    $(function () {
        const host = $("#id_host");
        const fqdn = $("#id_fqdn");
        const service = $("#id_service");
        const username = $("#id_username");

        if (host.length === 0)
            return;

        let hostOldValue = host.prop(host.prop('selectedIndex')).label;
        let usernameIsFqdn = false;

        // Change fqdn when host is changed
        host.change(function () {
            if (this.selectedIndex === 0)
                return;

            const newValue = this[this.selectedIndex].label;

            if (fqdn.val() === "" || fqdn.val() === hostOldValue)
                fqdn.val(newValue);

            hostOldValue = newValue;
        });

        // Disable username field if usernameisfqdn is enabled
        service.change(function () {
            if (this.selectedIndex === 0)
                return;

            $.ajax({
                "type": "GET",
                "url": "/updateservice/" + this.selectedIndex + "/get/usernameisfqdn",
                "dataType": "json",
                "cache": true,
                "success": function (json) {
                    username.prop("disabled", json);
                    username.val(fqdn.val());
                    usernameIsFqdn = json;
                }
            })
        });

        // Change username to fqdn if usernameisfqdn is enabled (only cosmetic)
        fqdn.change(function () {
            if (usernameIsFqdn)
                username.val(this.value);
        });

    });
})(jQuery);
