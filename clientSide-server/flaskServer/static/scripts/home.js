

function getData(e) {
    e.preventDefault();
    var handle = $("#TwitterHandleInput").val().trim()
    var ele = checkLocalStorage(handle);
    if (ele == null) {
        $.get(`/graph?TwitterHandleInput=${handle}`, function (data, status) {
            console.log(data, status);

        })
    }
    else {
        window.location.href = "/graph?TwitterHandleInput=" + handle;
    }

}

// function checkLocalStorage(twitter_handle) {
//     if (localStorage.getItem(twitter_handle) == null) {
//         elements[0].data.time = new Date();
//         //console.log(elements);
//         localStorage.setItem(twitter_handle, JSON.stringify(elements));
//     }
//     else {
//         var ele = localStorage.getItem(twitter_handle);

//         console.log((new Date().getTime() - ele[0].data.time.getTime())/ (1000 * 3600 * 24) >=1);
//         if ((new Date().getTime() - ele[0].data.time.getTime())/ (1000 * 3600 * 24) >=1 ) {
//             elements = ele;
//         }
//     }
// }
function checkLocalStorage(twitter_handle) {
    if (localStorage.getItem(twitter_handle) == null) {
        //elements[0].data.time = new Date();
        //console.log(elements);
        //localStorage.setItem(twitter_handle, JSON.stringify(elements));
    }
    else {
        var ele = localStorage.getItem(twitter_handle);

        console.log((new Date().getTime() - ele[0].data.time.getTime()) / (1000 * 3600 * 24) >= 1);
        if ((new Date().getTime() - ele[0].data.time.getTime()) / (1000 * 3600 * 24) >= 1) {
            return ele;
        }
    }
    return null;
}