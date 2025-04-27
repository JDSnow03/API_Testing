<!--PubViewFeedbak
    This is where publisher can see the feedback left on their questions-->
<template>
  <div class="theme-publisher">
    <div class="top-banner">
      <!--banner contents-->
      <div class="banner-title">Draft Pool: {{ selectedTestBank }}</div>
      <div class="banner-actions">
        <router-link to="/PubHome" class="p_banner-btn">Home</router-link>
        <router-link to="/" class="p_banner-btn">Log Out</router-link>
      </div>
    </div>
    <!--page contents-->
    <div class="page-wrapper">
      <!--button to return to the draft pool-->
      <router-link :to="{
        path: '/PubViewTB',
        query: {
          name: selectedTestBank,
          textbook_id: textbookId,
          testbank_id: $route.query.testbank_id,
          title: $route.query.title
        }
      }">
        <button class="p_button">Return to Draft Pools</button>
      </router-link>

      <hr />
      <div id="feedbackContainer">
        <!--loading spinner-->
        <p v-if="loading">Loading feedback...</p>
        <p v-else-if="feedbackList.length === 0">No questions in this draft pool have feedback yet.</p>

        <div v-else>
          <!--displays questions if they have feedback-->
          <div v-for="(entry, index) in feedbackList" :key="index"
            :class="['p_question-box', { selected: selectedQuestionId === entry.question_id }]"
            @click="toggleQuestionSelection(entry.question_id)">
            <strong>Question {{ index + 1 }}:</strong> {{ entry.question_text }}

            <!-- Always show feedback -->
            <div v-if="entry.feedback && entry.feedback.length" class="feedback-section">
              <p><strong>Feedback:</strong></p>
              <!--displays comment and username of feedback-->
              <ul>
                <li v-for="(fb, i) in entry.feedback" :key="i">
                  "{{ fb.comment }}" — <em>{{ fb.username }} ({{ fb.role }})</em>
                </li>
              </ul>
            </div>
            <div v-else>
              <!-- No feedback yet -->
              <p>No feedback yet.</p>
            </div>

            <!-- add feedback button when question is selected-->
            <div v-if="selectedQuestionId === entry.question_id" class="p_button-group">
              <button @click.stop="openFeedbackForm(entry.question_id)">Leave Feedback</button>
            </div>
          </div>

          <!--Feedback popup -->
          <div v-if="showFeedbackForm" class="popup-overlay">
            <div class="form-popup-modal">
              <h2>Leave Feedback</h2>
              <textarea v-model="feedbackText" rows="5" placeholder="Enter your comment here..."></textarea>
              <br /><br />
              <button class="btn" @click="submitFeedback">Submit</button>
              <button class="btn cancel" @click="closeFeedbackForm">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Importing necessary modules and components
import api from '@/api';

export default {
  name: 'PubViewFeedback',
  data() {
    //data for the page
    return {
      testbankId: null,
      textbookId: this.$route.query.textbook_id || null,
      selectedTestBank: '',
      feedbackList: [],
      loading: true,
      userRole: '',
      selectedQuestionId: null,
      showFeedbackForm: false,
      selectedQuestionIdForFeedback: null,
      feedbackText: ''
    };
  },
  //grabs the testbank id for the title
  async mounted() {
    const query = this.$route.query;
    this.testbankId = parseInt(query.testbank_id);
    this.selectedTestBank = query.title || 'No Draft Pool Selected';

    const token = localStorage.getItem('token');
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      this.userRole = payload.role;
    }
    //automatically fetches feedback when the page loads
    this.fetchFeedbackByTestbank();
  },
  methods: {
    //This function fetches questions and feedback from the database
    async fetchFeedbackByTestbank() {
      try {
        const res = await api.get(`/feedback/${this.testbankId}/questions-with-feedback`);
        //saves the feedback
        this.feedbackList = res.data;
        console.log('Feedback loaded:', this.feedbackList);
        //if there is no feedback, it will show a message
      } catch (err) {
        console.error('Error loading feedback:', err);
        //stops the loading spinner
      } finally {
        this.loading = false;
      }
    },
    //This function allows the user to select a question
    toggleQuestionSelection(questionId) {
      this.selectedQuestionId = this.selectedQuestionId === questionId ? null : questionId;
    },
    //This function opens the feedback form
    openFeedbackForm(questionId) {
      this.selectedQuestionIdForFeedback = questionId;
      this.feedbackText = '';
      this.showFeedbackForm = true;
    },
    //This function closes the feedback form
    closeFeedbackForm() {
      this.selectedQuestionIdForFeedback = null;
      this.feedbackText = '';
      this.showFeedbackForm = false;
    },
    //This functions submits the feedback to the database
    async submitFeedback() {
      try {
        await api.post('/feedback/create', {
          //sends question id and comment to the database
          question_id: this.selectedQuestionIdForFeedback,
          comment_field: this.feedbackText
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        //closes form after submission
        this.closeFeedbackForm();

        const entry = this.feedbackList.find(q => q.question_id === this.selectedQuestionIdForFeedback);
        if (entry) {
          if (!entry.feedback) entry.feedback = [];
          entry.feedback.push({
            comment: this.feedbackText,
            username: 'You',
            role: this.userRole
          });
        }

      } catch (error) {
        console.error('Error submitting feedback:', error);
      }
    }
  }
};
</script>


<style scoped>
/* import styling*/
@import '../assets/publisher_styles.css';
</style>
