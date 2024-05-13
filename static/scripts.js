// removes duplicate options from the dropdown menus
function remDupe(id) {
	var selectElement = document.getElementById(id);
	var i, L = selectElement.options.length - 1;
	for (i = L; i >= 0; i--) {
		if (selectElement[i].value === selectElement[0].value) {
			selectElement.remove(i);
			return 0;
		}
	}
}

// checks if the screen is a phone
function isPhone() {
	x = window.innerWidth || document.documentElement.clientWidth;
	
	if (x <= 450) { return true }
	else { return false }
}

// remember the status of the checkbox using cookies
function checkBoxStatus(id, theCheck) { if (theCheck == 'true') { document.getElementById(id).checked = true; } }

// highlights the text when the user selects a text input
function selectTextListener(id) { document.getElementById(id).addEventListener('focus', () => document.getElementById(id).select()); }
	
// if a toggle is clicked it updates the state 
function updateStateListener(id) { document.getElementById(id).addEventListener('click', () => updateState()); }

// toggles the options container 
function toggleOptions() {
	var togOptions = document.getElementById('togOptions');
	var togWrap = document.getElementById('togWrapper');
	
	if (togOptions.checked) { togWrap.style.setProperty('display', 'block'); }

	else { togWrap.style.setProperty('display', 'none'); }
}

// specialization option 
function toggleSpecialization() {
	var checkBox = document.getElementById('specToggle');
	var specInput = document.getElementById('specInput');
	var spec = document.getElementById('spec');
	
	
	if (checkBox.checked) {
		specInput.value = specName;
		spec.style.setProperty('display', 'block');
	}
	
	else {
		specInput.value = '';
		spec.style.setProperty('display', 'none');
	}
}

// raider.io option 
function toggleRio() {
	var checkBox = document.getElementById('rioToggle');
	
	var rio = document.getElementById('rio');
	var rioInp = document.getElementById('rioInput');
	
	var serv = document.getElementById('serv');
	var servInp = document.getElementById('servInput');
	
	var chara = document.getElementById('char');
	var charaInp = document.getElementById('charInput');
	
	var pasteRioCont = document.getElementById('pasteRioCont');
	
	
	if (checkBox.checked) {
		rioInp.value = rioInfo;
		rio.style.setProperty('display', 'block');
		
		servInp.value = '';
		serv.style.setProperty('display', 'none');
		
		charaInp.value = '';
		chara.style.setProperty('display', 'none');
		
		pasteRioCont.style.setProperty('display', 'block');
	}
	
	else {
		rioInp.value = '';
		rio.style.setProperty('display', 'none');
		
		servInp.value = servName;
		serv.style.setProperty('display', 'block');
		
		charaInp.value = charName;
		chara.style.setProperty('display', 'block');
		
		pasteRioCont.style.setProperty('display', 'none');
		
		document.getElementById('pasteRioToggle').checked = false;
	}
	
	togglePasteRio();
}

// autorun on paste option 
function onPaste() { window.setTimeout(() => { document.getElementById('runBtn').click(); }, 1) }
function togglePasteRio() {

	togPasteBox = document.getElementById('pasteRioToggle');
	rioInput = document.getElementById('rioInput');
	submitForm = document.getElementById('submitForm');
	
	if (togPasteBox.checked) { 
		rioInput.addEventListener('paste', onPaste); 
		submitForm.target = '_blank';
	}
	
	else { 
		rioInput.removeEventListener('paste', onPaste); 
		submitForm.target = '';
	}

}

