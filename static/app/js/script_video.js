function createView() {
    let xhr = new XMLHttpRequest();
    let data = '';
    let form = new FormData();
    xhr.open('POST', 'videos/' + this.uid + '/views', false);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                data = JSON.parse(xhr.responseText);
            }
        }
    };
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.send(form);
    return data;
}

let player = videojs('codetube-video');

player.on('loadedmetadata', function () {
    let duration = Math.round(player.duration());
    if (!duration) {
        return false;
    }
    setInterval(function () {
        let currentTime = Math.round(player.currentTime()) === Math.round((10 * duration) / 100);
        if (currentTime) {
            createView()
        }
    }, 1000);

});