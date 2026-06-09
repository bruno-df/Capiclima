"""
Management command para migrar dados do SiteSection genérico
para os novos modelos dedicados (SecaoHome, SecaoSobre, SecaoApoie).

Uso: python manage.py migrate_sitesection
"""
from django.core.management.base import BaseCommand

from apps.ong.models import SecaoApoie, SecaoHome, SecaoSobre, SiteSection


# Mapa de slugs do SiteSection → campo nos novos modelos
SLUG_MAP_HOME = {
    "home-juventudes": {
        "titulo_field": "titulo_juventudes",
        "texto_field": "texto_juventudes",
    },
    "home-parceiros": {
        "titulo_field": "titulo_parceiros",
        "texto_field": "texto_parceiros",
    },
    "home-cta": {
        "titulo_field": "titulo_cta",
        "texto_field": "texto_cta",
        "link_field": "link_cta",
    },
}

SLUG_MAP_APOIE = {
    "apoie-voluntariado": {
        "texto_field": "texto_voluntariado",
        "link_field": "link_voluntariado",
    },
    "apoie-doacao": {
        "texto_field": "texto_doacao",
        "link_field": "link_doacao",
    },
    "apoie-parcerias": {
        "texto_field": "texto_parcerias",
        "link_field": "link_parcerias",
    },
    "apoie-compartilhe": {
        "texto_field": "texto_compartilhe",
    },
}


class Command(BaseCommand):
    help = "Migra dados de SiteSection para SecaoHome, SecaoSobre e SecaoApoie."

    def handle(self, *args, **options):
        home = SecaoHome.load()
        apoie = SecaoApoie.load()
        sobre = SecaoSobre.load()

        migrated = 0

        # --- Migrar seções da Home ---
        for slug, field_map in SLUG_MAP_HOME.items():
            try:
                section = SiteSection.objects.get(slug=slug)
            except SiteSection.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  Slug '{slug}' não encontrado, pulando."))
                continue

            titulo_field = field_map.get("titulo_field")
            texto_field = field_map.get("texto_field")
            link_field = field_map.get("link_field")

            if titulo_field and section.titulo:
                setattr(home, titulo_field, section.titulo)
            if texto_field and section.texto_principal:
                setattr(home, texto_field, section.texto_principal)
            if link_field and section.botao_url:
                setattr(home, link_field, section.botao_url)

            migrated += 1
            self.stdout.write(f"  [OK] '{slug}' -> SecaoHome.{texto_field}")

        home.save()
        self.stdout.write(self.style.SUCCESS(f"SecaoHome salva com {migrated} seções migradas."))

        # --- Migrar seções do Apoie ---
        migrated = 0
        for slug, field_map in SLUG_MAP_APOIE.items():
            try:
                section = SiteSection.objects.get(slug=slug)
            except SiteSection.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  Slug '{slug}' não encontrado, pulando."))
                continue

            texto_field = field_map.get("texto_field")
            link_field = field_map.get("link_field")

            if texto_field and section.texto_principal:
                setattr(apoie, texto_field, section.texto_principal)
            if link_field and section.botao_url:
                setattr(apoie, link_field, section.botao_url)

            migrated += 1
            self.stdout.write(f"  [OK] '{slug}' -> SecaoApoie.{texto_field}")

        apoie.save()
        self.stdout.write(self.style.SUCCESS(f"SecaoApoie salva com {migrated} seções migradas."))

        # --- SecaoSobre (sem dados no SiteSection, mantém defaults) ---
        sobre.save()
        self.stdout.write(self.style.SUCCESS("SecaoSobre criada/atualizada com defaults."))

        self.stdout.write(self.style.SUCCESS("\nMigração concluída com sucesso!"))
        self.stdout.write(
            self.style.NOTICE(
                "NOTA: O modelo SiteSection NÃO foi removido. "
                "Remova manualmente após confirmar que tudo funciona."
            )
        )
