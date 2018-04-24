var ADDR = "http://dsg1.crc.nd.edu"
var PORT = 5002;



function repopulate_rooms(){

    clear_rooms(); // TODO: write the code for this function
    
    var maxCap = document.getElementById("capRange").value;
    var maxSize = document.getElementById("sqftRange").value;
    get_data(ADDR + ":" + PORT + "/filter/netid/Zahm/"+maxCap+"/0/"+maxSize, populate_rooms);
}

function commit_preference(){
    /* TODO:
        This function should make a post request to the server 
        some data about the new preference (I'll add a format for this in a little).

        if the post request was successful:
            - add that data to the local queue variable
            - call function to re-populate the queue html
            - clear & close modal
        else:
            - issue sometime of error message to the user (netid not in dorm)
            - leave modal open for new input ???
    */
}

function save_queue(){

}

function save_modal(){

  commit_preference();  // TODO: write the code for this function
  //clear_modal();
}

function clear_modal(){
  var modal = document.getElementById("modal-body1");
  while (modal.firstChild) {
    modal.removeChild(modal.firstChild);
  } 
}

function clear_rooms(){
    var accordion = document.getElementById("panel");
    while (accordion.firstChild) {
        accordion.removeChild(accordion.firstChild);
    } 
}


var get_data = function(url, callback) // How can I use this callback?
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

