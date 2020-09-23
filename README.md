# Recipe application

The Recipe application is used to store and create cooking recipes. Some of it's features:

- Store products with price information and conversion between units
- Store recipes with instructions. Each recipe consists of ingredients and other recipes (but cycles are not allowed).
- Store sessions, a way of combining multiple recipes and/or products in a single cook. Such as a cake with various fillings.
- Grocery list generation based on the ingredients used in a session and shows the prices if known
- Forms have (optional) javascript upgrades to enhance data entry, such as search in lists and dynamic addition of extra forms in a formset

## To improve

[] Layout and styling is not good
[] Layout is not responsive enough for phone, tablet and laptop screen sizes
[] User interface is not dynamic and makes data entry and navigation slow
[] Images are stored and displayed uncompressed, this detoriates page load times

# Architecture

The application uses the Django web framework. The different parts of the app are split using Django apps: common, data and baking.
