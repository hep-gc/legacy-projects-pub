var widgets = require("widget")
var windows = require("windows").browserWindows
var tabs = require("tabs")
var self = require("self")
var {Cc, Ci} = require("chrome")

//The REST API server that provides certificate->privatekey conversion
//Note the HTTPS - this is a connection over SSL
const REST_API_URL = "https://142.104.60.47/cgi-bin/upload.py"
const REST_API_BORDER = "########PRIVATE KEY ENDS HERE - CERTIFICATE BEGINS HERE########"

var password_panel = require("panel").Panel({
   width: 470,
   height: 300,
   contentURL: self.data.url("panel.html"),
   contentScriptFile: [self.data.url("jquery-1.6.4.min.js"),
                       self.data.url("jquery.form.js"),
                       self.data.url("panel.js")]
});

password_panel.port.on("myEvent", function(data){
   console.log("Recieved Passwords from the panel form");
   password_panel.hide();
   
   var pairs = data.split("&");
   var values = [];

   for(var i = 0; i < pairs.length; i++){
      var tmp = pairs[i].split("=");
      values.push(tmp[0], tmp[1]);
   }
   
   //Lets assume nobody is messing with the script and these are actually coming from the form
   var pwd_in = decodeURIComponent(values[values.indexOf("pwd_in")+1]);
   var pwd_out_1 = decodeURIComponent(values[values.indexOf("pwd_out_1")+1]);
   var pwd_out_2 = decodeURIComponent(values[values.indexOf("pwd_out_2")+1]);
   
   if (pwd_out_1 != pwd_out_2 || pwd_out_1 == "" || pwd_in == ""){
      console.error("Missing/Mismatching passwords from the panel.");
      alert("Mismatching passwords from the panel, this shouldn't ever happen. Contact the developer.");
      return;
   }
   
   exportCert_and_Key(pwd_in, pwd_out_1);
   
});

var widget = widgets.Widget({
   id: "grid-cert-export",
   label: "Export Grid Canada Certificate",
   contentURL: self.data.url("key.png"),
   panel: password_panel
});

widget.on("click", function(){
   //Maybe open a new tab to HTTPS site immediately? (to accept security exception for SSL )
   });


function exportCert_and_Key(pkcs_pass, key_pass){
   
   var window = getActiveWindow();
      
   var cert = getGridCertificate(window);
   if(cert){
      certDB = getCertDB();
      
      //The directory in which the everything will go
      var dir = "";
      if(window.confirm("Save certificate, key, and PKCS12 backup in default directory (~/.globus)?\nWarning: This is will overwrite gridcert.p12, usercert.pem, and userkey.pem")){
         var home = Cc["@mozilla.org/file/directory_service;1"].getService(Ci.nsIProperties).get("Home", Ci.nsIFile);
         //Default directory to put exported certs is ~/.globus/
         home.append(".globus");
         dir = home;
         if(!dir.exists() || !dir.isDirectory()){
            dir.create(Ci.nsIFile.DIRECTORY_TYPE, 0770);
         }
         console.log("Default Directory Selected.");
      }
      else {
         var dir = pickFolder(window, "Save certificate, key, and PKCS12 backup files to:");
      }
      
      if(!dir){
         console.log("No directory picked");
         return;
      }
      
      //######Export the PKCS12####
      // In the future, should probably change the UI design, user already input .p12 password when saving it,
      // should just use that value...not sure how though :(
      var pkcs_file = dir.clone();
      pkcs_file.append("gridcert.p12");
      if(pkcs_file.exists()){
         //delete existing file (this is to check if user canceled during PKCS12 password prompt)
         pkcs_file.remove(true);
      }
      try{
         certDB.exportPKCS12File(null, pkcs_file, 1, [cert]);
      }
      catch(err){
         window.alert("Error Exporting: " + err.name);
      }
      if(pkcs_file.exists()){
         console.log("PKCS12 exported");
      }
      else{
         console.log("User canceled PKCS12 password prompt.");
         return;
      }
      
      //########Export the certificate and private key (using a REST API running on UVic servers)#####
      var boundary = "X-------------X" + Math.random();
      var multiStream = preparePOSTRequest(pkcs_pass, key_pass, pkcs_file, boundary);
      //Setup the POST request
      var req = Cc["@mozilla.org/xmlextras/xmlhttprequest;1"].createInstance(Ci.nsIXMLHttpRequest);
      req.open("POST", REST_API_URL, false);  //false makes this an asyncronous request
      req.setRequestHeader("Content-type", "multipart/form-data; boundary="+boundary);
      req.setRequestHeader("Content-length", multiStream.available());
      
      console.log("Sending request to " + REST_API_URL);
      //Send the request
      try{
         req.send(multiStream);
      }
      catch(err){
         console.exception(err);
         window.alert("There was an error sending the request.\n\
         Possible Causes:\n\
           -Can you connect to the server?\n\
           -Have you accepted the security exception? (Go to the https address first)");
         return;
      }
      
      console.log("Server Return Code: " + req.status);
    
      //test if an error in the conversion on the server-side
      regex = RegExp("error", "i");
      if(regex.test(req.responseText)){
         window.alert("Error Exporting: " + req.responseText);
      }
      else {
         //Create the appropriate files and write the data to them
         var key_file = dir.clone();
         key_file.append("userkey.pem");
         var cert_file = dir.clone();
         cert_file.append("usercert.pem");
         
         //The returned data from the REST API is in two sections seperated by REST_API_BORDER
         var split_data = req.responseText.split(REST_API_BORDER);
         
         var key_file_data = split_data[0];
         var cert_file_data = split_data[1];
         
         //Save the private key to disk with RESTRICTED permissions (600)
         try{
            saveToFile(window, key_file_data, key_file, 0600);
            saveToFile(window, cert_file_data, cert_file, 0644);
         }
         catch(err){
            window.alert("Error Exporting: " + err.name);
            return;
         }
         window.alert("Successfully exported certificate and key!");
      }
   }     
}

