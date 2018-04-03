Vue.component('video-container', {
    template: "" +
    "<div>" +
    "<div class='alert alert-success' v-if='showAlert'>Your video will be availible. <a href='/videos'>Go to your videos</a></div>" +
    "<input v-if='!uploading' v-on:change='fileInputChange' type='file' name='video' id='video'/>" +
    "<div v-if='uploading && !failed' id='form-video'><div class='form-group'><label for='title'>Title</label><input class='form-control' type='text' v-model='title'></div><div class='form-group'><label for='description'>Description</label><textarea class='form-control' v-model='description' id='description'></textarea></div><div class='form-group'><label for='visibility'>Visibility</label><select class='form-control' v-model='visibility'><option value='1'>Public</option><option value='2'>Unlisted</option><option value='3'>Private</option></select></div><span class='help-block pull-right'>{{ saveStatus }}</span><button @click.prevent='update' class='btn btn-default'>Save update</button></div>" +
    "<div style='margin-top: 20px;' v-if='UploadingComplete' class='progress'><div id='progress-bar' class='progress-bar'></div></div>" +
    "</div>",
    data: function () {
        return {
            process: null,
            uid: null,
            uploading: false,
            UploadingComplete: false,
            failed: false,
            title: 'Untitled',
            description: null,
            visibility: '1',
            saveStatus: null,
            showAlert: false,
            file_name: null
        };
    },
    methods: {
        fileInputChange: function () {
            this.uploading = true;
            this.failed = false;
            this.file = document.getElementById('video').files[0];
            this.store();

        },
        store: function () {
            var params = new FormData();
            params.append('title', this.title);
            params.append('description', this.description);
            params.append('visibility', this.visibility);
            params.append('extension', this.file.name.split('.').pop());
            return axios.post('/video', params).then(response => {
                this.uid = response.data.uid;
                this.file_name = response.data.file_name;
                this.upload_video();
            });
        },
        update: function () {
            this.saveStatus = 'Saving changes';
            var params = new FormData();
            params.append('title', this.title);
            params.append('description', this.description);
            params.append('visibility', this.visibility);
            return axios.post('/video/' + this.uid, params).then(response => {
                this.saveStatus = 'Changed save';
                this.uid = response.data.uid;
                setTimeout(() => {
                    this.saveStatus = null;

                }, 1000);
            });
        },
         upload_video: function () {
            console.log(this.uid);
            var formData = new FormData();
            formData.append("video", this.file);
            formData.append("file_uid", this.file_name);
            return axios.post('/video/store/upload',
                formData,
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    timeout: 10000000,
                    onUploadProgress: function (progressEvent) {
                        var upload_process = Math.round((progressEvent.loaded / progressEvent.total) * 100);
                        var progressbar = document.getElementById('progress-bar') || "";
                        if (progressbar !== "") {
                             progressbar.style.width = upload_process + "%";
                        }
                        this.UploadingComplete = true;
                    }.bind(this)
                }
            ).then((response) => {
                this.UploadingComplete = false;
                this.showAlert = true;
                 setTimeout(() => {
                     this.showAlert = false;
                }, 3000);
                console.log(response);

            }).catch((error) => {
                console.log(error);
            });
         }
    }

});

var app = new Vue({
    el: '#app',
    data: window.codetube
});
