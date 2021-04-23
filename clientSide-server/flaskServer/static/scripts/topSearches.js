

$(document).ready(function () {
  
  var tablebody = $("#topSearchesTable > tbody");
  tablebody.empty();
    for(var account of accounts) {
      console.log(account);
      var row = CreateTableRow(account);
      tablebody.append(row);
    }


    var table = document.getElementById("topSearchesTable");
    var rows = table.getElementsByTagName("tr");
    for (let i = 0; i < rows.length; i++) {
      var currentRow = table.rows[i];
      currentRow.onclick = createClickHandler(currentRow);
      
      
    }
})
    
function CreateTableRow(account) {
  var row = document.createElement("tr");
  var number = document.createElement("th");
  number.innerHTML = 1;
  number.scope = "row";
  var imgCol = document.createElement("td");
  var img = document.createElement("img");
  img.src=account.image;
  img.className = "image"
  imgCol.appendChild(img);

  var name = document.createElement("td");
  name.innerHTML = account.name;
  var link = document.createElement("td");
  link.innerHTML= "<a href='http://twitter.com/"+account.twitter_handle+"'>"+"@"+account.twitter_handle+"</a>";
  var views = document.createElement("td");
    views.innerHTML=account.views;
  row.appendChild(number);
  row.appendChild(imgCol);
  row.appendChild(name);
  row.appendChild(link);
  row.appendChild(views);
  return row;
}

var createClickHandler = function(row) {
  return function() {

    var cell = row.getElementsByTagName("td")[2];
    console.log(cell.children[0].innerHTML)
    var name = cell.children[0].innerHTML.substring(1);
    $.ajax({
      type:"POST",
      url:"/topSearches/update",
      data: {"twitter_handle":name},
      success: function() {
        console.log("pass");
      }
    })
    window.location.href ="/graph?TwitterHandleInput="+name;
    //var id = cell.innerHTML;
    //alert("id:" + id);
  };
};