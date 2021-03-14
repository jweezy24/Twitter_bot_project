

function getData(e) {
    e.preventDefault();
    var handle = $("#TwitterHandleInput").val().trim()
    
    $.get(`/getData/${ handle }` , function(data, status) {
        console.log(data, status);
        
    })
}
    