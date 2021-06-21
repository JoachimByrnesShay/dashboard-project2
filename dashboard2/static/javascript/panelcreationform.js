$(document).ready(function() {
    elem = $('select#id_panel_type')
    current_selected = elem.children('option:selected').val()
    show_and_hide(current_selected)

    elem.change(function() {
        const selectedOption = $(this).children('option:selected').val()
        // const selectedOption = current_selected
        alert('You have selected the option - ' + selectedOption)
        show_and_hide(selectedOption)
        messages = $('.alert')
        messages.hide()
    })
})

function show_and_hide(selected) {
    if (selected == 'TableOfRepos') {
        $('id_repo_name').val('')
        // $("text#id_repo_name").prop('disabled', true);
        // $("text#id_repo_name").each(function(){
        //  $(this).attr('readonly','readonly');
        $('#id_repo_name').prop('required', false)
        $('#id_repo_name').prop('readonly', true)
        $('#id_repo_name').prop('disabled', true)
        $('#id_repo_name').hide()
        $('#id_panel_style').hide()
        $('label[for=id_repo_name]').hide()
        $('label[for=id_panel_style]').hide()

        // });
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