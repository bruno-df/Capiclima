"""Data migration: copia chave_pix e qrcode_pix de SiteConfig para SecaoApoie."""

from django.db import migrations


def copiar_pix_para_apoie(apps, schema_editor):
    SiteConfig = apps.get_model("ong", "SiteConfig")
    SecaoApoie = apps.get_model("ong", "SecaoApoie")

    try:
        config = SiteConfig.objects.get(pk=1)
    except SiteConfig.DoesNotExist:
        return

    apoie, _created = SecaoApoie.objects.get_or_create(pk=1)
    apoie.pix = config.chave_pix or ""
    apoie.qrcode_pix = config.qrcode_pix or ""
    apoie.save()


def reverter_pix_para_config(apps, schema_editor):
    SiteConfig = apps.get_model("ong", "SiteConfig")
    SecaoApoie = apps.get_model("ong", "SecaoApoie")

    try:
        apoie = SecaoApoie.objects.get(pk=1)
    except SecaoApoie.DoesNotExist:
        return

    config, _created = SiteConfig.objects.get_or_create(pk=1)
    config.chave_pix = apoie.pix or ""
    config.qrcode_pix = apoie.qrcode_pix or ""
    config.save()


class Migration(migrations.Migration):

    dependencies = [
        ("ong", "0010_add_pix_to_secaoapoie"),
    ]

    operations = [
        migrations.RunPython(copiar_pix_para_apoie, reverter_pix_para_config),
    ]
