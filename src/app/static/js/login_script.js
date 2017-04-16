
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
    //inputPassword.value = sha256_digest(inputPassword.value);
    //inputReEnterPassword.value = sha256_digest(inputReEnterPassword.value);

    //Submitting
    return true;
}


