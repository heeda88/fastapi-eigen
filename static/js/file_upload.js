//selecting all requierd elements
const bodyArea= document.querySelector('body');
const dropArea= document.querySelector('.drag-area');
const button = dropArea.querySelector('button');
const input = dropArea.querySelector('input');
const uploadBtn = document.querySelector('#upload-btn')
const progressArea= document.querySelector(".progress-area")
const uploadedArea= document.querySelector(".uploaded-area")
const fileProgress= progressArea.querySelector('.file-progress')
const filePercent= progressArea.querySelector('.file-percent')


button.addEventListener('click',(e)=>{
	console.log('button click');
	input.click();
});

input.addEventListener('change',(e)=>{
	let file = input.files;
	let fileType=file.type;
	let fileName=file.name;
	var formdata = new FormData();

	// console.log(file);
	// console.log(fileType);
	// console.log(fileName);
	for (var i=0; i<file.length; i++){
		formdata.append('file_list',file[i])
	}
	uploadData(formdata);
})

// dropArea 제외지역에 파일 드롭시 웹 브라우저 자체 리더기 기능 활성 방지 
bodyArea.addEventListener('dragover',(e)=>{
	e.preventDefault();
});

bodyArea.addEventListener('drop',(e)=>{
	e.preventDefault();
});

// If user Drag file over DragArea
dropArea.addEventListener('dragover',(e)=>{
	e.preventDefault();
	dropArea.classList.add('active');
});

dropArea.addEventListener('dragleave',(e)=>{
	e.preventDefault();
	dropArea.classList.remove('active');
});

dropArea.addEventListener('drop',(e)=>{
	e.preventDefault();
	// console.log('drop event');
	dropArea.classList.remove('active');
  // when user drop the file list , we choose first-file in multiple files.
	let file = e.dataTransfer.files;
	let fileType=file.type;
	let fileName=file.name;
	var formdata = new FormData();
	console.log(file);
	// console.log(fileType);
	// console.log(file.name);
	// console.log(fileName);
	for (var i=0; i<file.length; i++){
		formdata.append('file_list',file[i])
	}
	// uploadData(formdata);
	uploadEachData(file);
	// if you want the specific type, then you have to use file.type to limit wanna type.
	// let validExtensions= ['image/jpeg','image/jpg','image/png',]
	// if(validExtensions.includes(fileType))
});

uploadBtn.addEventListener('click',(e)=>{
	console.log('upload')
})

// Sending AJAX request and upload file
function uploadData (formdata) {
  $.ajax({
    url: '/upload/new_list/',
    type: 'post',
    data: formdata,
    contentType: false,
    processData: false,
		xhr: function(){
			var xhr = $.ajaxSettings.xhr();
			xhr.upload.onprogress = function(e){
				var per = Math.floor(e.loaded * 100 / e.total);
				var fileSize= Math.floor(e.total / 1024);
				var fileName=formdata.get('file_list').name;
				console.log(fileName);
				let progressHTML= `<li class="row">
														<div class="file-content">
															<div class="file-detail">
																<i class="fas fa-file-alt"></i>
																<span class="file-name">${fileName} · Uploading </span>
																<span class="file-percent"> ${per}% </span>
															</div>
															<div class="file-progress-bar">
																<div class="file-progress" style="width:${per}%"></div>
															</div>
														</div>
													</li>`;
					progressArea.innerHTML=progressHTML;
					if (e.loaded == e.total){
						let uploadedHTML =`<li class="row">
																<div class="file-content">
																	<div class="file-detail">
																		<i class="fas fa-file-alt"></i>
																		<span class="file-name">${fileName} · Uploaded </span>
																		<span class="file-size"> ${fileSize} [KB] </span>
																		<i class="fas fa-check"> </i>
																	</div>
																</div>
															</li>`
						uploadedArea.insertAdjacentHTML('afterbegin',uploadedHTML);
						progressArea.innerHTML=``;
					}
			};
			return xhr;
		},
    success: function (data) {
      console.log(data);
    }
  });
}

// Sending AJAX request and upload file
function uploadFirstData (formdata) {
  $.ajax({
    url: '/upload/new/',
    type: 'post',
    data: formdata,
    contentType: false,
    processData: false,
		xhr: function(){
			var xhr = $.ajaxSettings.xhr();
			xhr.upload.onprogress = function(e){
				var per = Math.floor(e.loaded * 100 / e.total);
				var fileSize= Math.floor(e.total / 1024);
				var fileName=formdata.get('file').name;
				let progressHTML= `<li class="row">
														<div class="file-content">
															<div class="file-detail">
																<i class="fas fa-file-alt"></i>
																<span class="file-name">${fileName} · Uploading </span>
																<span class="file-percent"> ${per}% </span>
															</div>
															<div class="file-progress-bar">
																<div class="file-progress" style="width:${per}%"></div>
															</div>
														</div>
													</li>`;
					progressArea.innerHTML=progressHTML;
					if (e.loaded == e.total){
						let uploadedHTML =`<li class="row">
																<div class="file-content">
																	<div class="file-detail">
																		<i class="fas fa-file-alt"></i>
																		<span class="file-name">${fileName} · Uploaded </span>
																		<span class="file-size"> ${fileSize} [KB] </span>
																		<i class="fas fa-check"> </i>
																	</div>
																</div>
															</li>`
						uploadedArea.insertAdjacentHTML('afterbegin',uploadedHTML);
						progressArea.innerHTML=``;
					}
					
			};
			return xhr;
		},
    success: function (data) {
      console.log(data);
    }
  });
}


// Sending AJAX request and upload file
async function uploadEachData (file) {

	for (var i=0; i<file.length; i++){
		let formdata = new FormData;
		formdata.append('file',file[i]);
		uploadFirstData(formdata);
	}
}
