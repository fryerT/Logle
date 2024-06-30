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
	var togWrap = document.getElementById('togGrid');
	
	if (togOptions.checked) { togWrap.style.setProperty('display', 'grid'); }

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
	runBtn = document.getElementById('runBtn');
	
	if (togPasteBox.checked) { 
		rioInput.addEventListener('paste', onPaste);
		runBtn.style.setProperty('display', 'none');
		//submitForm.target = '_blank';
	}
	
	else { 
		rioInput.removeEventListener('paste', onPaste); 
		runBtn.style.setProperty('display', 'block');
		//submitForm.target = '';
	}

}

// avoidable deaths option
function toggleAvoidableDeaths() {

	avoidableDeathsBox = document.getElementById('avoidableDeathsToggle');
	
	specBox = document.getElementById('specToggle');
	specCont = document.getElementById('specCont');
	specInp = document.getElementById('spec');
	
	rioBox = document.getElementById('rioToggle');
	rioCont = document.getElementById('rioCont');
	rioInp = document.getElementById('rio');
	
	pasteRioBox = document.getElementById('pasteRioToggle');
	pasteRioCont = document.getElementById('pasteRioCont');
	
	keyLvlInp = document.getElementById('keyLvl');
	
	metricInp = document.getElementById('met');
	
	charInp = document.getElementById('char');
	
	servInp = document.getElementById('serv');
	
	runBtn = document.getElementById('runBtn');
	
	if (avoidableDeathsBox.checked) {
		
		// hide the other checkboxes
		specCont.style.setProperty('display', 'none');
		// rioCont.style.setProperty('display', 'none');
		// pasteRioCont.style.setProperty('display', 'none');
		
		
		// hide the inputs
		specInp.style.setProperty('display', 'none');
		// rioInp.style.setProperty('display', 'none');
		keyLvlInp.style.setProperty('display', 'none');
		metricInp.style.setProperty('display', 'none');
		
		
		// show character input, server input, and run button in case they were hidden prior
		if (charInp.style.display == 'none') { charInp.style.setProperty('display', 'block'); }
		if (servInp.style.display == 'none') { servInp.style.setProperty('display', 'block'); }
		if (runBtn.style.display == 'none') { runBtn.style.display = 'block'; }
		
		// disable all other check boxes
		specBox.checked = false;
	}
	
	else { 
		// unhide the other checkboxes minus rioPaste since it depends on rio being checked
		specCont.style.setProperty('display', 'block');
		rioCont.style.setProperty('display', 'block');
		
		// unhide the inputs except rio and spec since they depend on their togs
		keyLvlInp.style.setProperty('display', 'block');
		metricInp.style.setProperty('display', 'block');
	}

	toggleRio();

	return 0
}

