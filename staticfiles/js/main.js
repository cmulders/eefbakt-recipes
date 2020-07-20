$(() => {
  let select2_options = {
    minimumResultsForSearch: 8,
  };
  $(".inline-formset.select2 tr:not(.empty-form) select").select2(
    select2_options
  );
});
