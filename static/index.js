
// document.getElementById("start_program").addEventListener("click", startProgram);
// function startProgram() {
//   console.log("Start")
//   document.getElementById("myForm").action = "/run_script";
// }





// var btnCal = document.getElementById('btnCal');

// console.log(btnCal)

// function showMessage() {
// 	message.innerHTML = 'Test Doo';
// 	console.log('Test Doo');
// 	console.log(document.getElementById('input-box').value);
// 	var inputbox = document.getElementById('input-box').value
	
// 	var text = ''
// 	for(let i = 1; i <= 12;i++){
// 		text += String(i) + ' * ' + String(inputbox) + ' = ' + String(i*inputbox) + '<br>'
		
// 		console.log(text)
// 	}
// 	message.innerHTML = text
// }

// btnCal.addEventListener('click', showMessage);


function ValidateFile(){
    var input, file, extension;

    input = document.getElementById('dol_qrcode');
    file = input.files[0];
    extension = file.name.split('.').pop().toLowerCase() //Check file extension
    if(extension != 'png' ){
        // document.getElementById('message').innerHTML =  "File " + file.name + " is " + file.size + " bytes in size" + extension;
        document.getElementById('message').innerHTML = "File extension is not PNG"
        document.getElementById('message').removeAttribute('hidden')
        return false;
    }
    return true;
}