// checks the state of the checkboxes and updates the screen accordingly 
function updateState() {
	
	var specBox = document.getElementById('specToggle');
	var rioBox = document.getElementById('rioToggle');
	var avoidableDeathsBox = document.getElementById('avoidableDeathsToggle');
	
	var charCont = document.getElementById('char');
	var servCont = document.getElementById('serv');
	var specCont = document.getElementById('spec');
	var metCont = document.getElementById('met');
	var keyCont = document.getElementById('keyLvl');
	
	var grid = document.getElementById('contGrid');
	var optGrid = document.getElementById('togGrid');
	
	var phone = isPhone();
	
	var phoneSize = 4.5;
	var size = 1.75;
	
	if (avoidableDeathsBox.checked && rioBox.checked) {
		
		const boxHeight = 3;
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'rio rio' '. .' '. .' '. .' '. .' 'runButton runButton' '. .' 'desc desc'");
			
			optGrid.style.height = String(phoneSize * boxHeight) + 'vw';
		}
		
		else if (!phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'rio rio' 'runButton runButton' '. .' '. .' '. .' 'desc desc'");
			
			optGrid.style.height = String(size * boxHeight) + 'vw';
		}
		
	}
	
	// both boxes == checked
	else if (specBox.checked && rioBox.checked) {
		
		const boxHeight = 4;
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'rio rio' 'specInput specInput' 'metricDDW metricDDW' 'keyLvlDDW keyLvlDDW' '. .' 'runButton runButton' '. .' 'desc desc'");
			
			optGrid.style.height = String(phoneSize * boxHeight) + 'vw';
		}

		if(!phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'rio rio' 'metricDDW keyLvlDDW' 'specInput runButton' '. .' '. .' 'desc desc'");
			optGrid.style.height = String(size * boxHeight) + 'vw';
		}

	}
	
	// rioBox == checked
	else if (rioBox.checked) {
		
		const boxHeight = 4;
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'rio rio' 'metricDDW metricDDW' 'keyLvlDDW keyLvlDDW' '. .' '. .' 'runButton runButton' '. .' 'desc desc'");
			
			optGrid.style.height = String(phoneSize * boxHeight) + 'vw';
		}
		
		else if (!phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'rio rio' 'metricDDW keyLvlDDW' 'runButton runButton' '. .' '. .' 'desc desc'");
			optGrid.style.height = String(size * boxHeight) + 'vw';
		}
	
	}
	
	// specBox == checked
	else if (specBox.checked) {
		
		const boxHeight = 3;
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'charInput charInput' 'servInput servInput' 'specInput specInput' 'metricDDW metricDDW' 'keyLvlDDW keyLvlDDW' 'runButton runButton' '. .' 'desc desc'");
			
			optGrid.style.height = String(phoneSize * boxHeight) + 'vw';
		}
	
		else if (!phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'charInput metricDDW' 'servInput keyLvlDDW' 'specInput runButton' '. .' '. .' 'desc desc'");	
			optGrid.style.height = String(size * boxHeight) + 'vw';
		}
		
	}
	
	else if (avoidableDeathsBox.checked) {
		
		const boxHeight = 2;
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'charInput charInput' 'servInput servInput' '. .' '. .' '. .' 'runButton runButton' '. .' 'desc desc'");
			
			optGrid.style.height = String(phoneSize * boxHeight) + 'vw';
		}
		
		else if (!phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'charInput servInput' 'runButton runButton' '. .' '. .' '. .' 'desc desc'");	
			optGrid.style.height = String(size * boxHeight) + 'vw';
		}
	}
	
	// default grid-template-areas
	else {
		
		const boxHeight = 3;
		
		if (phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'charInput charInput' 'servInput servInput' 'metricDDW metricDDW' 'keyLvlDDW keyLvlDDW' '. .' 'runButton runButton' '. .' 'desc desc'");
			
			optGrid.style.height = String(phoneSize * boxHeight) + 'vw';
		}
		
		else if (!phone) {
			grid.style.setProperty('grid-template-areas', "'headerTxt headerTxt' '. .' 'charInput metricDDW' 'servInput keyLvlDDW' 'runButton runButton' '. .' '. .' 'desc desc'");
			optGrid.style.height = String(size * boxHeight) + 'vw';
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
		specChoice = document.getElementById('specChoiceGrid');
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
		
		specChoice.style.setProperty('display', 'grid');
	}
	
}

// sets the spec to be queried based on the button pressed
function setAndSubmit(itemId, formId, textBoxId) {
	document.getElementById(textBoxId).value = document.getElementById(itemId).value;
	document.getElementById(formId).submit();
}

