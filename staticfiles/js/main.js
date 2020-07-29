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
  document.querySelectorAll(".inline-formset").forEach((ele, idx) => {
    let container = ele;
    let total_form_input = ele.querySelector("input[id$='-TOTAL_FORMS']");
    let max_form_input = ele.querySelector("input[id$='-MAX_NUM_FORMS']");
    let form_idx = parseInt(total_form_input.value);
    let form_max = parseInt(max_form_input.value);

    if (form_idx == form_max) {
      return; // Do not add a button
    }
    let button_container = container.appendChild(document.createElement("div"));
    button_container.className = "d-flex justify-content-center";
    button_container.innerHTML =
      "<button type='button' class='btn btn-sm btn-success mt-n2 formset-add-row'>+ Add</button>";
  });

  $(".inline-formset").on("click", ".btn.formset-add-row", (ev) => {
    let formset = $(ev.delegateTarget);
    let total_form_input = formset.find("input[id$='-TOTAL_FORMS']");
    let max_form_input = formset.find("input[id$='-MAX_NUM_FORMS']");
    let form_idx = total_form_input.val();
    let form_max = max_form_input.val();

    if (form_idx == form_max) {
      $(ev.target)
        .addClass("disabled btn-danger")
        .removeClass("btn-success")
        .html("Max forms");
      return;
    }

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

function make_bootstrap_fileinput() {
  $(".inline-formset").on("change", ".custom-file-input", (ev) => {
    var filenames = "";
    for (let i = 0; i < ev.target.files.length; i++) {
      filenames += (i > 0 ? ", " : "") + ev.target.files[i].name;
    }
    ev.target.parentNode.querySelector(
      ".custom-file-label"
    ).textContent = filenames;
  });
}

$(() => {
  try_upgrade_select2();
  try_upgrade_dateinput();
  try_upgrade_inlineformset_ordering();
  try_upgrade_inlineformset_add_button();
  make_bootstrap_fileinput();
});
