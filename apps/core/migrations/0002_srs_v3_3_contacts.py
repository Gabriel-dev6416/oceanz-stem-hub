"""SRS v3.3 contacts: one WhatsApp number, three call lines, hub address, WhatsApp channel and
brand line (FR-WEB-10, FR-WEB-20, FR-COM-03)."""

from django.db import migrations, models

import apps.core.models

ADDRESS = "#5 Gunning Rd, Abakaliki, Ebonyi State, Nigeria"


def fill_address(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(address="").update(address=ADDRESS)


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="sitesettings", name="whatsapp_secondary"),
        migrations.RenameField(
            model_name="sitesettings", old_name="whatsapp_primary", new_name="whatsapp"
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="whatsapp",
            field=models.CharField(
                default="+234 706 457 9661",
                max_length=20,
                validators=[apps.core.models.phone_validator],
                verbose_name="WhatsApp number",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="phone_primary",
            field=models.CharField(
                default="+234 706 457 9661",
                max_length=20,
                validators=[apps.core.models.phone_validator],
                verbose_name="call line 1",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="phone_secondary",
            field=models.CharField(
                blank=True,
                default="+234 705 526 0308",
                max_length=20,
                validators=[apps.core.models.phone_validator],
                verbose_name="call line 2",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="phone_tertiary",
            field=models.CharField(
                blank=True,
                default="+234 902 835 3019",
                max_length=20,
                validators=[apps.core.models.phone_validator],
                verbose_name="call line 3",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="address",
            field=models.TextField(blank=True, default=ADDRESS, verbose_name="hub address"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="whatsapp_channel_url",
            field=models.URLField(blank=True, verbose_name="WhatsApp channel URL"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="brand_line",
            field=models.CharField(
                default=(
                    "We don't just raise learners; we raise teachers, professionals, "
                    "innovators and leaders."
                ),
                max_length=160,
            ),
        ),
        migrations.RunPython(fill_address, migrations.RunPython.noop),
    ]
