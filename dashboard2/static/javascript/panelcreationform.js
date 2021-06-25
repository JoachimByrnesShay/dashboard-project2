/** function for controlling panel fields show and hide for purposes of differentiating tables (non-pygal in this app) from pygal charts using the same exact model.
 * tables do not use and should not use repo_name and panel_style, so these are hidden, unrequired, readonly, disabled if user selects 'TableOfRepos'
 * from panel_type options, and then on change to any other field, renabled, required, and shown again.   the toggle_non_table_fields function is called
 * on each call of the view/template, as well as on each change (of panel_type select option), to ensure not only the desired functionality upon change of option, but that the fields stay hidden in cases such as
 *  validation errors upon submitting after selecting 'TableOfRepos' with invalid fields, where the view is called and form must be re-rendered with the POST data for user review/correction **/

$(document).ready(function() {
    // select panel_type select field by id
    elem = $('select#id_panel_type')
    // get current value of panel_type from select
    current_selected = elem.children('option:selected').val()
    // this call will show/enable/de-readonly or hide/disable/readonly depending on value of selection option
    toggle_non_table_fields(current_selected)

    // on change of select field option, do the same (above) but also hide any alert messages on each change
    elem.change(function() {
        const selectedOption = $(this).children('option:selected').val()
        toggle_non_table_fields(selectedOption)
        messages = $('.alert')
        messages.hide()
    })
})

/** hides and disables repo_name and panel_style fields if 'TableOfRepos' is selected, otherwise shows and enables these
 **/
function toggle_non_table_fields(selected) {
    if (selected == 'TableOfRepos') {
        $('id_repo_name').val('')
        $('#id_repo_name').prop('required', false)
        $('#id_repo_name').prop('readonly', true)
        $('#id_repo_name').prop('disabled', true)
        $('#id_repo_name').hide()
        $('#id_panel_style').hide()
        $('label[for=id_repo_name]').hide()
        $('label[for=id_panel_style]').hide()
    } else {
        $('#id_repo_name').show()
        $('#id_repo_name').prop('required', true)
        $('#id_repo_name ').prop('readonly', false)
        $('#id_repo_name').removeAttr('disabled')
        $('#id_panel_style').show()
        $('label[for=id_repo_name]').show()
        $('label[for=id_panel_style]').show()
    }
}