from crispy_forms.helper import FormHelper
from django.db import transaction
from django.views.generic import edit


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
