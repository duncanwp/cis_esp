/**
 * Created by duncan on 04/01/2017.
 */

function data_to_select(data, select_selector) {
    /*
     Fill a select multiple input field with JSON data
     Inspired by: http://stackoverflow.com/questions/1388302/create-option-on-the-fly-with-jquery
     */
    var opt = $(select_selector);
    var old_val = opt.val();
    opt.html('');
    $.each(data.results.features, function () {
        opt.append($('<option/>').val(this.id).text(this.properties.name));
    });
    opt.val(old_val);
    opt.change();
}
