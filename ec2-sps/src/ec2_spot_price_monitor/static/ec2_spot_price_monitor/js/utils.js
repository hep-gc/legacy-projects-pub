/*
 * Create by r desmarais
 */
function JSONMessageFactory(){
	this.createMessage = function(vm_types,instance_types,regions,zones,response_type,request_type,filter_type,args){
		jsonData_VM = JSON.stringify(vm_types);
		jsonData_INST = JSON.stringify(instance_types);
		jsonData_REGIONS = JSON.stringify(regions);
		jsonData_ZONES = JSON.stringify(zones);
		
    	return '{"filter_type":"'+filter_type+'","response_type":"'+response_type+'","request":"'+request_type+'","other_args":'+args+',"request_args":[{"ImageTypes":'+jsonData_VM+'},{"InstanceTypes":'+jsonData_INST+'},{"Regions":'+jsonData_REGIONS+'},{"ZONES":'+jsonData_ZONES+'}  ] }';
	}
}

function HTTPUtils()
{
  this.sendViaPOST=function(httpReq,url,jsonMsg,callback){
    console.log("Try to Send JSON Req");
	httpReq.onreadystatechange=callback;
	httpReq.open("POST",url,true);
	httpReq.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	httpReq.send("jsonMsg="+jsonMsg);
  }
  
  this.sendViaGET=function(httpReq,url,jsonMsg,callback){
    console.log("Try to Send JSON Req");
	httpReq.onreadystatechange=callback;
	httpReq.open("GET",url+'/?jsonmsg='+jsonMsg+'&',true);
	//httpReq.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	httpReq.send(null);
  }
  
  this.CreateHttpObject=function(){
	if (window.XMLHttpRequest)
	  {
	  // code for IE7+, Firefox, Chrome, Opera, Safari
	  return new XMLHttpRequest();
	  }
	if (window.ActiveXObject)
	  {
	  // code for IE6, IE5
	  return new ActiveXObject("Microsoft.XMLHTTP");
	  }
	return null;
  }
}