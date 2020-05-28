var imagecomponent = {
    props: ["imageorder", "images"],
    template: "\
    <div class='responsive-img'>\
        <img :src='currentimage' alt='face'>\
    </div>\
    ",
    computed: {
        currentimage() {
            return "./images/" + this.$props.images[this.$props.imageorder] + ".jpg"
        }
    }
}

var ratingcomponent = {
    props: ["isfinalimage"],
    template: "\
    <div class='row' id='stars'>\
        <div class='col s12 m12 l12'>\
            <p>How would you rate her level of attractiveness?</p>\
            <i @click='selectstar(star)' v-for='star in stars' \
                v-if='star.selected' :key='star.value' class='material-icons' id='star'>star</i>\
            <i @click='selectstar(star)' v-else class='material-icons' id='star'>star_outline</i>\
        </div>\
        <div class='col s12 m12 l12'>\
            <a href='./index.html' class='btn-large grey lighten-1 waves-effect waves-light'>\
                <i class='material-icons left'>stop</i>Cancel\
            </a>\
            <button @click='nextface' v-if='!isfinalimage' \
                        class='btn-large green darken-1 waves-effect waves-light'>\
                <i class='material-icons left'>navigate_next</i>Next\
            </button>\
            <a @click='finalizerating' v-else href='#!' \
                class='btn-large red darken-1 waves-effect waves-light'>\
                    <i class='material-icons left'>done_all</i>Final rating\
            </a>\
        </div>\
    </div>\
    ",
    data() {
        return {
            stars: [
                {value: 1, selected: true},
                {value: 2, selected: false},
                {value: 3, selected: false},
                {value: 4, selected: false}
            ],
            selectedstar: 1
        }
    },
    methods: {
        selectstar: function(selectedstar) {
            this.$data.selectedstar = selectedstar.value
            this.$data.hasrated = true
            this.$data.stars.forEach(star => {
                star.selected = false
                if (star.value <= selectedstar.value) {
                    star.selected = true
                }
            })
        },
        resetstars: function() {
            this.$data.stars.forEach(star => {
                star.selected = false
                if (star.value === 1) {
                    star.selected = true
                }
            })
        },
        nextface: function() {
            this.resetstars()
            this.$emit("nextface", this.$data.selectedstar)
        },
        finalizerating: function() {
            this.$emit("finalizerating", this.$data.selectedstar)
        }
    }
}

var scoringfaces = new Vue({
    el: "#app",
    components: {imagecomponent, ratingcomponent},
    data() {
        return {
            finalrating: [],
            images: [],
            numberofimages: 1,
            imageorder: 0,
            isfinalimage: false
        }
    },
    mounted() {
        var images = ["fw1", "fw2", "fw3", "fw4", "fw5", "fw6", "fw7", "fw8", 
            "fw9", "fw10", "fw11", "fw12", "fw13", "fw14"]
        var shuffledimages = _.shuffle(images)
        this.$data.images = shuffledimages
        this.$data.numberofimages = this.$data.images.length
    },
    methods: {
        shownextface: function(imagerating) {
            if (this.$data.imageorder + 1 === this.$data.numberofimages - 1) {
                this.$data.isfinalimage = true
            }
            this.$data.imageorder = this.$data.imageorder + 1
            this.$data.finalrating.push([this.$data.images[this.$data.imageorder], imagerating])
        },
        doratings: function(imagerating) {
            this.$data.finalrating.push([this.$data.images[this.$data.imageorder], imagerating])
            $.ajax({
                type: "GET",
                url: "/",
                // data: this.$data.finalrating,
                dataType: "json",
                success: function (response) {
                    window.location.href = "/my_machine_learning/face_rating/index.html"
                },
                error: function() {}
            });
        }
    }
})