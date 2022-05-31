const container = document.querySelector(".container"),
audio = container.querySelector(".audio")
phone = container.querySelector("#phone")
playPauseBtn= container.querySelector("#play_pause")
mainAudio = container.querySelector("#main-audio")
volumeUpBtn=container.querySelector("#volume-up")
volumeDownBtn=container.querySelector("#volume-down")
volumeMuteBtn=container.querySelector("#volume-mute")
timeRange=document.querySelector("#timeRange")
const progres = phone.querySelector(".progres");
const progresFilled = phone.querySelector(".progres__filled");
let isMove = false;

//play music function
function playMusic(){
  container.classList.remove("paused");
	playPauseBtn.querySelector("i").classList.remove("fa-play");
	playPauseBtn.querySelector("i").classList.add("fa-pause");
  mainAudio.play();
}

//pause music function
function pauseMusic(){
  container.classList.add("paused");
	playPauseBtn.querySelector("i").classList.remove("fa-pause");
  playPauseBtn.querySelector("i").classList.add("fa-play");
  mainAudio.pause();
}
//play music function
function unmuteMusic(){
  container.classList.remove("muted");
	volumeMuteBtn.querySelector("i").classList.remove("fa-bell-slash");
	volumeMuteBtn.querySelector("i").classList.add("fa-bell");
  mainAudio.muted=false;
	console.log("mute")
}

//pause music function
function muteMusic(){
  container.classList.add("muted");
	volumeMuteBtn.querySelector("i").classList.remove("fa-bell");
  volumeMuteBtn.querySelector("i").classList.add("fa-bell-slash");
  mainAudio.muted=true;
	console.log("unmute")
}

// play or pause button event
playPauseBtn.addEventListener("click", ()=>{
  const isMusicPlay = container.classList.contains("paused");
  //if isPlayMusic is true then call pauseMusic else call playMusic
  isMusicPlay ? playMusic() : pauseMusic(); 
  // playingSong();
});

// play or pause button event
volumeMuteBtn.addEventListener("click", ()=>{
  const isMusicMute = container.classList.contains("muted");
  //if isPlayMusic is true then call muteMusic else call unmuteMusic
  isMusicMute ? unmuteMusic() : muteMusic(); 
  // playingSong();
});

//volume up button event
volumeUpBtn.addEventListener("click", ()=>{
  // volump up
	if ((mainAudio.volume >=0) && (mainAudio.volume <0.89) ){
		mainAudio.volume +=0.1
		
	}else if(mainAudio.volume>=0.89){
		mainAudio.volume =1.0
	}
	console.log(mainAudio.volume)
});

//volume down button event
volumeDownBtn.addEventListener("click", ()=>{
  //volume down
	if ((mainAudio.volume > 0.1) && (mainAudio.volume <=1) ){
		mainAudio.volume -=0.1
		
	}else if(mainAudio.volume <=0.1){
		mainAudio.volume = 0
	}
  console.log(mainAudio.volume)
});



mainAudio.addEventListener("timeupdate", (e)=>{
  const currentTime = e.target.currentTime; //getting playing song currentTime
  const duration = e.target.duration; //getting playing song total duration
  let progressWidth = (currentTime / duration) * 100;
  // progressBar.style.width = `${progressWidth}%`;
	// console.log(progressBar.style.width)
	timeRange.value=progressWidth
  let musicCurrentTime = container.querySelector(".current-time"),
  musicDuartion = container.querySelector(".max-duration");

	// 이전 이벤트 는 dataloaded였음 
  mainAudio.addEventListener("timeupdate", ()=>{
    // update song total duration
    let mainAdDuration = mainAudio.duration;
    let totalMin = Math.floor(mainAdDuration / 60);
    let totalSec = Math.floor(mainAdDuration % 60);
    if(totalSec < 10){ //if sec is less than 10 then add 0 before it
      totalSec = `0${totalSec}`;
    }
    musicDuartion.innerText = `${totalMin}:${totalSec}`;
  });
  // update playing song current time
  let currentMin = Math.floor(currentTime / 60);
  let currentSec = Math.floor(currentTime % 60);
  if(currentSec < 10){ //if sec is less than 10 then add 0 before it
    currentSec = `0${currentSec}`;
  }
  musicCurrentTime.innerText = `${currentMin}:${currentSec}`;
});


// update playing song currentTime on according to the progress bar width
timeRange.addEventListener("click", (e)=>{
	pauseMusic()
  let progressWidth = timeRange.clientWidth; //getting width of progress bar
  let clickedOffsetX = e.offsetX; //getting offset x value
  let songDuration = mainAudio.duration; //getting song total duration
  
  mainAudio.currentTime = (clickedOffsetX / progressWidth) * songDuration;
  playMusic(); //calling playMusic function
});


// 슬라이더 말고  프로그레스바
// function scurb(e) {

// 	// If we use e.offsetX, we have trouble setting the song time, when the mousemove is running
// 	// const currentTime = ( (e.clientX - progres.getBoundingClientRect().left) / progres.offsetWidth ) * song.duration;
// 	const currentTime=(e.clientX/100)*mainAudio.duration;
// 	mainAudio.currentTime = currentTime;
// 	console.log(timeRange.value)
// 	console.log(currentTime)
// 	console.log(mainAudio.currentTime)
// }

// timeRange.addEventListener("pointerdown", (e) => {
// 	scurb(e);
// 	isMove = true;
// });

// timeRange.addEventListener("pointermove", (e) => {
// 	if (isMove) {
// 			scurb(e); 
// 			mainAudio.muted=true;
// 	}
// });
// timeRange.addEventListener("pointerup", () => {
// 	isMove = false;
// 	mainAudio.muted=false;
// });

