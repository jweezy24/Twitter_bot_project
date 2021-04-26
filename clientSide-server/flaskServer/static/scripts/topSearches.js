

$(document).ready(function () {
  //console.log(accounts)
  var tablebody = $("#topSearchesTable > tbody");
  tablebody.empty();
  var count = 1;
  sortElements(accounts)
  for (var account of accounts) {
    //console.log(account);
    var row = CreateTableRow(account, count);
    count++;
    tablebody.append(row);
  }


  var table = document.getElementById("topSearchesTable");
  var rows = table.getElementsByTagName("tr");
  for (let i = 0; i < rows.length; i++) {
    var currentRow = table.rows[i];
    currentRow.onclick = createClickHandler(currentRow);


  }
})

function sortElements(items) {
  items.sort(function (first, second) {
    return second.requested - first.requested;
  })
}

function CreateTableRow(account, count) {
  var row = document.createElement("tr");
  var number = document.createElement("th");
  number.innerHTML = count;
  number.scope = "row";
  var imgCol = document.createElement("td");
  var img = document.createElement("img");
  img.src = account.image;
  img.className = "image"
  imgCol.appendChild(img);

  var name = document.createElement("td");
  name.innerHTML = account.id;
  var link = document.createElement("td");
  link.innerHTML = "<a href='http://twitter.com/" + account.id + "'>" + "@" + account.id + "</a>";
  var views = document.createElement("td");
  views.innerHTML = account.requested;
  row.appendChild(number);
  row.appendChild(imgCol);
  row.appendChild(name);
  row.appendChild(link);
  row.appendChild(views);
  return row;
}

var createClickHandler = function (row) {
  return function () {

    var cell = row.getElementsByTagName("td")[2];
    //console.log(cell.children[0].innerHTML)
    var name = cell.children[0].innerHTML.substring(1);
    
    window.location.href = "/graph?TwitterHandleInput=" + name;
    //var id = cell.innerHTML;
    //alert("id:" + id);
  };
};