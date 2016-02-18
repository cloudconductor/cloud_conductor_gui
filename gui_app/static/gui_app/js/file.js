function read (ele, id, mid) {
  target = document.getElementById(mid);

    if (!ele.files.length) return; // File unselected

    var file = ele.files[0];
  var fr = new FileReader();

    fr.onload = function () {
      if (!isJson(fr.result)){
        target.innerHTML = "NG Json format.";
        return ;
      }
      document.getElementById(id).value = fr.result;  // The contents of the file textarea to the output
        target.innerHTML = "OK Json format.";  // Output a message.
    };
    fr.readAsText(file);  // Loading files
}

function json_check (id, mid){
  target = document.getElementById(mid);

  if(isJson(document.getElementById(id).value)){
    target.innerHTML = "OK Json format.";
  } else {
    target.innerHTML = "NG Json format";
  }
  return ;
}

var isJson = function(arg){
    arg = (typeof(arg) == "function") ? arg() : arg;
    if(typeof(arg) != "string"){return false;}
    try{arg = (!JSON) ? eval("(" + arg + ")") : JSON.parse(arg);return true;}catch(e){return false;}
};
