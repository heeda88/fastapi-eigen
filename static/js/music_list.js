
const container= document.querySelector('.container');
const playBtn = container.querySelector('.play-btn');
const pauseBtn = container.querySelector('.pause-btn');
const preBtn = container.querySelector('.prev-btn');
const nextBtn = container.querySelector('.next-btn');
const music = document.getElementById('music');
const musicList = container.getElementsByTagName('li');
const progressBar = document.getElementById('progress-bar');
let currentTrack = 0;
let currentList;

let tracks = [
			{
                "track": 1,
                "name": "I Won't Hurt You",
                "artist": "The West Coast Pop Art Experimental Band",
                "duration": "02:23",
                "url": "https://raw.githubusercontent.com/yuyuchi/AudioPlayer/master/music/I%20Won%20t%20Hurt%20You.mp3"
            },
            {
            	"track": 2,
                "name": "Ganesha",
                "artist": "Wah!",
                "duration": "04:26",
                "url": "https://raw.githubusercontent.com/yuyuchi/AudioPlayer/master/music/Ganesha.mp3"
            },
            {
            	"track": 3,
                "name": "Blueless Bird",
                "artist": "Joni",
                "duration": "03:26",
                "url": "https://raw.githubusercontent.com/yuyuchi/AudioPlayer/master/music/Blueless%20Bird.mp3"            	
            }
    			];

function init() {
	if (currentTrack === 0) {
		music.src = tracks[0].url;
		music.load();
	}

	for(let i=0; i<tracks.length; i++){
		$('#music-list').append(`<li id="${i}"><div class="wrapper"><div>${tracks[i].track}</div><div>${tracks[i].name}</div><div>${tracks[i].artist}</div><div>${tracks[i].duration}</div></div></li><hr/>`);
	}

	for(let musicIndex=0; musicIndex<musicList.length; musicIndex++){
		musicList[musicIndex].addEventListener('click', switchMusic, false);
	}
}

function switchMusic(e) {

	if(currentList !== undefined) {
		removePlayedBackground();
		music.pause();
	}	
	currentTrack = this.id;
	music.src = tracks[currentTrack].url;
	music.load();
	play();

}

function addChoosedBackground() {
	currentList = document.getElementById(currentTrack);
	currentList.classList.add("song-play-now");


}

function removePlayedBackground() {
	currentList.classList.remove("song-play-now");

}

function play() {
	playBtn.classList.add("hidden");
	pauseBtn.classList.remove("hidden");
	
	music.play();
	musicIsPlaying = true;
	addChoosedBackground();
	document.getElementById('end-time').innerHTML = tracks[currentTrack].duration;
}

function pause() {
	pauseBtn.classList.add("hidden");
	playBtn.classList.remove("hidden");

	musicIsPlaying = false;
	music.pause();
}


function prePlay() {
	removePlayedBackground();
	music.pause();

	if (currentTrack > 0){
		currentTrack --;

	} else {
		currentTrack = tracks.length-1;
	}
	
	music.src = tracks[currentTrack].url;
	music.load();
	play();

}

function nextPlay() {
	removePlayedBackground();
	music.pause();
	
	if (currentTrack < tracks.length-1){
		currentTrack ++;

	} else {
		currentTrack = 0;
	}

	music.src = tracks[currentTrack].url;
	music.load();
	play();

}

function calculateTotalValue(length) {
  let minutes = Math.floor(length / 60),
    seconds_int = length - minutes * 60,
    seconds_str = seconds_int.toString(),
    seconds = seconds_str.substr(0, 2),
    time = minutes + ':' + seconds

  return time;
}

function formatTime() {
	let timeline = document.getElementById('start-time');
    let s = parseInt(music.currentTime % 60);
    let m = parseInt((music.currentTime / 60) % 60);
    if (s < 10) {
        timeline.innerHTML = m + ':0' + s;
    }
    else {
        timeline.innerHTML = m + ':' + s;
    }
}

function updateProgress() {
	let current = music.currentTime;
	let percent = (current / music.duration) * 100;
	progressBar.setAttribute('value', percent);

}

function scurb(e) {

	// If we use e.offsetX, we have trouble setting the song time, when the mousemove is running
	// const currentTime = ( (e.clientX - progres.getBoundingClientRect().left) / progres.offsetWidth ) * song.duration;
	// song.currentTime = currentTime;
	console.log
	console.log(e.clientX )
	console.log(progressBar.getBoundingClientRect().left)

}





playBtn.addEventListener('click', play, false);
pauseBtn.addEventListener('click', pause, false);
preBtn.addEventListener('click', prePlay, false);
nextBtn.addEventListener('click', nextPlay, false);
music.addEventListener('ended', nextPlay, false);


music.addEventListener("timeupdate", formatTime, false);
music.addEventListener("timeupdate", updateProgress, false);



progressBar.addEventListener("pointerdown", (e) => {
	scurb(e);
	isMove = true;
});

document.addEventListener("pointermove", (e) => {
	if (isMove) {
			scurb(e); 
			song.muted = true;
	}
});

document.addEventListener("pointerup", () => {
	isMove = false;
	song.muted = false;
});






init();