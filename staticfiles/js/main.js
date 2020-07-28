function try_upgrade_select2() {
  try {
    // Upgrade select inputs to select2 with search function
    $(".inline-formset.select2 tr:not(.empty-form) select").select2({
      minimumResultsForSearch: 8,
    });
  } catch (error) {
    console.error(error);
    // We tried to initialize, but failed, no worries
  }
}

function try_upgrade_dateinput() {
  try {
    // Upgrade date inputs to datapicker
    $("input.dateinput").flatpickr({
      altInput: true,
      altFormat: "F j, Y",
      dateFormat: "Y-m-d",
      weekNumbers: true,
    });
  } catch (error) {
    console.error(error);
    // We tried to initialize, but failed, no worries
  }
}

function try_upgrade_inlineformset_ordering() {
  try {
    $(".inline-formset table").each((idx, table) => {
      Sortable.create($(table).find("tbody").get(0), {
        handle: 'td[id$="-ORDER"]',
        animation: 100,
        swapThreshold: 0.7,
        onUpdate: (ev) => {
          // Update the order input with the current value
          let tbody = ev.to;
          Array.from(tbody.children)
            .map((ele, idx) =>
              ele.querySelector('input[id$="-ORDER"]:not([id*="__prefix__"])')
            )
            .filter(Boolean)
            .forEach((ele, idx) => {
              if (!!ele.value) {
                // idx is zero based, increase by 1 to get one-based
                ele.value = (idx + 1).toString();
              }
            });
        },
      });
      table.classList.add("sortable");
    });
  } catch (error) {
    console.error(error);
    // We tried to initialize, but failed, no worries
  }
}

function try_upgrade_inlineformset_add_button() {
  $(".inline-formset").each((idx, ele) => {
    let container = ele;
    let button_container = container.appendChild(document.createElement("div"));
    button_container.className = "d-flex justify-content-center";
    button_container.innerHTML =
      "<div class='btn btn-sm btn-success mt-n2 formset-add-row'>+ Add</div>";
  });

  $(".inline-formset").on("click", ".btn.formset-add-row", (ev) => {
    let formset = $(ev.delegateTarget);
    let total_form_input = formset.find("input[id$='-TOTAL_FORMS']");
    let form_idx = total_form_input.val();

    let tbody = formset.find("tbody");
    let new_row = tbody
      .find(".empty-form")
      .html()
      .replace(/__prefix__/g, form_idx);
    tbody.get(0).appendChild(document.createElement("tr")).innerHTML = new_row;
    total_form_input.val(parseInt(form_idx) + 1);

    // Need to reupgrade select2 fields
    try_upgrade_select2();
  });
}

$(() => {
  try_upgrade_select2();
  try_upgrade_dateinput();
  try_upgrade_inlineformset_ordering();
  try_upgrade_inlineformset_add_button();
});