// sets the current metric type and key level queried
function showQueriedOptions() {
	
	var queryData = characterData.replace(/&#39;| /g, '');
	queryData = queryData.slice(1,-1);
	queryData = queryData.split(',');
	
	var metric = queryData[3];
	var keyLvl = queryData[4];
	var spec = queryData[2];
	

	function updateQueriedOption(optionQueried) {
		var currentOption = document.getElementById(optionQueried);
		currentOption.style.setProperty('background-color', 'var(--borderColor)');
		currentOption.style.setProperty('border-color', 'var(--textColor)');
		currentOption.style.setProperty('color', 'var(--backgroundColorMain)');
		currentOption.style.setProperty('pointer-events', 'none');
		return 0
	}
	function updateSpecQueried(specQueried) {
		var specOption0 = document.getElementById('specBtn0');
		var specOption1 = document.getElementById('specBtn1');
		var specOption2 = document.getElementById('specBtn2');
		var specOption3 = document.getElementById('specBtn3');
		
		if (specQueried == specOption0.value) { updateQueriedOption('specBtn0'); }
		else if (specQueried == specOption1.value) { updateQueriedOption('specBtn1'); }
		else if (specQueried == specOption2.value) { updateQueriedOption('specBtn2'); }
		else { updateQueriedOption('specBtn3'); }
		
		return 0
	}
	
	updateSpecQueried(spec);
	
	updateQueriedOption(metric);
	updateQueriedOption(keyLvl);
	
	
	
	
	return 0
}




// sleep function that resolves if the animation class is removed from the object
function animationSleep(ms, obj, fadeClass) {
	return new Promise(resolve => {
		setTimeout(resolve, ms);
		checkOnAnimationStatus => {
			if (obj.classList.contains(fadeClass)) { setTimeout(checkOnAnimationStatusStatus, 30); }
			else { return resolve(); }
		};
	})
}

// causes object to fade in on click
async function fade(target, whichFadeClass) {
	
	var target = document.getElementById(target);
	
	var fadeClass = '';
	switch(whichFadeClass) {
		
		case '0':
			fadeClass = 'fade0';
			break;
		
		default:
			fadeClass = 'fade';
			break;
		
	}
	
	/*
	if (target.classList.contains(fadeClass)) {
		target.classList.remove(fadeClass);
		if (target.style.opacity == '1') { target.style.opacity = '0' }
		await sleep(50);
	}
	*/
	
	target.classList.add(fadeClass);
	
	var targetDuration = window.getComputedStyle(target).getPropertyValue('animation-duration'),
		targetDuration = targetDuration.replace('s', ''),
		targetDuration = Number(targetDuration) * 1000;
	
	await animationSleep(targetDuration, target, fadeClass);
	
	if (target.classList.contains(fadeClass)) { target.classList.remove(fadeClass); }
	target.style.opacity = '1';
	
}

// causes objects of a certain class to fade in on click
async function fadeClass(target, whichFadeClass) {
	
	var target = document.getElementsByClassName(target);
	var btn = document.getElementById('runBtn');
	
	var fadeClass = '';
	switch(whichFadeClass) {
		case '0':
			fadeClass = 'fade0';
			break;
		default:
			fadeClass = 'fade';
			break;
	}
	
	if ( target[0].classList.contains(fadeClass) ) { 
		for (var i = 0; i < target.length; i++) {
			if (target[i].classList.contains(fadeClass)) {
				target[i].classList.remove(fadeClass);
				if (target[i].style.opacity == '1') { target[i].style.opacity = '0'; }
			}
		}
		if (btn.classList.contains(fadeClass)) { btn.classList.remove(fadeClass); } 
		if (btn.style.opacity == '1') { btn.style.opacity = '0'; }
		await sleep(1);
	}

	for (var i = 0; i < target.length; i++) { target[i].classList.add(fadeClass); }
	btn.classList.add(fadeClass);
	
	var targetDuration = window.getComputedStyle(target[0]).getPropertyValue('animation-duration'),
		targetDuration = targetDuration.replace('s', ''),
		targetDuration = Number(targetDuration) * 1000;
	
	await animationSleep(targetDuration, target[target.length - 1], fadeClass);
	
	if (target[target.length - 1].classList.contains(fadeClass)) {
	
		for (var i = 0; i < target.length; i++) {
			if (target[i].classList.contains(fadeClass)) {
				target[i].classList.remove(fadeClass);
				if (target[i].style.opacity == '0') { target[i].style.opacity = '1'; }
			}
		}
		
		if (btn.classList.contains(fadeClass)) { btn.classList.remove(fadeClass); } 
		if (btn.style.opacity == '0') { btn.style.opacity = '1'; }
		
	}
	

	
}


// sleep/wait
function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

