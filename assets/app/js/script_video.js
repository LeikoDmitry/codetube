
class Vote {
    constructor() {
        if (document.getElementsByClassName('video__voting').length > 0) {
             this.videoUid = document.getElementsByClassName('video__voting')[0].getAttribute('data-uid');
        }
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
            if (up_element) {
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

class Comments {

    constructor() {
        this.comment_block_count = document.getElementsByClassName('count-comment')[0];
        this.content_comment = document.getElementById('content_comment');
        this.comment_video = document.getElementById('video-comment');
        this.xhr = new XMLHttpRequest();
    }

    get_comments() {
        let comments = '';
        let xhr = new XMLHttpRequest();
        if (uid) {
            xhr.open('GET', '/videos/' + uid + '/comments', false);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        comments = JSON.parse(xhr.responseText);
                    }
                }
            };
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.send();
            this.set_data_comments(comments);
        }

    }

    set_data_comments(array) {
        if (array !== undefined) {
            if (this.comment_block_count !== undefined) {
                this.comment_block_count.textContent = array.length + ' comments';
                this.content_comment.innerHTML = this.tree_comments(array, null);
                return this;
            }
        }
        return false;
    }

    createVideoComment() {
        let xhr = this.xhr;
        let form = new FormData();

        form.append('body', this.comment_video.value);
        form.append('reply_id', null);
        xhr.open('POST', '/videos/' + uid + '/comments/create', false);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 201) {
                    let comments_from_backend = JSON.parse(xhr.responseText);
                    let cls = new Comments();
                    cls.comment_block_count.textContent = comments_from_backend.length + ' comments';
                    cls.set_data_comments(comments_from_backend);
                }
            }
        };
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.setRequestHeader('X-CSRFToken', window.codetube.CSRF_TOKEN);
        xhr.send(form);
        this.comment_video.value = '';
        return this;
    }

    tree_comments(array, parent) {
        let html = '';
        for (let i = 0; i < array.length; i++) {
            if (parent === null) {
                html += '<li class="media">';
            } else {
                html += '<div class="media">';
            }
            if (array[i].reply_id === parent) {
                let comment_id = array[i].id;
                html += '<div class="media-left">';
                html += '<a href="#">' + '<img class="media-object" src="' + array[i].image_channel + '" >' + '</a>';
                html += '</div>';
                html += '<div class="media-body">';
                html += '<a href="#">' + array[i].name_channel + '</a> ' + array[i].create_at;
                html += '<p>' + array[i].body + '</p>';
                html += '<div class="video-comment clear">' +
                    '<textarea id="replay_body_' + comment_id + '" class="form-control"></textarea>' +
                    '<div class="pull-right">' +
                    '<button onclick="comments.createReply(' + comment_id + ');" class="btn btn-default video-comment__input">Reply</button>' +
                    '</div>' +
                    '</div>';
                html += this.tree_comments(array, array[i].id);
                html += '</div>';
            }
            if (parent === null) {
                html += '</li>';
            } else {
                html += '</div>';
            }
        }
        return html;
    }

    createReply(comment_id) {
        let xhr = this.xhr;
        let form = new FormData();
        let bodyReply = document.getElementById('replay_body_' + comment_id);
        form.append('body', bodyReply.value);
        form.append('reply_id', comment_id);
        xhr.open('POST', '/videos/' + uid + '/comments/create', false);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 201) {
                    let comments_from_backend = JSON.parse(xhr.responseText);
                    let cls = new Comments();
                    cls.comment_block_count.textContent = comments_from_backend.length + ' comments';
                    cls.set_data_comments(comments_from_backend);
                }
            }
        };
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.setRequestHeader('X-CSRFToken', window.codetube.CSRF_TOKEN);
        xhr.send(form);
        bodyReply.value = '';
        return this;
    }

}

class Subscibed {
    constructor() {
        this.block_subsribed = document.getElementById('block__subscribe');
    }

    subscribe_user() {
        let xhr = new XMLHttpRequest();
        let data = '';
        let name_channel = this.block_subsribed.getAttribute('data-slug-channel');
        xhr.open('GET', '/subscription/' + name_channel, false);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    data = JSON.parse(xhr.responseText);
                    if (data !== undefined) {
                        let button = document.querySelector('#block__subscribe button');
                        let span = document.querySelector('#block__subscribe span');
                        if (data.user_subscribed === false && data.can_subscribe === true) {
                            button.textContent = 'Unsubscribe';
                            let ajax = new XMLHttpRequest();
                            ajax.open('PUT', '/subscription/' + name_channel, false);
                            ajax.onreadystatechange = function () {
                                data = JSON.parse(ajax.responseText);
                                if (data.response === true) {
                                     span.textContent = data.count + ' ' + 'subscribers';
                                }
                            };
                            ajax.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                            ajax.send();
                        } else {
                            button.textContent = 'Subscribe';
                            let ajax = new XMLHttpRequest();
                            ajax.open('DELETE', '/subscription/' + name_channel, false);
                             ajax.onreadystatechange = function () {
                                data = JSON.parse(ajax.responseText);
                                 if (data.response === true) {
                                     span.textContent = data.count + ' ' + 'subscribers';
                                 }
                            };
                            ajax.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                            ajax.send();
                        }
                    }
                }
            }
        };
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send();
    }

    set_subscibed_user_information() {
        let xhr = new XMLHttpRequest();
        let data = '';
        let form = new FormData();
        let name_channel = this.block_subsribed.getAttribute('data-slug-channel');
        xhr.open('GET', '/subscription/' + name_channel, false);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    data = JSON.parse(xhr.responseText);
                    if (data !== undefined) {
                        console.log(data);
                        let span = document.querySelector('#block__subscribe span');
                        span.textContent = data.count + ' ' + 'subscribers';
                        if (data.user_subscribed === true && data.can_subscribe === false) {
                            let button = document.querySelector('#block__subscribe button');
                            button.textContent = 'Unsubscribe';
                        }
                    }
                }
            }
        };
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send(form);
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

video_block = document.getElementById('codetube-video');

if (video_block) {
    let player = videojs('codetube-video');
    player.on('loadedmetadata', function () {
        let duration = Math.round(player.duration());
        if (! duration) {
            return false;
        }
        setInterval(function () {
            let currentTime = Math.round(player.currentTime()) === Math.round((10 * duration) / 100);
            if (currentTime) {
                createView()
            }
        }, 1000);
    });
}

let vote = new Vote();
vote.get_votes();
vote.set_data();

let comments = new Comments();
comments.get_comments();

let sub = new Subscibed();
sub.set_subscibed_user_information();

let collection = document.getElementsByClassName('subscribe');
console.log(collection);
if (collection) {
    collection[0].addEventListener('click', function () {
        sub.subscribe_user()
    });
}
