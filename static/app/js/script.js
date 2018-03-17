
Vue.component('video-container', {
    template: "" +
    "<div>" +
        "<input v-if='!uploading' v-on:change='fileInputChange' type='file' name='video' id='video'/>" +
        "<div v-if='uploading && !failed' id='form-video'>Form</div>" +
    "</div>",
    data: function () {
      return {uploading: false,  UploadingComplete: false,  failed: false};
    },
    methods: {
        fileInputChange: function () {
            this.uploading = true;
            this.failed = false;
        }
    }
});

const app = new Vue({
    el: '#app'
});
