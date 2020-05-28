var questionslist = [
    {
        id: 1,
        text: "Vous ____ raison",
        answers: [
            {id: 1, text: "avez", correct: true, selected: false},
            {id: 2, text: "avons", correct: false, selected: false},
            {id: 3, text: "aurez", correct: false, selected: false},
            {id: 4, text: "auriez", correct: false, selected: false}
        ]
    },
    {
        id: 2,
        text: "Vous ____ parler avec raison",
        answers: [
            {id: 1, text: "devez", correct: true, selected: false},
            {id: 2, text: "devons", correct: false, selected: false},
            {id: 3, text: "deviez", correct: false, selected: false},
            {id: 4, text: "diriez", correct: false, selected: false}
        ]
    }
]


var answers = {
    props: ["question"],
    template: "\
    <div class='answers'>\
        <button @click='doselection(answer)' v-for='answer in currentanswers' :key='answer.id' \
            class='btn-large z-depth-0 red waves-effect waves-light'>\
                    {{ answer.text }}\
        </button>\
    </div>\
    ",
    data() {
        return {
            answers: []
        }
    },
    computed: {
        currentanswers() {
            return _.shuffle(this.$props.question.answers)
        },
        selectedanswer() {
            return this.$data.answers.filter(answer => {
                return answer.selected === true
            })
        }
    },
    methods: {
        doselection: function(selectedanswer) {
            this.$data.answers.forEach(answer => {
                answer.selected = false
                if (answer.id === selectedanswer.id) {
                    selectedanswer.selected = true
                }
            })
            this.$emit("doselection")
        }
    }
}


var phrase = {
    props: ["question"],
    template: "\
    <div class='phrase'>\
        {{ question.text }}\
    </div>\
    "
}

var languages = new Vue({
    el: "#app",
    components: {phrase, answers},
    data() {
        return {
            cursor: 0,
            numberofquestions: 1,
            isfinalquestion: false,
            questions: []
        }
    },
    beforeMount() {
        this.$data.questions = questionslist
    },
    computed: {
        currentquestion() {
            return this.$data.questions[this.$data.cursor]
        }
    },
    methods: {
        updatecursor: function() {
            if (this.$data.cursor === this.$data.numberofquestions) {
                this.$data.isfinalquestion = true
            } else {
                this.$data.cursor = this.$data.cursor + 1
            }
        }
    }
})