var populate_modal = function(event){
    var parent = document.getElementById("modal-body1");
    var element;

    var capId = "cap" + event.target.id.substring(6,9);
    var cap = parseInt(document.getElementById(capId).innerText);
    for(var i=1; i<=cap-1; i++){
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

function populate_carousel(data){

    var floorPlans = JSON.parse(data);
    var dorm = floorPlans[0];
    var imagePath = "../../data/floorplans/" + dorm + "/";

    var carousel = document.getElementById("myCarousel");

    var ol = document.createElement("ol");
    ol.className = "carousel-indicators";
    carousel.insertBefore(ol, carousel.childNodes[0]);

    var inner = document.createElement("div");
    inner.className = "carousel-inner";
    carousel.insertBefore(inner, carousel.childNodes[0]);

    var parent;
    var element;
    for(var i=1; i<floorPlans.length; i++){
        imagePath = "../../data/floorplans/" + dorm + "/";
        imagePath = imagePath + floorPlans[i];

        // Indicator stuff
        parent = ol;    //Parent now ol
        element = document.createElement("li");
        if(i == 1){
            element.className = "active";
        }
        $(element).attr("data-target", "#myCarousel");
        $(element).attr("data-slide-to", (i-1).toString());
        parent.appendChild(element);

        //Slide Wrappers
        parent = inner;     //Parent now inner
        element = document.createElement("div");
        if(i == 1){
            element.className = "item active";
        } else{
            element.className = "item";
        }

        parent.appendChild(element);
        parent = element;

        element = document.createElement("img");
        element.src = imagePath;
        var floorString = "Floor " + i.toString();
        parent.appendChild(element);

        element = document.createElement("div");
        element.className = "carousel-caption";
        parent.appendChild(element);
        parent = element;

        element = document.createElement("h3");
        element.innerText = floorString;
        parent.appendChild(element);
    }
}

function populate_preference_queue(data){
    var jsonPrefs = JSON.parse(data);
    var prefsArr = jsonPrefs["preferences"];

    var queue = document.getElementById("queue");

    var parent;
    var element;


    parent = queue;
    // parent is now queue

    var table = document.createElement("table");
    element = table;
    element.className = "table table-striped header-fixed2 my-queue-table";
    parent.appendChild(element);
    parent = element;

    element = document.createElement("thead");
    element.className = "queue-header";
    parent.appendChild(element);
    parent = element;

    element = document.createElement("tr");
    element.className = "queue-header-text";
    parent.appendChild(element);
    parent = element;

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = "Room";
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = "Roommate 1";
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = "Roommate 2";
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = "Roommate 3";
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = " ";
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = " ";
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = " ";
    parent.appendChild(element);

    element = document.createElement("th");
    element.scope = "col";
    element.innerText = " ";
    parent.appendChild(element);

    parent = table;

    var tbody = document.createElement("tbody");
    element = tbody;
    parent.appendChild(element);

    var parent2;
    for(var i=0; i <prefsArr.length; i++){
        parent = tbody;     // parent is now tbody

        element = document.createElement("tr");
        parent.appendChild(element);
        parent = element;

        element = document.createElement("td");
        element.innerText = prefsArr[i]["room"];
        parent.appendChild(element); 

        element = document.createElement("td");
        element.innerText = prefsArr[i]["rm1"];
        parent.appendChild(element);

        element = document.createElement("td");
        element.innerText = prefsArr[i]["rm2"];
        parent.appendChild(element); 

        element = document.createElement("td");
        element.innerText = prefsArr[i]["rm3"];
        parent.appendChild(element); 

        element = document.createElement("td");
        parent.appendChild(element); 
        parent2 = parent;  // parent2 is the table row
        parent = element;  // parent is the table data

        element = document.createElement("button");
        element.className = "btn btn-primary";
        element.type = "button";
        element.title = "Move room up the queue";
        parent.appendChild(element);
        parent = element;   //parent is now the button 

        element = document.createElement("span");
        element.className = "glyphicon glyphicon-chevron-up"
        parent.appendChild(element); 

        parent = parent2;
        element = document.createElement("td");
        parent.appendChild(element); 
        parent = element;  // parent is the table data

        element = document.createElement("button");
        element.className = "btn btn-primary";
        element.type = "button";
        element.title = "Move room down the queue";
        parent.appendChild(element);
        parent = element;   //parent is now the button 

        element = document.createElement("span");
        element.className = "glyphicon glyphicon-chevron-down"
        parent.appendChild(element); 

        parent = parent2;   // parent is back to the table row
        element = document.createElement("td");
        parent.appendChild(element); 
        parent = element;  // parent is the table data

        element = document.createElement("button");
        element.className = "btn btn-success";
        element.type = "button";
        element.title = "Lock in this room";
        parent.appendChild(element);
        parent = element;   //parent is now the button 

        element = document.createElement("span");
        element.className = "glyphicon glyphicon-lock"
        parent.appendChild(element); 

        parent = parent2;   // parent is back to the table row
        element = document.createElement("td");
        parent.appendChild(element); 
        parent = element;  // parent is the table data

        element = document.createElement("button");
        element.className = "btn btn-danger";
        element.type = "button";
        element.title = "Remove room from queue";
        parent.appendChild(element);
        parent = element;   //parent is now the button 

        element = document.createElement("span");
        element.className = "glyphicon glyphicon-remove";
        parent.appendChild(element); 

    }

}

function populate_rooms(data) {
// replace these with actually data using endpoint
  var minFloor = 1;
  var floors = 3;
  var jsonRooms = JSON.parse(data);
  var roomsArr = jsonRooms["rooms"];
  var room;

  for(var i=1; i<=floors; i++){
    var floor = i.toString();
   
    // varying parent
    var accordion = document.getElementById("accordion");
    var parent = accordion;

    var panel = document.getElementById("panel");
    parent.appendChild(panel);
    parent = panel;

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
    parent = panel;  
    // parent is now accordion

    element = document.createElement("div");
    element.id = attrText;
    if(i == minFloor){
        element.className = "collapse in";
    }else{
         element.className = "collapse";
    }
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
    element.className = "room-header"
    parent.appendChild(element);
    parent = element;

    element = document.createElement("tr");
    element.className = "room-header-text";
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
    element.innerText = "";
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
    element.title = "Add room to queue";
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

  // populate the floor-buttons and rooms table
  get_data(ADDR + ":" + PORT + "/floors/netid/Zahm", populate_rooms);

  // populate floor plan images on carousel
  get_data(ADDR + ":" + PORT + "/floors/images/netid/fisher", populate_carousel);

  // populate the current users preference data
  get_data(ADDR + ":" + PORT + "/preferences/netid/Zahm", populate_preference_queue);

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


  $('[data-toggle="collapse"]').click(function() {
  $('.collapse.in').collapse('hide')
});

