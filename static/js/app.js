
        //progressbar
        window.onscroll = function() {myFunction()};
function myFunction() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById("myBar").style.width = scrolled + "%";
}
//invert color
function InvertColor() {
  document.getElementById("Invert Color").style.filter = "invert(100%)";
}
//login
var attempt = 3; // Variable to count number of attempts.
// Below function Executes on click of login button.
function validate(){
var username = document.getElementById("username").value;
var password = document.getElementById("password").value;
var email = document.getElementById("email").value;
if ( username == "Hireability" && password == "Hireability#123"){
    if(email == "ps@gmail.com"){
alert ("Login successfully");
window.location = "resumeparser.html"; // Redirecting to other page.
return false;
}
}
else{
attempt --;// Decrementing by one.
alert("You have left "+attempt+" attempt;");
// Disabling fields after 3 attempts.
if( attempt == 0){
document.getElementById("username").disabled = true;
document.getElementById("password").disabled = true;
document.getElementById("email").disabled = true;
document.getElementById("submit").disabled = true;
return false;
}
}
}