var ADDR = "http://dsg1.crc.nd.edu"
var PORT = 5002;

var roomClicked = "";
var queueSize = 0;

var NETID = localStorage.netid;
var DORM_NAME = localStorage.dorm_name;

function repopulate_rooms(){

    clear_rooms(); // TODO: write the code for this function
    
    var maxCap = document.getElementById("capRange").value;
    var maxSize = document.getElementById("sqftRange").value;
    get_data(ADDR + ":" + PORT + "/filter/netid/Zahm/"+maxCap+"/0/"+maxSize, populate_rooms);
}

function repopulate_queue(pref_num1, pref_num2){
    clear_queue();
    send_data(
                'PUT',
                ADDR + ":" + PORT + "/preferences/ktong1/Fisher", 
                "{ pref_num1:"+pref_num1+", pref_num2:"+pref_num2+" }",
                get_data,
                [ADDR + ":" + PORT + "/preferences/ktong1/Fisher", populate_preference_queue]
            );
}

function delete_preference(pref_num){
    clear_queue();
    send_data(
                'DELETE',
                ADDR + ":" + PORT + "/preferences/ktong1/Fisher", 
                "{ pref_num:"+pref_num+" }",
                get_data,
                [ADDR + ":" + PORT + "/preferences/ktong1/Fisher", populate_preference_queue]
            );
}

function commit_preference(){
    var pref = [];

    var modal_body = document.getElementById("modal-body1");
    var num_roommates = modal_body.childElementCount;
    var rm_base = "rm";
    var rm_tmp = "";
    var input = "";
    var dict = {
            "netID": "ktong1",
            "pref_num": queueSize+1, 
            "room_num": roomClicked,
            "dorm_name": "Fisher",
        };

    for(var i=0; i < num_roommates; i++){
        rm_tmp = rm_base + (i+1).toString();
        input = document.getElementById(rm_tmp).value;
        dict[rm_tmp] = input; 
    }


    pref.push(dict);
    var result = {
        "preferences": pref
    };
    console.log(JSON.stringify(result));

    send_data('POST', ADDR + ":" + PORT + "/preferences/ktong1/Fisher", JSON.stringify(result), get_data,  [ADDR + ":" + PORT + "/preferences/ktong1/Fisher", populate_preference_queue]);

}
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

function save_modal(){
  clear_queue();
  commit_preference();  // TODO: write the code for this function
  clear_modal();
}

function clear_modal(){
  var modal = document.getElementById("modal-body1");
  while (modal.firstChild) {
    modal.removeChild(modal.firstChild);
  } 
}

function clear_rooms(){
    var panel = document.getElementById("panel");
    while (panel.firstChild) {
        panel.removeChild(panel.firstChild);
    } 
}

function clear_queue(){
    var queue = document.getElementById("queue");
    while (queue.firstChild) {
        queue.removeChild(queue.firstChild);
    } 
}

var send_data = function(type, url, data, callback, args)
{
    var request = new XMLHttpRequest();
    request.onreadystatechange = function()
    {
        if (request.readyState == 4 && request.status == 200)
        {
            callback(args[0], args[1]);
        }
    }; 
    request.open(type, url);
    request.send(data);
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
    var modal_body = document.getElementById("modal-body1");
    var parent;
    var element;

    // sets global var for later use
    roomClicked = event.target.id.substring(6,9);
    var capId = "cap" + roomClicked;
    
    var cap = parseInt(document.getElementById(capId).innerText);
    for(var i=1; i<=cap-1; i++){
        parent = modal_body;

        element = document.createElement("div");
        element.className = "form-group";
        parent.appendChild(element);
        parent = element;

        element = document.createElement("label");
        element.innerText = "Roommate " + i + ":";
        parent.appendChild(element);

        element = document.createElement("input");
        element.className = "form-control";
        element.id = "rm" + i;
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
        $(element).attr("id", imagePath); // set img id to the image path so I can get it in zoom modal
        element.onclick = function(){ zoom_in_img(imagePath); }
        var floorString = "Floor " + i.toString();
        element.alt = floorString;
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
    queueSize = prefsArr.length;

    var queue = document.getElementById("queue");

    var parent;
    var element;


    parent = queue;
    // parent is now queue

    //<h4 id="queue-title"> Preference Queue </h4>
    var queueTitle = document.createElement("h4");
    queueTitle.id = "queue-title";
    queueTitle.innerHTML = " Preference Queue ";
    parent.appendChild(queueTitle);

    var table = document.createElement("table");
    element = table;
    element.className = "table table-striped header-fixed2 my-queue-table";
    element.id = "queue_table_id";
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
    for(var i=0; i < queueSize; i++){
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
        if(i == 0){
            element.disabled = true;
        }
        element.className = "btn btn-primary";
        element.type = "button";
        element.title = "Move room up the queue";
        // i+1 is the actual pref num since this loop starts at i=0
        $(element).attr("onclick", "repopulate_queue("+(i+1).toString()+", "+i.toString()+")");
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
        if(i == prefsArr.length-1){
            element.disabled = true;
        }
        element.className = "btn btn-primary";
        element.type = "button";
        element.title = "Move room down the queue";
        $(element).attr("onclick", "repopulate_queue("+(i+1).toString()+", "+(i+2).toString()+")");
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
        element.onclick = function(){ delete_preference(i+1); } // i starts at 0, prefs start at 1, so i+1 = real pref_num
        $(element).attr("onclick", "delete_preference("+(i+1).toString()+")");
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

function zoom_in_img(imgId){
    var modal = document.getElementById("myModal");
    var panel = document.getElementsByClassName("item active")[0];
    var img = panel.childNodes[0];
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");
    
    modal.style.display = "block";
    modalImg.src = img.src;
    captionText.innerHTML = img.alt;
    
    var span = document.getElementsByClassName("close")[1];
    span.onclick = function(){
        modal.style.display = "none";
    }
}


  document.addEventListener("DOMContentLoaded", function() { 
    // this function runs when the DOM is ready

  // populate the floor-buttons and rooms table
  get_data(ADDR + ":" + PORT + "/floors/netid/Zahm", populate_rooms);

  // populate floor plan images on carousel
  get_data(ADDR + ":" + PORT + "/floors/images/netid/fisher", populate_carousel);

  // populate the current users preference data
  get_data(ADDR + ":" + PORT + "/preferences/ktong1/Fisher", populate_preference_queue);

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
