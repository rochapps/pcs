$(document).ready(partial(show_new_form, '#id_reference_id', '#id_new_reference'));
$(document).ready(partial(show_new_form, '#id_taxonomy_id', '#id_new_taxonomy'));
$(document).ready(partial(show_new_form, '#id_location_id', '#id_new_location'));
$('#id_reference_id').on('change', partial(show_new_form, '#id_reference_id', '#id_new_reference'))
$('#id_taxonomy_id').on('change', partial(show_new_form, '#id_taxonomy_id', '#id_new_taxonomy'))
$('#id_location_id').on('change', partial(show_new_form, '#id_location_id', '#id_new_location'))
