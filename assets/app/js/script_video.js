class Vote {
    constructor() {
        this.videoUid = document.getElementsByClassName('video__voting')[0].getAttribute('data-uid');
        this.data = []
    }

    get_video_uid() {
        return this.videoUid;
    }

    get_votes() {
        let data = 'None';
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/videos/' + this.get_video_uid() + '/votes', false);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    data = JSON.parse(xhr.responseText);
                }
            }
        };
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send();
        this.data = data;
    }

    set_data() {
        if (this.data) {
            let up_element = document.getElementById('up');
            let down_element = document.getElementById('down');
            up_element.textContent = this.data.data.up;
            down_element.textContent = this.data.data.down;
            let elements = document.getElementsByClassName('video__voting-button');
            for (let i = 0; i < elements.length; i++) {
                if (elements[i].getAttribute('data-up') === this.data.data.user_vote) {
                    elements[i].classList.add('video__voting-button--voted');
                } else {
                    elements[i].classList.remove('video__voting-button--voted');
                }
            }
            return true;
        }
        return false;
    }

    vote(type) {
        if (this.data.data.user_vote === type) {
            this.deleleVote();
        } else {
            this.createVote(type);
        }
    }

    deleleVote() {
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/videos/' + this.get_video_uid() + '/votes/remove', false);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send();
        this.get_votes();
        this.set_data();
    }

    createVote(type) {
        let form = new FormData();
        form.append('type', type);
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/videos/' + this.get_video_uid() + '/votes/create', false);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send(form);
        this.get_votes();
        this.set_data();
    }

}


function createView() {
    let xhr = new XMLHttpRequest();
    let data = '';
    let form = new FormData();
    xhr.open('POST', '/videos/' + uid + '/views', false);
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

let vote = new Vote();
vote.get_votes();
vote.set_data();