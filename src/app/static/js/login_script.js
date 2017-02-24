/*
    Let's leave login scripts here to keep it organized
    and simple to modify
*/

/* I will remove this in the next version unless someone identifies why this is needed?
Shouldn't bootstrap automatically take care of the viewport?-Phil
$('#monitor').html($(window).width());
$(window).resize(function() {
    var viewportWidth = $(window).width();
    $('#monitor').html(viewportWidth);
});*/


function checkPasswordsMatch() {
	var password = $("#password").val();
    var confirmPassword = $("#reenterpassword").val();

    if (password != confirmPassword)
        $("#divCheckPasswordMatch").html("Passwords do not match!");
}


function onSignUpSubmit(aForm) {


	var inputPassword = aForm['password'];
	var inputReEnterPassword = aForm['reenterpassword'];

	if (inputPassword.value != inputReEnterPassword.value) {
		return false;
	} 

    //Hashing the value before submitting
    inputPassword.value = sha256_digest(inputPassword.value);
    inputReEnterPassword.value = sha256_digest(inputReEnterPassword.value);

    //Submitting
    return true;
}


function onLoginSubmit(aForm) {
	var inputPassword = aForm['password'];

    //Hashing the values before submitting
    inputPassword.value = sha256_digest(inputPassword.value);

    //Submitting
    return true;
}
