Vue.component('video-container', {
    template: "" +
    "<div>" +
    "<input v-if='!uploading' v-on:change='fileInputChange' type='file' name='video' id='video'/>" +
    "<div v-if='uploading && !failed' id='form-video'><div class='form-group'><label for='title'>Title</label><input class='form-control' type='text' v-model='title'></div><div class='form-group'><label for='description'>Description</label><textarea class='form-control' v-model='description' id='description'></textarea></div><div class='form-group'><label for='visibility'>Visibility</label><select class='form-control' v-model='visibility'><option value='1'>Public</option><option value='2'>Unlisted</option><option value='3'>Private</option></select></div><span class='help-block pull-right'>{{ saveStatus }}</span><button @click.prevent='update' class='btn btn-default'>Save update</button></div>" +
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
            saveStatus: null
        };
    },
    methods: {
        fileInputChange: function () {
            this.uploading = true;
            this.failed = false;
            this.file = document.getElementById('video').files[0];
            this.store();
            this.upload_video();
        },
        store: function () {
            var params = new FormData();
            params.append('title', this.title);
            params.append('description', this.description);
            params.append('visibility', this.visibility);
            params.append('extension', this.file.name.split('.').pop());
            return axios.post('/video', params).then(response => {
                this.uid = response.data.uid
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
                setTimeout(() => {
                    this.saveStatus = null;
                }, 3000);
            });
        },
         upload_video: function () {
            var formData = new FormData();
            formData.append("video", this.file);
            return axios.post('/video/store/upload',
                formData,
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    timeout: 10000,
                    onUploadProgress: function (progressEvent) {
                        var upload_process = Math.round((progressEvent.loaded / progressEvent.total) * 100);
                        console.log(upload_process)
                    }.bind(this)
                }
            ).then((response) => {
                console.log(response);
            }).catch((error) => {
                console.log(error);
            });
         }
    }

});

const app = new Vue({
    el: '#app'
});