// checks the state of the checkboxes and updates the screen accordingly 
function updateState() {

	var specBox = document.getElementById('specToggle');
	var rioBox = document.getElementById('rioToggle');
	
	var charCont = document.getElementById('char');
	var servCont = document.getElementById('serv');
	var specCont = document.getElementById('spec');
	var metCont = document.getElementById('met');
	var keyCont = document.getElementById('keyLvl');
	
	var grid = document.getElementById('theGrid');
	var optGrid = document.getElementById('togWrapper');
	
	phone = isPhone();
	
	// both boxes == checked
	if (specBox.checked && rioBox.checked) {
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'. .' 'rio rio' 'specInput specInput' 'metricDDW metricDDW' 'keyLvlDDW keyLvlDDW' '. .' 'runButton runButton'");
			
			optGrid.style.setProperty('height', '13.75vw');
		}

		if(!phone) {
			grid.style.setProperty('grid-template-areas', "'. .' 'rio rio' 'metricDDW keyLvlDDW' 'specInput runButton' '. .' '. .' '. .'");
			optGrid.style.setProperty('height', '5.25vw');
		}

	}
	
	// rioBox == checked
	else if (rioBox.checked) {
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'. .' 'rio rio' 'metricDDW metricDDW' 'keyLvlDDW keyLvlDDW' '. .' '. .' 'runButton runButton'");
			
			optGrid.style.setProperty('height', '13.75vw');
		}
		
		else if (!phone) {
			grid.style.setProperty('grid-template-areas', "'. .' 'rio rio' 'metricDDW keyLvlDDW' 'runButton runButton' '. .' '. .' '. .'");
			optGrid.style.setProperty('height', '5.25vw');
		}
	
	}
	
	// specBox == checked
	else if (specBox.checked) {
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'. .' 'charInput charInput' 'servInput servInput' 'specInput specInput' 'metricDDW metricDDW' 'keyLvlDDW keyLvlDDW' 'runButton runButton'");
			
			optGrid.style.setProperty('height', '9.5vw');
		}
	
		else if (!phone) {
			grid.style.setProperty('grid-template-areas', "'. .' 'charInput metricDDW' 'servInput keyLvlDDW' 'specInput runButton' '. .' '. .' '. .'");	
			optGrid.style.setProperty('height', '3.5vw');
		}
		
	}
	
	// default grid-template-areas
	else {
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'. .' 'charInput charInput' 'servInput servInput' 'metricDDW metricDDW' 'keyLvlDDW keyLvlDDW' '. .' 'runButton runButton'");
			
			optGrid.style.setProperty('height', '9.5vw');
		}
		
		else if (!phone) {
			grid.style.setProperty('grid-template-areas', "'. .' 'charInput metricDDW' 'servInput keyLvlDDW' 'runButton runButton' '. .' '. .' '. .'");
			optGrid.style.setProperty('height', '3.5vw');
		}
	}


}

// used to submit form
function submit(formId) {
	document.getElementById(formId).submit();
}

// changes the color of the parse based on percentile
function parseColor(parse, id) {
	var x = document.getElementById(id);
	var parseNumber = Number(parse);
	if (parseNumber <= 24) {
		x.style.color = '#889D9D';
	}
	else if (parseNumber >= 25 && parseNumber <= 49) {
		x.style.color = '#1EFF0C';
	}
	else if (parseNumber >= 50 && parseNumber <= 74) {
		x.style.color = '#0070FF';
	}
	else if (parseNumber >= 75 && parseNumber <= 94) {
		x.style.color = '#A335EE';
	}
	else if (parseNumber >= 95 && parseNumber <= 98) {
		x.style.color = '#FF8000';
	}
	else if (parseNumber == 99) {
		x.style.color = '#FF7EFF';
	}
	else if (parseNumber == 100) {
		x.style.color = '#E6CC80';
	}
}


// detects the number of specs and makes buttons based on specs found
function specChoice() {
	
	specList = specList.replace(/&#39;| /g, '');
	specList = specList.slice(1,-1);
	specList = specList.split(',');
	specList.sort();
	
	if (specList.length > 1) {
		specChoice = document.getElementById('specChoice');
		spec0 = document.getElementById('specBtn0');
		spec1 = document.getElementById('specBtn1');
		spec2 = document.getElementById('specBtn2');
		spec3 = document.getElementById('specBtn3');
		
		//const specList = specName.split(' &amp; ');
		
		// there will always be a minimum of 2 specs if this triggers
		spec0.value = specList[0];
		spec1.value = specList[1];
		spec0.style.setProperty('display', 'block');
		spec1.style.setProperty('display', 'block');
		
		specChoice.style.setProperty('height', '5.75vw');
		
		if (specList.length > 2) {
			
			spec2.value = specList[2];
			spec2.style.setProperty('display', 'block');
			specChoice.style.setProperty('height', '7.7vw');
			
			if (specList.length > 3) {
				spec3.value = specList[3];
				spec2.style.setProperty('display', 'block');
				specChoice.style.setProperty('height', '9.75vw');
			}
		}
		
		specChoice.style.setProperty('display', 'block');
	}
	
}

// sets the spec to be queried based on the button pressed
function setSpecChoice(id) {
	specClicked = document.getElementById(id);
	newSpec = document.getElementById('newSpec');
	
	newSpec.value = specClicked.value;
	
	submit('specForm');
}