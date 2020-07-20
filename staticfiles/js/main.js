$(() => {
  let select2_options = {
    minimumInputLength: 2,
    minimumResultsForSearch: 15,
  };
  $(".inline-formset.select2 tr:not(.empty-form) select").select2(
    select2_options
  );
});
