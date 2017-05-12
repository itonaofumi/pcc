function addValue(event) {
  var parent_object = document.getElementById(event.currentTarget.id);
  parent_object.firstElementChild.innerHTML = " / CC: " + event.data[1]
    + " Value: " + event.data[2];
}

function addList(id, name) {
  var li_element = document.createElement("li");
  li_element.id = id;
  li_element.innerHTML = id + ' : ' + name;
  var parent_object = document.getElementById("devices");
  parent_object.appendChild(li_element);

  var span_element = document.createElement("span");
  parent_object = document.getElementById(id);
  parent_object.appendChild(span_element);
}

const ipc = require('electron').ipcRenderer
function onMIDIMessage(event) {
  // console.log(event);
  // console.log("CC: " + event.data[1] + " Value: " + event.data[2]);
  addValue(event);

  // Send event data to main.js
  ipc.send('asynchronous-message', event.data)
}

function startLoggingMIDIInput(midiAccess, indexOfPort) {
  midiAccess.inputs.forEach(function (entry) {
    entry.onmidimessage = onMIDIMessage;
  });
}

function listInputsAndOutputs(midiAccess) {
  for (var entry of midiAccess.inputs) {
    //console.log(entry);
    var input = entry[1];
    startLoggingMIDIInput(midiAccess, input.id);
    addList(input.id, input.name);
  }
}

function onMIDISuccess(midiAccess) {
  listInputsAndOutputs(midiAccess);
}

function onMIDIFailure(mst) {
  console.log('Failed to get MIDI access - ' + msg);
}

navigator.requestMIDIAccess().then(onMIDISuccess, onMIDIFailure);