var ADDR = "http://dsg1.crc.nd.edu"
var PORT = 5002;


function save_modal(){

  clear_modal();
}

function clear_modal(){
  var modal = document.getElementById("modal-body1");
  while (modal.firstChild) {
    modal.removeChild(modal.firstChild);
  } 
}

var populate_modal = function(event){
  var parent = document.getElementById("modal-body1");
  var element;

  var capId = "cap" + event.target.id.substring(6,9);
  var cap = parseInt(document.getElementById(capId).innerText);
  for(var i=1; i<=cap; i++){
    element = document.createElement("div");
    element.className = "form-group";
    parent.appendChild(element);
    parent = element;

    element = document.createElement("label");
    element.innerText = "Roommate " + i + ":";
    parent.appendChild(element);

    element = document.createElement("input");
    element.className = "form-control";
    element.id = "roommate" + cap;
    element.type ="text";
    parent.appendChild(element);
  }

}

var select_rooms = function(url, callback) // How can I use this callback?
{
    var request = new XMLHttpRequest();
    request.onreadystatechange = function()
    {
        if (request.readyState == 4 && request.status == 200)
        {
            callback(request.responseText); // Another callback here
        }
    }; 
    request.open('GET', url);
    request.send(null);
}

function populate_rooms(data) {
  var floors = 3;
  var jsonRooms = JSON.parse(data);
  var roomsArr = jsonRooms["rooms"];
  var room;

  for(var i=1; i<=floors; i++){
    var floor = i.toString();
   
    // varying parent
    var accordion = document.getElementById("accordion");
    var parent = accordion;

    var element = document.createElement("div");
    element.className = "mydiv";
    parent.appendChild(element);
    parent = element;

    element = document.createElement("h5");
    element.className = "mb-0";
    parent.appendChild(element);
    parent = element;

    /*
    element = document.createElement("h5");
    parent.appendChild(element);
    parent = element;
    */

    element = document.createElement("button");
    element.className = "btn btn-default floor-button";
    element.type = "button"
    $(element).attr("data-toggle", "collapse");
    var attrText = "collapse" + floor;
    $(element).attr("data-target", "#" + attrText);
    $(element).attr("aria-expanded" , "true");
    $(element).attr("aria-controls" , attrText);
    element.innerText = "Floor " + floor;
    parent.appendChild(element);
    parent = accordion;  
    // parent is now accordion

    element = document.createElement("div");
    element.id = attrText;
    element.className = "collapse";
    var headingText = "heading" + floor;
    $(element).attr("aria-labelledby" , headingText);
    $(element).attr("data-parent", "#accordion");
    parent.appendChild(element);
    parent = element;

    var table = document.createElement("table");
    element = table;
    element.className = "table table-striped header-fixed my-table";
    parent.appendChild(element);
    parent = element;

    element = document.createElement("thead");
    parent.appendChild(element);
    parent = element;

    element = document.createElement("tr");
    parent.appendChild(element);
    parent = element;
    // parent is now tr

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = "Room"
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = "Sqft."
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = "Occupants"
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = "Add to Queue"
    parent.appendChild(element);
    parent = table;
    // parent is now table

    element = document.createElement("tbody");
    element.id = "tbody" + floor;
    parent.appendChild(element);
    parent = element;

  }

  for(var i=0; i<roomsArr.length; i++){
    room = roomsArr[i];

        for(var j=1; j<=floors; j++){
          if(j == room["floor_num"]){
            parent = document.getElementById("tbody" + j);
          }
        }  
    
    element = document.createElement("tr");
    parent.appendChild(element);
    var parent2 = element;
    // parent is now tr

    element = document.createElement("td");
    element.innerText = room["room_num"];
    parent2.appendChild(element);

    element = document.createElement("td");
    element.innerText = room["size"];
    parent2.appendChild(element);

    element = document.createElement("td");
    element.id = "cap" + room["room_num"];
    element.innerText = room["capacity"];
    parent2.appendChild(element);

    element = document.createElement("td");
    var parent3 = element;
    element = document.createElement("button");
    element.className = "btn btn-primary";
    element.id = "button" + room["room_num"];
    element.type = "button";
    $(element).attr("data-target", "#GSCCModal");
    $(element).attr("data-toggle", "modal");
    element.innerText = " + ";
    element.onclick = populate_modal;
    parent3.appendChild(element);
    parent2.appendChild(parent3);
      
   }
}

  document.addEventListener("DOMContentLoaded", function() { 
    // this function runs when the DOM is ready

  //var jsonRooms = select_rooms();
  select_rooms(ADDR + ":" + PORT + "/floors/netid/Zahm", populate_rooms);

  var slider = document.getElementById("capRange");
  var output = document.getElementById("capValue");
  output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
  slider.oninput = function() {
    output.innerHTML = this.value;
}

  var slider2 = document.getElementById("sqftRange");
  var output2 = document.getElementById("sqftValue");
  output2.innerHTML = slider2.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
  slider2.oninput = function() {
    output2.innerHTML = this.value;
}


});

