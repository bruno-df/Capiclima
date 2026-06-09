CMS_ADMIN_GROUPS = ("Admin", "Colaboradores")
COLLABORATOR_MODEL_NAMES = (
    "atividade",
    "conteudosobre",
    "destaqueinicio",
    "membroequipe",
    "opportunity",
    "siteconfig",
    "sitesection",
)


def user_has_cms_access(user):
    if not user.is_authenticated or not user.is_active or not user.is_staff:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=CMS_ADMIN_GROUPS).exists()


def sync_cms_groups():
    from django.contrib.auth.models import Group, Permission

    collaborators, _created = Group.objects.get_or_create(name="Colaboradores")
    admins, _created = Group.objects.get_or_create(name="Admin")

    collaborator_permissions = Permission.objects.filter(
        content_type__app_label="ong",
        content_type__model__in=COLLABORATOR_MODEL_NAMES,
    )
    collaborators.permissions.set(collaborator_permissions)
    admins.permissions.set(Permission.objects.all())

    return collaborators, admins
