class AjaxRequest {

    constructor(params, url, method) {
        this.params = params;
        this.url = url;
        this.method = method;
    }

    sendData(update = false) {
        let xhr = new XMLHttpRequest();
        xhr.open(this.method, this.url, false);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    if (update === false) {
                        let response = JSON.parse(xhr.responseText);
                        localStorage.setItem('uid', response.uid);
                        localStorage.setItem('file_name', response.file_name);
                    } else {
                        let element_help_block = document.getElementById('help-block');
                        element_help_block.textContent = 'Changed save';
                        setTimeout(function () {
                            element_help_block.textContent = '';
                        }, 3000)
                    }

                }
            }
        };
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send(this.params);
    }

    upload_video(progressbar, progress_block, element) {
        let ajax = new XMLHttpRequest();
        ajax.upload.addEventListener('progress', function (event) {
            let percent = Math.round((event.loaded / event.total) * 100);
            progressbar.style.width = percent + '%';
        });
        ajax.onreadystatechange = function () {
            if (ajax.readyState === 4) {
                if (ajax.status === 200) {
                    progress_block.style.display = 'none';
                    progressbar.style.width = 0 + '%';
                    element.style.display = 'block';
                    setTimeout(function () {
                        element.style.display = 'none';
                    }, 4000)
                }
            }
        };
        ajax.open(this.method, this.url);
        ajax.send(this.params);
    }
}

class UploadListener {
    constructor() {
        this.title = 'Untitled';
        this.description = 'null';
        this.visibility = '1';
        this.form = new FormData();
    }

    fileUpload(element) {
        this.file = element.files[0];
        let form = this.form;
        element.style.display = 'none';
        let form_video = document.getElementById('form-video');
        let progressBar = document.getElementsByClassName('progress')[0];
        form_video.style.display = 'block';
        document.getElementById('title').value = this.title;
        document.getElementById('description').value = this.description;
        progressBar.style.display = 'block';
        form.append('title', this.title);
        form.append('description', this.description);
        form.append('visibility', this.visibility);
        form.append('extension', this.file.name.split('.').pop());
        let request = new AjaxRequest(form, '/video', 'POST');
        request.sendData();
        this.upload_video();
    }

    upload_video() {
        let progressbar = document.getElementsByClassName('progress-bar')[0];
        let progress_block = document.getElementsByClassName('progress')[0];
        let element = document.getElementById('alert-show');
        let form = this.form;
        form.append("video", this.file);
        form.append("file_uid", localStorage.getItem('file_name'));
        let ajaxRequest = new AjaxRequest(form, '/video/store/upload', 'POST');
        ajaxRequest.upload_video(progressbar, progress_block, element);
    }

    saveDataUpload() {
        let form = this.form;
        document.getElementById('help-block').textContent = 'Saving changes';
        this.title = document.getElementById('title').value;
        this.description = document.getElementById('description').value;
        this.visibility = document.getElementById('visibility').value;
        form.append('title', this.title);
        form.append('description', this.description);
        form.append('visibility', this.visibility);
        let request = new AjaxRequest(form, '/video/' + localStorage.getItem('uid'), 'POST');
        request.sendData(true);
    }

}

let app = new UploadListener();
