function playSound(soundfile) {
    var audio = new Audio(soundfile || "http://fnaflore.com/wp-content/uploads/2016/04/Rawr_SFX.mp3");
    audio.play();
  }