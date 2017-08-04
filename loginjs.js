var email = document.getElementById('email');
var password = document.getElementById('password');
var bsignin = document.getElementById('login');

bsignin.addEventListener('click', e => {

	var mail = email.value;
	var pass = password.value;

	var auth = firebase.auth();

	var promise = auth.signInWithEmailAndPassword(mail, pass);

	promise.catch(function(error) {

		var errorcode = error.code;
		var errormes = error.message;
		console.log(errormes+ "code"+errorcode);
	});
});

firebase.auth().onAuthStateChanged(firebaseUser => {
	if(firebaseUser){
		console.log(firebaseUser);

		window.location="welcome.html";
	}else{
		console.log("not logged in");
	}
});
	