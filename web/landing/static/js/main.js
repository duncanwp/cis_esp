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
    $.each(data.results, function () {
        opt.append($('<option/>').val(this.id).text(this.name));
    });
    opt.val(old_val);
    opt.change();
}

function toWKT(layer) {
    /*
        Convert a layer (array) object to a WKT representation using Wicket
     */
    var wkt = new Wkt.Wkt();

    // Deconstruct an existing point feature e.g. google.maps.Marker instance
    wkt.fromObject(layer[0]);
    return wkt
}