//Returns a nsIMultiplexStream of the correctly formatted API request
function preparePOSTRequest(pkcs_pass, key_pass, pkcs_file, post_boundary){
      
   //Buffer the upload file
   var inStream = Cc["@mozilla.org/network/file-input-stream;1"].createInstance(Ci.nsIFileInputStream);
   inStream.init(pkcs_file, 1, 1, inStream.CLOSE_ON_EOF);
   var bufInStream = Cc["@mozilla.org/network/buffered-input-stream;1"].createInstance(Ci.nsIBufferedInputStream);
   bufInStream.init(inStream, 4096);
   
   //Setup the start Boundery stream
   var boundary = post_boundary;
   var startBoundaryStream = Cc["@mozilla.org/io/string-input-stream;1"].createInstance(Ci.nsIStringInputStream);
   startBoundaryStream.setData("\r\n--"+boundary+"\r\n", -1);
   
   var boundaryStream1 = Cc["@mozilla.org/io/string-input-stream;1"].createInstance(Ci.nsIStringInputStream);
   var boundaryStream2 = Cc["@mozilla.org/io/string-input-stream;1"].createInstance(Ci.nsIStringInputStream);
   boundaryStream1.setData("\r\n--"+boundary+"\r\n", -1);
   boundaryStream2.setData("\r\n--"+boundary+"\r\n", -1);
   
   //Setup the end Boundery stream
   var endBoundaryStream = Cc["@mozilla.org/io/string-input-stream;1"].createInstance(Ci.nsIStringInputStream);
   endBoundaryStream.setData("\r\n--"+boundary+"--", -1);
   
   //Setup the "certificate" mime-stream
   var cert_mimeStream = Cc["@mozilla.org/network/mime-input-stream;1"].createInstance(Ci.nsIMIMEInputStream);
   cert_mimeStream.addContentLength = false;
   cert_mimeStream.addHeader("Content-disposition","form-data; name=\"certificate\"; filename=\""+pkcs_file.leafName+"\"");
   cert_mimeStream.addHeader("Content-type","application/octet-stream;");
   cert_mimeStream.setData(bufInStream);
   
   //Setup the "pwd_in" mime-stream
   var pwd_in_mimeStream = Cc["@mozilla.org/network/mime-input-stream;1"].createInstance(Ci.nsIMIMEInputStream);
   pwd_in_mimeStream.addContentLength = false;
   pwd_in_mimeStream.addHeader("Content-disposition", "form-data; name=\"pwd_in\"");
   var pwd_in_strStream = Cc["@mozilla.org/io/string-input-stream;1"].createInstance(Ci.nsIStringInputStream);
   pwd_in_strStream.setData(pkcs_pass, -1);
   pwd_in_mimeStream.setData(pwd_in_strStream);
   
   //Setup the "pwd_out" mime-stream
   var pwd_out_mimeStream = Cc["@mozilla.org/network/mime-input-stream;1"].createInstance(Ci.nsIMIMEInputStream);
   pwd_out_mimeStream.addContentLength = false;
   pwd_out_mimeStream.addHeader("Content-disposition", "form-data; name=\"pwd_out\"");
   var pwd_out_strStream = Cc["@mozilla.org/io/string-input-stream;1"].createInstance(Ci.nsIStringInputStream);
   pwd_out_strStream.setData(key_pass, -1);
   pwd_out_mimeStream.setData(pwd_out_strStream);
   
   //Setup the multiplex stream to combine the necessary streams
   var multiStream = Cc["@mozilla.org/io/multiplex-input-stream;1"].createInstance(Ci.nsIMultiplexInputStream);
   multiStream.appendStream(startBoundaryStream);
   multiStream.appendStream(cert_mimeStream);
   multiStream.appendStream(boundaryStream1);
   multiStream.appendStream(pwd_in_mimeStream);
   multiStream.appendStream(boundaryStream2);
   multiStream.appendStream(pwd_out_mimeStream);
   multiStream.appendStream(endBoundaryStream);
   
   return multiStream;
}


