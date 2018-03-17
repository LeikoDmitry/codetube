
var data = {uploading: true,  UploadingComplete: false,  failed: false};
Vue.component('video-container', {
    template: "<input v-if='uploading' v-on:change='fileInputChange' type='file' name='video' id='video'><div>Form</div>",
    data: function () {
      return data;
    },
    methods: {
        fileInputChange: function () {
            this.uploading = false;
            this.failed = false;
        }
    }
});

const app = new Vue({
    el: '#app'
});
