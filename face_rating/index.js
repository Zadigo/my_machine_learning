var submitinformation = {
    props: ["userinformation"],
    template: "\
    <div class='modal-footer'>\
        <a @click='processinformation' class='btn-flat waves-effect waves-red'>Submit and continue</a>\
    </div>\
    ",
    methods: {
        processinformation: function() {
            var self = this
            $.ajax({
                type: "GET",
                url: "/",
                data: self.$props.userinformation,
                dataType: "json",
                success: function (response) {
                    window.location.pathname = "/my_machine_learning/face_rating/scoring.html"
                }
            });
        }
    }
}

var modalcontent = {
    template: "\
    <div id='modal1' class='modal'>\
        <div class='modal-content'>\
            <h4>User information</h4>\
            <div class='row'>\
                <div class='input-field col s12 m4 l4'>\
                    <select v-model='userinformation.gender' name='gender' id='gender'>\
                        <option v-for='gender in genders' \
                            :key='gender' :value='gender'>{{ gender }}</option>\
                    </select>\
                </div>\
                <div class='input-field col s12 m6 l6'>\
                    <select v-model='userinformation.orientation' name='sexual_orientation' id='sexual_orientation'>\
                        <option v-for='sexualorientation in sexualorientations' \
                            :key='sexualorientation' :value='sexualorientation'>{{ sexualorientation }}</option>\
                    </select>\
                </div>\
                <div class='col s12 m12 l12'>\
                    <p>How did you know about this website?</p>\
                </div>\
                <div class='input-field col s12 m4 l4'>\
                    <select v-model='userinformation.referrer' name='medium' id='medium'>\
                        <option v-for='referrer in referrers' \
                            :key='referrer' :value='referrer'>{{ referrer }}</option>\
                    </select>\
                </div>\
                <div class='input-field col s12 m12 l12'>\
                    <p>\
                        <label>\
                            <input @click='futureresearches=!futureresearches' type='checkbox' name='email' id='email'>\
                            <span>I would like to take part in future experiences of this kind</span>\
                        </label>\
                    </p>\
                </div>\
                <div v-if='futureresearches' class='input-field col s12 m6 l6'>\
                    <input v-model='userinformation.email' type='email' name='email' id='email' placeholder='Email'>\
                </div>\
            </div>\
        </div>\
        <submitinformation v-bind:userinformation='userinformation' />\
    </div>\
    ",
    components: {submitinformation},
    data() {
        return {
            showemail: false,
            genders: ["male", "female"],
            sexualorientations: ["heterosexual", "homosexual", "not precised"],
            referrers: ["reddit", "facebook", "twitter", "email"],
            futureresearches: false,
            email: "",
            userinformation: {gender: "male", orientation: "heterosexual", referrer: "reddit", email: ""}
        }
    }
}

var userinformation = new Vue({
    el: "#user_information",
    components: {modalcontent},
    data() {
        return {
        }
    }
})