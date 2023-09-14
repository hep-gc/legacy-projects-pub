$('#password_form').submit(function() {
    
    //sends the submit to the Firefox Addon Script
    self.port.emit("myEvent", $(this).serialize());
    
    //prevents the actual submittion
    return false;  
});