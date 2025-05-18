// Check for previously saved content
window.onload = function() {
	const savedHTML = localStorage.getItem('journalEntryHTML');
	
	if (savedHTML) {
		document.getElementById('journal-text').innerHTML = savedHTML;
	}
	
	// Add format toolbar
	updateFormatControls();
	
	// Setup auto-save
	setupAutoSave();
};

function updateFormatControls() {
	const formatControlsDiv = document.querySelector('.format-controls');
	
	if (formatControlsDiv) {
		formatControlsDiv.innerHTML = `
			<div class="format-toolbar">
				<select class="font-selector" onchange="applyFontFamily(this.value)">
					<option value="'Roboto Mono', monospace">Roboto Mono</option>
					<option value="'Lora', serif">Lora</option>
					<option value="'Playfair Display', serif">Playfair</option>
					<option value="Arial, sans-serif">Arial</option>
					<option value="'Times New Roman', serif">Times New Roman</option>
				</select>
				<select class="font-size-selector" onchange="applyFontSize(this.value)">
					<option value="1">Small</option>
					<option value="2">Medium</option>
					<option value="3" selected>Normal</option>
					<option value="4">Large</option>
					<option value="5">X-Large</option>
					<option value="6">XX-Large</option>
					<option value="7">XXX-Large</option>
				</select>
				<button onclick="applyFormat('bold')" title="Bold"><i class="fas fa-bold"></i></button>
				<button onclick="applyFormat('italic')" title="Italic"><i class="fas fa-italic"></i></button>
				<button onclick="applyFormat('underline')" title="Underline"><i class="fas fa-underline"></i></button>
				<button onclick="applyFormat('strikeThrough')" title="Strike-through"><i class="fas fa-strikethrough"></i></button>
				<button onclick="applyList('unordered')" title="Bullet List"><i class="fas fa-list-ul"></i></button>
				<button onclick="applyList('ordered')" title="Numbered List"><i class="fas fa-list-ol"></i></button>
				<button onclick="applyFormat('justifyLeft')" title="Align Left"><i class="fas fa-align-left"></i></button>
				<button onclick="applyFormat('justifyCenter')" title="Center"><i class="fas fa-align-center"></i></button>
				<button onclick="applyFormat('justifyRight')" title="Align Right"><i class="fas fa-align-right"></i></button>
			</div>
		`;
	}
}

function applyFormat(command) {
	document.execCommand(command, false, null);
	document.getElementById('journal-text').focus();
}

function applyFontFamily(fontFamily) {
	document.execCommand('fontName', false, fontFamily);
	document.getElementById('journal-text').focus();
}

function applyFontSize(size) {
	document.execCommand('fontSize', false, size);
	document.getElementById('journal-text').focus();
}

function applyList(type) {
	if (type === 'unordered') {
		document.execCommand('insertUnorderedList', false, null);
	} else if (type === 'ordered') {
		document.execCommand('insertOrderedList', false, null);
	}
	
	// Focus back on the text area
	document.getElementById('journal-text').focus();
	
	// Fix for list styling
	const listElements = document.querySelectorAll('#journal-text ul, #journal-text ol');
	listElements.forEach(list => {
		if (type === 'unordered') {
			list.style.listStyleType = 'disc';
		} else {
			list.style.listStyleType = 'decimal';
		}
		list.style.paddingLeft = '40px';
	});
}

/* Finish button */
document.getElementById("finish").onclick = function() {
	// Show separator and analysis container
	document.querySelector('.separator').style.display = 'block';
	document.getElementById('analysis-container').style.display = 'block';
	
	// Scroll to the analysis section
	setTimeout(() => {
		document.getElementById('analysis-container').scrollIntoView({ behavior: 'smooth' });
	}, 100);
	
	document.getElementById('analysis-text').textContent = "[insert AI analysis]";
}
