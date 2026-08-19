document.addEventListener('DOMContentLoaded', function() {
    const audio = document.getElementById('podcast-audio');
    const playPauseBtn = document.getElementById('podcast-play-pause');
    const progressContainer = document.querySelector('.podcast-progress-container');
    const progress = document.getElementById('podcast-progress');
    const currentTimeEl = document.getElementById('podcast-current-time');
    const durationEl = document.getElementById('podcast-duration');
    const speedSelect = document.getElementById('podcast-speed');
    const rewindBtn = document.getElementById('podcast-rewind');
    const forwardBtn = document.getElementById('podcast-forward');

    playPauseBtn.addEventListener('click', function() {
        if (audio.paused) {
            audio.play();
            playPauseBtn.classList.remove('play');
            playPauseBtn.classList.add('pause');
            playPauseBtn.innerHTML = `<i class="fa-solid fa-pause"></i>`
        } else {
            audio.pause();
            playPauseBtn.classList.remove('pause');
            playPauseBtn.classList.add('play');
            playPauseBtn.innerHTML = `<i class="fa-solid fa-play "></i>`
        }
    });

    audio.addEventListener('timeupdate', function() {
        const progressPercent = (audio.currentTime / audio.duration) * 100;
        progress.style.width = `${progressPercent}%`;

        const currentMinutes = Math.floor(audio.currentTime / 60);
        const currentSeconds = Math.floor(audio.currentTime % 60);
        const durationMinutes = Math.floor(audio.duration / 60);
        const durationSeconds = Math.floor(audio.duration % 60);

        currentTimeEl.textContent = `${currentMinutes}:${currentSeconds < 10 ? '0' + currentSeconds : currentSeconds}`;
        durationEl.textContent = `${durationMinutes}:${durationSeconds < 10 ? '0' + durationSeconds : durationSeconds}`;
    });

    progressContainer.addEventListener('click', function(e) {
        const width = this.clientWidth;
        const clickX = e.offsetX;
        const duration = audio.duration;

        audio.currentTime = (clickX / width) * duration;
    });

    audio.addEventListener('loadedmetadata', function() {
        const durationMinutes = Math.floor(audio.duration / 60);
        const durationSeconds = Math.floor(audio.duration % 60);

        durationEl.textContent = `${durationMinutes}:${durationSeconds < 10 ? '0' + durationSeconds : durationSeconds}`;
    });

    speedSelect.addEventListener('change', function() {
        audio.playbackRate = this.value;
    });

    rewindBtn.addEventListener('click', function() {
        audio.currentTime = Math.max(0, audio.currentTime - 5);
    });

    forwardBtn.addEventListener('click', function() {
        audio.currentTime = Math.min(audio.duration, audio.currentTime + 5);
    });
});
