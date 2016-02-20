function partial(func /*, 0..n args */) {
    var args = Array.prototype.slice.call(arguments, 1);
    return function() {
        var allArguments = args.concat(Array.prototype.slice.call(arguments));
        return func.apply(this, allArguments);
    };
}

function show_new_form(trigger_id, form_id) {
    if ($(trigger_id).val() === "-1") {
        $(form_id).show();
    } else {
        $(form_id).hide();
    }
}

function select_all(section_id) {
    $(section_id + ' .toggle-button').click( function () {
        $(section_id + ' input[type="checkbox"]').prop('checked', this.checked);
    })
}

function select_all_sub(section_id) {
    $(section_id + ' .toggle-button-sub').click( function () {
        $(section_id + ' input[type="checkbox"]').prop('checked', this.checked);
    })
}

/* Select/Deselect all button for Query Data -> Species
$( '#species .toggle-button' ).click( function () {
    $( '#species input[type="checkbox"]' ).prop('checked', this.checked)
})*/
select_all('#species_raw');
select_all('#species_ch');
select_all('#species_wr');

/* Select/Deselect all button for Query Data -> Traits
$( '#traits .toggle-button' ).click( function () {
    $( '#traits input[type="checkbox"]' ).prop('checked', this.checked)
})*/
/*select_all('#traits')*/
select_all_sub('#category_1');
select_all_sub('#category_2');
select_all_sub('#category_3');
select_all_sub('#category_4');
select_all_sub('#category_5');
select_all_sub('#category_6');
select_all_sub('#category_7');
select_all_sub('#category_8');
select_all('#traits');


/*$("#taxonomy").change(function () {
    if ($(this).attr("checked")) {
        $("#species_raw").show();
    }
    else {
        $("#species_raw").hide();
    }
});
*/
$("#species_raw").hide();
$("#species_ch").hide();
$("#species_wr").hide();

$(document).on( "change", "input[name=taxonomy]", function() {
    var tax = $(this).val();
    $(".species_container").hide();
    $("#"+tax).show();
    $('#id_reference_id').on('change', partial(show_new_form, '#id_reference_id', '#id_new_reference'));
    $('#id_taxonomy_id').on('change', partial(show_new_form, '#id_taxonomy_id', '#id_new_taxonomy'));
    $('#id_location_id').on('change', partial(show_new_form, '#id_location_id', '#id_new_location'));
});

$(document).ready(partial(show_new_form, '#id_reference_id', '#id_new_reference'));
$(document).ready(partial(show_new_form, '#id_taxonomy_id', '#id_new_taxonomy'));
$(document).ready(partial(show_new_form, '#id_location_id', '#id_new_location'));
