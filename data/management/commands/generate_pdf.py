import logging
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

import weasyprint
from data.models import Session
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse
from django.test.client import RequestFactory
from django.urls import get_script_prefix, resolve, reverse

logger = logging.getLogger("weasyprint")
logger.addHandler(logging.StreamHandler())


def django_static_fetcher(url):
    if url.startswith("file:"):
        mime_type, encoding = mimetypes.guess_type(url)
        url_path = urlparse(url).path
        data = {
            "mime_type": mime_type,
            "encoding": encoding,
            "filename": Path(url_path).name,
        }

        default_media_url = settings.MEDIA_URL in ("", get_script_prefix())
        if not default_media_url and url_path.startswith(settings.MEDIA_URL):
            media_root = settings.MEDIA_ROOT
            if isinstance(settings.MEDIA_ROOT, Path):
                media_root = f"{settings.MEDIA_ROOT}/"
            path = url_path.replace(settings.MEDIA_URL, media_root, 1)
            data["file_obj"] = default_storage.open(path)
            return data

        elif settings.STATIC_URL and url_path.startswith(settings.STATIC_URL):
            path = url_path.replace(settings.STATIC_URL, "", 1)
            data["file_obj"] = open(staticfiles_storage.path(path), "rb")
            return data

    if url not in cache:
        result = weasyprint.default_url_fetcher(url)

        if "file_obj" in result:
            result["string"] = result["file_obj"].read()
            result["file_obj"].close()
            del result["file_obj"]
            cache.set(url, result)
        else:
            return result

    return cache.get(url)


class Command(BaseCommand):
    help = "Generates pdf export of all sessions."
    rf = RequestFactory()

    def add_arguments(self, parser):
        parser.add_argument("export_dir", type=Path)

    def handle(self, *args, **options):
        root: Path = options["export_dir"]
        root.mkdir(exist_ok=True, parents=True)
        self.stdout.write(
            self.style.SUCCESS(f"Starting export of all sessions to {root}")
        )

        to_export = Session.objects.count()

        session: Session
        for idx, session in enumerate(Session.objects.all(), start=1):
            if not session.images.exists():
                continue
            name = f"{session.pk}_{slugify(session.title)}.pdf"
            filepath = root / name

            for present in root.glob(f"{session.pk}_*.pdf"):
                present.unlink(missing_ok=True)

            html = self.render_view("data:session-export", pk=session.pk)

            # filepath.with_suffix(".html").write_text(html)

            weasyprint.HTML(
                string=html, url_fetcher=django_static_fetcher, base_url=f"file://"
            ).write_pdf(
                filepath,
            )
            self.stdout.write(
                f"{idx: 3}/{to_export: 3} Exported {filepath.name}",
                style_func=self.style.SUCCESS,
            )

    def render_view(self, viewname: str, *args, **kwargs) -> str:
        url = reverse(viewname, args=args, kwargs=kwargs)
        func, vw_args, vw_kwargs = resolve(url)

        response = func(self.rf.get(url), *vw_args, **vw_kwargs)

        assert isinstance(response, HttpResponse)
        assert response.status_code == 200

        if isinstance(response, TemplateResponse):
            response = response.render()

        html: str = response.content.decode()
        return html