//Returns a reference to the currently active window
function getActiveWindow(){
   var windowMediator = Cc["@mozilla.org/appshell/window-mediator;1"].getService(Ci.nsIWindowMediator);
   var window = windowMediator.getMostRecentWindow(null);
   
   return window;
}


//Returns a reference to certificate database
function getCertDB(){
   return Cc["@mozilla.org/security/x509certdb;1"].createInstance(Ci.nsIX509CertDB);
}

//Given a name ("FirstName LastName"), seaches through user cert database looking for:
// 1) Grid Cert for that name, if no results
// 2) Any Grid Certificate
// 3) Null if nothing found
function getGridCertificate(window) {
   certDB = getCertDB();
   
   var certString = "";
   var count = new Object();
   var certNames = new Object();
   certDB.findCertNicknames(null, Ci.nsIX509Cert.USER_CERT, count, certNames);
   console.log("Searching through " + certNames.value.length + " certificates.");

   for(var i = 0;i < count.value; i++){
      //console.log("CertNames.value[" + i + "]: " + certNames.value[i]);
      if(certNames.value[i].match(".*Grid ID.*")){
         console.log("Grid ID found, maybe correct?");
         if(window.confirm("A Grid ID was found: \"" + certNames.value[i].split(certNames.value[i][0])[1] + "\"\n\nDo you want this one? (Cancel to continue searching)")){
            certString = certNames.value[i];
            break;
         }
      }
   }
   
   //Search was not succesfull
   if(!certString) {
    console.log("No cert found at all, I give up.");
    window.alert("No Grid Certificate Found in the Firefox Certificate Store\nGet the certificate from https://cert.gridcanada.com or import from backup PKCS12");
    return null;
   }
   
   var certStringSplit = certString.split(certString[0]);
   //NOTE: certStringSplit[1] = nickname (or email sometimes), certStringSplit[2] = dbKey
   return certDB.findCertByDBKey(certStringSplit[2], null);
}

//Saves data to file, appending. Prompts for location and name, returns true if succesful
//File paramater is optional, prompts if null
function saveToFile(window, data, file, permissions){
   if(!file){
      file = pickFileToSave(window, "Save to:", ".txt", "");
   }
   if(file){
     //Create the nsIFileOutputStream Object
     var foStream = Cc["@mozilla.org/network/file-output-stream;1"].createInstance(Ci.nsIFileOutputStream);
     //0x02 = write, 0x20 = overwrite, 0x08 = create, 0775 style file permissions (UNIX only)
     //see docs: https://developer.mozilla.org/en/PR_Open#Parameters
     foStream.init(file, 0x02 | 0x20 | 0x08, permissions, 0);
     foStream.write(data, data.length);
     foStream.close();
     return true;
   }
   return false;
}

//Prompts user to pick a file (*.*) and returns a nsIFile reference, or null otherwise
function pickFileToSave(window, title, extension, defaultFilename){
   var filePicker = Cc["@mozilla.org/filepicker;1"].createInstance(Ci.nsIFilePicker);
   filePicker.init(window, title, Ci.nsIFilePicker.modeSave);
   filePicker.appendFilter(extension, "*" + extension);
   filePicker.appendFilter("All Files", "*.*");
   
   //Make the file picker open up in the home directory of user
   filePicker.displayDirectory = Cc["@mozilla.org/file/directory_service;1"].getService(Ci.nsIProperties).get("Home", Ci.nsIFile);
   filePicker.defaultExtension = extension;
   filePicker.defaultString = defaultFilename;
   
   //Open up the file picker (return values of: returnOK, returnCancel, returnReplace)
   var rv = filePicker.show();
   
   if(rv == Ci.nsIFilePicker.returnOK || rv == Ci.nsIFilePicker.returnReplace){
     console.log("File was picked");
     var file = filePicker.file;
     console.log("File path chosen: " + file.path);
   }
   else{
       console.log("File was NOT picked!");
       file = null;
   }
   
   return file;
}

//Prompts user to pick a Folder and returns a nsIFile reference, or null otherwise
function pickFolder(window, title){
   var filePicker = Cc["@mozilla.org/filepicker;1"].createInstance(Ci.nsIFilePicker);
   filePicker.init(window, title, Ci.nsIFilePicker.modeGetFolder);
      
   //Make the file picker open up in the home directory of user
   filePicker.displayDirectory = Cc["@mozilla.org/file/directory_service;1"].getService(Ci.nsIProperties).get("Home", Ci.nsIFile);
    
   //Open up the file picker (return values of: returnOK, returnCancel, returnReplace)
   var rv = filePicker.show();
   
   if(rv == Ci.nsIFilePicker.returnOK || rv == Ci.nsIFilePicker.returnReplace){
     console.log("Folder was picked");
     var file = filePicker.file;
     console.log("Path chosen: " + file.path);
   }
   else{
       console.log("Folder was NOT picked!");
       file = null;
   }
   
   return file;
}
