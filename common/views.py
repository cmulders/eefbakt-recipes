from django.shortcuts import render

from .forms import ImageTagInlineFormset

# Create your views here.


class ImageTagFormsetMixin(object):
    def get_imagetag_formset(self):
        kwargs = {
            "prefix": "images",
            "instance": self.object,
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {"data": self.request.POST, "files": self.request.FILES,}
            )

        return ImageTagInlineFormset(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update(
            {"images_formset": self.get_imagetag_formset(),}
        )
        return super().get_context_data(**kwargs)

    def form_valid(self, form, products_formset, recipes_formset):
        response = super().form_valid(form)

        products_formset.instance = self.object
        products_formset.save()

        recipes_formset.instance = self.object
        recipes_formset.save()
        return response

    def form_invalid(self, form, products_formset, recipes_formset):
        """If the form is invalid, render the invalid form and formsets."""
        return self.render_to_response(
            self.get_context_data(
                form=form,
                products_formset=products_formset,
                recipes_formset=recipes_formset,
            )
        )

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate the form and formset instances with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        products_formset = self.get_product_formset()
        recipes_formset = self.get_recipe_formset()
        if (
            form.is_valid()
            and products_formset.is_valid()
            and recipes_formset.is_valid()
        ):
            return self.form_valid(form, products_formset, recipes_formset)
        else:
            return self.form_invalid(form, products_formset, recipes_formset)
