function recordData() {
    // get form data
    var size = document.getElementById('size').value;
    var colour = document.getElementById('colour').value;
    var id = document.getElementById('id').value;

    // create table if there is no table 
    if (!document.getElementById('data-table')) {
        var table = document.createElement('table');
        table.setAttribute('id', 'data-table');

        // create header
        var header = table.createTHead();
        var headerRow = header.insertRow(0);
        headerRow.insertCell(0).innerHTML = "<b>Size</b>";
        headerRow.insertCell(1).innerHTML = "<b>Colour</b>";
        headerRow.insertCell(2).innerHTML = "<b>ID</b>";

        // create 
        document.getElementById('table-container').appendChild(table);
    }

    // add a new line 
    var table = document.getElementById('data-table');
    var newRow = table.insertRow();
    newRow.insertCell(0).innerHTML = size;
    newRow.insertCell(1).innerHTML = colour;
    newRow.insertCell(2).innerHTML = id;

    // clear 
    document.getElementById('data-form').reset();

}
function sendData(){
    
}