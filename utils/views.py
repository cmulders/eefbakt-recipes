from crispy_forms.helper import FormHelper
from django.core.exceptions import ImproperlyConfigured
from django.db import models, transaction
from django.http import HttpResponseRedirect
from django.views.generic import detail, edit


class ModelFormWithInlinesView(
    edit.SingleObjectTemplateResponseMixin, edit.ModelFormMixin, edit.ProcessFormView
):
    template_name_suffix = "_form"
    inlines = {}

    def get_inline(self, prefix, cls):
        kwargs = {
            "prefix": prefix,
            "instance": self.object,
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {"data": self.request.POST, "files": self.request.FILES,}
            )

        return cls(**kwargs)

    def get_inlines(self):
        return {
            f"{key}_formset": self.get_inline(key, cls)
            for key, cls in self.inlines.items()
        }

    def get_formset_helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        helper.use_custom_control = False
        helper.template = "bootstrap4/table_inline_formset.html"
        return helper

    def get_context_data(self, **kwargs):
        kwargs.update(
            {"formset_helper": self.get_formset_helper(), "inlines": self.get_inlines()}
        )
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form, inlines={}):
        response = super().form_valid(form)

        for inline in inlines.values():
            inline.instance = self.object
            inline.save()

        return response

    def form_invalid(self, form, inlines={}):
        """If the form is invalid, render the invalid form and formsets."""
        return self.render_to_response(self.get_context_data(form=form, **inlines,))

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate the form and formset instances with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        inlines = self.get_inlines()
        if form.is_valid() and all(inline.is_valid() for inline in inlines.values()):
            return self.form_valid(form, inlines)
        else:
            return self.form_invalid(form, inlines)


class DuplicateView(detail.SingleObjectTemplateResponseMixin, detail.BaseDetailView):
    """Provide the ability to duplicate objects."""

    template_name_suffix = "_confirm_duplicate"
    success_url = None

    def clone_relations(self, target):
        source = self.get_object()

        for rel in source._meta.get_fields():
            if rel.many_to_many and rel.concrete:
                ThroughModel = rel.remote_field.through
                field_name = rel.m2m_field_name()
                filter = {field_name: source.pk}
                for obj in ThroughModel.objects.filter(**filter).all():
                    obj.pk = None
                    setattr(obj, field_name, target)
                    obj.save(force_insert=True)

    @transaction.atomic
    def duplicate(self, request, *args, **kwargs):
        """
        Call the duplicate() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()

        self.object.pk = None
        self.object.save(force_insert=True)

        self.clone_relations(self.object)

        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        return self.duplicate(request, *args, **kwargs)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model."
                )
        return url


class MixinObjectPageTitle:
    def get_context_data(self, **kwargs):
        if hasattr(self, "object"):
            kwargs["page_title"] = str(self.object)

        return super().get_context_data(**kwargs)
