<!--PubQuestions
    Page where publishers can view their questions, make new ones, select a draft pool, or create a new draft pool-->
<template>
  <div class="theme-publisher">
    <div class="top-banner">
      <!--banner contents-->
      <div class="banner-title">{{ textbookTitle }}</div>
      <div class="banner-actions">
        <router-link to="/PubHome" class="p_banner-btn">Home</router-link>
        <router-link to="/" class="p_banner-btn">Log Out</router-link>
      </div>
    </div>
    <!--page contents-->

    <!-- Edit Blocked Warning Popup: This will happen if the question is published/uneditable -->
    <div class="popup-overlay" v-if="editBlockedPopup">
      <div class="form-popup-modal">
        <h2>Cannot Edit Question</h2>
        <p>{{ editBlockedReason }}</p>
        <p>A new copy will be made instead.</p>
        <button class="btn" @click="createCopyInstead">Create a Copy</button>
        <button class="btn cancel" @click="editBlockedPopup = false">Cancel</button>
      </div>
    </div>
    <div class="page-wrapper">
      <div class="button-row">
        <!--dropdown that shows all of the available draft pools to choose from-->
        <div class="p_dropdown">
          <button class="p_dropbtn">
            {{ selectedTestBank ? selectedTestBank.name : 'Select Draft Pool' }}
          </button>
          <div class="p_dropdown-content">
            <a v-for="tb in testBanks" :key="tb.testbank_id" href="#" @click.prevent="selectTestBank(tb)">
              {{ tb.name }}
            </a>
          </div>
        </div>
        <!--when draft pool is selected, it takes them to the correct draft pool page-->
        <router-link :to="{ path: 'PubNewTB', query: { title: textbookTitle, textbook_id: textbookId } }">
          <button class="p_button">New Draft Pool</button>
        </router-link>

        <!--question type dropdown, displays questions of that type when selected-->
        <div class="p_dropdown">
          <button class="p_dropbtn">Question Type</button>
          <div class="p_dropdown-content">
            <a @click="fetchQuestions('True/False')">True/False</a>
            <a @click="fetchQuestions('Multiple Choice')">Multiple Choice</a>
            <a @click="fetchQuestions('Matching')">Matching</a>
            <a @click="fetchQuestions('Fill in the Blank')">Fill in the Blank</a>
            <a @click="fetchQuestions('Short Answer')">Short Answer</a>
            <a @click="fetchQuestions('Essay')">Essay</a>
          </div>
        </div>

        <!--create new question-->
        <button class="p_button" @click="edit">New Question</button>
      </div>

      <!-- Optional display of selected type -->
      <div id="selectedQuestionType" style="color: #222;" class="center large-paragraph">
        {{ selectedQuestionType }}
      </div>

      <hr />

      <!-- Question List Display -->
      <!--shows each question and relevant information inside a box-->
      <ul>
        <div v-for="(question, index) in questions" :key="index" class="p_question-box"
          :class="{ selected: selectedQuestionId === question.id }" @click="toggleQuestionSelection(question.id)">
          <strong>Question {{ index + 1 }}:</strong> {{ question.text }}<br>
          <span><strong>Type:</strong> {{ question.type }}</span><br>
          <span><strong>Chapter:</strong> {{ question.chapter || 'N/A' }}</span><br>
          <span><strong>Section:</strong> {{ question.section || 'N/A' }}</span><br>
          <span><strong>Points:</strong> {{ question.points }}</span><br>
          <span><strong>Estimated Time:</strong> {{ question.time }} minutes</span><br>

          <!--New Image Section -->
          <div v-if="question.image_url" style="margin-top: 10px;">
            <strong>Attached Image:</strong><br />
            <img :src="question.image_url" alt="Attached Image" style="max-width: 100%; margin-top: 5px;" />
          </div>

          <div v-if="question.type === 'True/False'">
            <strong>Answer:</strong> {{ question.answer ? 'True' : 'False' }}
          </div>

          <div v-if="question.type === 'Multiple Choice'">
            <strong>Correct Answer:</strong>
            {{ (question.correctOption && question.correctOption.option_text) || 'Not specified' }}<br>

            <strong>Other Options:</strong>
            <ul>
              <li v-for="(option, i) in question.incorrectOptions" :key="i">{{ option.option_text }}</li>
            </ul>
          </div>

          <div v-if="question.type === 'Matching'">
            <strong>Pairs:</strong>
            <ul>
              <li v-for="(pair, i) in question.pairs" :key="i">{{ pair.term }} - {{ pair.definition }}</li>
            </ul>
          </div>

          <div v-if="question.type === 'Fill in the Blank'">
            <strong>Correct Answer(s):</strong>
            <ul>
              <li v-for="(blank, i) in question.blanks" :key="i">{{ blank.correct_text }}</li>
            </ul>
          </div>

          <span><strong>Grading Instructions:</strong> {{ question.instructions || 'None' }}</span>

          <!--buttons for each question-->
          <div v-if="selectedQuestionId === question.id" class="p_button-group">
            <button v-if="!question.is_published" @click.stop="editQuestion(question)">Edit</button>
            <button v-if="!question.is_published" @click.stop="deleteQuestion(question.id)">Delete</button>
            <button @click.stop="openAddToTestBank(question.id)">Add to Draft Pool</button>
          </div>
        </div>
      </ul>

      <!-- Add to Test Bank Modal -->
      <div class="popup-overlay" v-if="showAddToTBModal">
        <div class="form-popup-modal">
          <h2 style="text-align: center;">Select Draft Pool</h2>
          <div class="form-container"
            style="display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 1rem;">
            <button v-for="tb in testBanks.filter(tb => !tb.is_published)" :key="tb.testbank_id" class="t_button"
              style="width: 100%;" @click="assignQuestionToTestBank(tb.testbank_id)">
              {{ tb.name }}
            </button>
            <button type="button" class="btn cancel" style="width: 100%;" @click="closeAddToTBModal">
              Close
            </button>
          </div>
        </div>
      </div>

      <!-- Popup Overlay -->
      <div class="popup-overlay" v-show="showForm">
        <div class="form-popup-modal">
          <form class="form-container" @submit.prevent="handleQuestionSave">
            <h1>{{ editingQuestionId ? 'Edit Question' : 'New Question' }}</h1>

            <label><b>Chapter Number</b></label>
            <input type="text" v-model="questionData.chapter" required />

            <label><b>Section Number</b></label>
            <input type="text" v-model="questionData.section" required />

            <label><b>Question Type</b><br /></label>

            <!-- Show a disabled select in view-only mode when editing -->
            <div v-if="editingQuestionId">
              <input type="text" :value="selectedQuestionType" disabled class="readonly-input" />
            </div>
            <!-- Allow selecting type only if creating -->
            <div v-else>
              <select v-model="selectedQuestionType" required>
                <option disabled value="">Select a type</option>
                <option>True/False</option>
                <option>Multiple Choice</option>
                <option>Matching</option>
                <option>Fill in the Blank</option>
                <option>Short Answer</option>
                <option>Essay</option>
              </select>
            </div>

            <br /><br />
            <label><b>Question Text</b></label>
            <input type="text" v-model="questionData.question" required />

            <!-- Conditional Fields -->
            <div v-if="selectedQuestionType === 'True/False'">
              <label><b>Answer</b></label>
              <select v-model="questionData.answer">
                <option value="True">True</option>
                <option value="False">False</option>
              </select>
            </div>

            <div v-if="selectedQuestionType === 'Multiple Choice'">
              <label><b>Correct Answer</b></label>
              <input type="text" v-model="questionData.answer" />
              <label><b>Incorrect Answer Choices (comma-separated)</b></label>
              <input type="text" v-model="questionData.answerChoices" />
            </div>

            <div v-if="selectedQuestionType === 'Matching'">
              <label><b>Matching Pairs</b></label>
              <div v-for="(pair, index) in matchingPairs" :key="index">
                <input type="text" v-model="pair.term" placeholder="Term" />
                <input type="text" v-model="pair.definition" placeholder="Definition" />
                <button type="button" @click="removePair(index)">Remove</button>
              </div>
              <button type="button" @click="addPair">Add Pair</button>
            </div>

            <div v-if="selectedQuestionType === 'Fill in the Blank'">
              <label><b>Correct Answer</b></label>
              <input type="text" v-model="questionData.answer" />
            </div>

            <div v-if="selectedQuestionType === 'Essay'">
            </div>

            <br />
            <label><b>Points Worth</b></label>
            <input type="text" v-model="questionData.points" required />

            <label><b>Estimated Time (in minutes)</b></label>
            <input type="text" v-model="questionData.time" required />

            <label><b>Grading Instructions</b></label>
            <input type="text" v-model="questionData.instructions" required />

            <label><b>Attached Image</b></label>
            <!-- Show existing image when editing -->
            <div v-if="editingQuestionId && imagePreview">
              <img :src="imagePreview" alt="Attached" style="max-width: 100%;" />
            </div>

            <!-- Only allow upload when creating -->
            <div v-else>
              <input type="file" @change="handleImageUpload" accept="image/*" />
              <img v-if="imagePreview" :src="imagePreview" alt="Preview" style="max-width: 100%;" />
            </div>
            <br /><br />

            <button type="submit" class="btn">Save</button>
            <button type="button" class="btn cancel" @click="closeForm">Close</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//importing the api file to make requests to the backend
import api from '@/api';

export default {
  name: 'PubQuestions',
  //data that is used in the page
  data() {
    return {
      textbookTitle: '',
      textbookId: '',
      testBanks: [],
      selectedTestBank: null,
      selectedQuestionType: '',
      questions: [],
      selectedQuestionId: null,
      showForm: false,
      showAddToTBModal: false,
      questionToAddToTB: null,
      matchingPairs: [],
      imagePreview: '',
      editingQuestionId: null,
      oldMCOptionIds: [],
      editBlockedPopup: false,
      editBlockedReason: '',
      questionData: {
        chapter: '',
        section: '',
        question: '',
        reference: '',
        answer: '',
        answerChoices: '',
        points: '',
        time: '',
        instructions: '',
        imageFile: null
      }
    };
  },
  methods: {
    //this function is used to save questions (create or edit) to the database
    async handleQuestionSave() {
      try {
        let postData;
        let config;
        const isEditing = !!this.editingQuestionId;
        const editingQuestion = this.questions.find(q => q.id === this.editingQuestionId);

        //image upload handling
        if (this.questionData.imageFile) {
          //image data
          postData = new FormData();

          postData.append('file', this.questionData.imageFile);
          postData.append('question_text', this.questionData.question);
          postData.append('default_points', this.questionData.points);
          postData.append('est_time', this.questionData.time);
          postData.append('chapter_number', this.questionData.chapter);
          postData.append('section_number', this.questionData.section);
          postData.append('grading_instructions', this.questionData.instructions);
          postData.append('type', this.selectedQuestionType);
          postData.append('source', 'manual');
          postData.append('textbook_id', this.textbookId);

          //handling for each question type
          if (this.selectedQuestionType === 'True/False') {
            postData.append('true_false_answer', this.questionData.answer === 'True');
          } else if (this.selectedQuestionType === 'Multiple Choice') {
            const incorrectChoices = this.questionData.answerChoices
              .split(',')
              .map(c => c.trim())
              .filter(Boolean);

            const options = [
              { option_text: this.questionData.answer.trim(), is_correct: true },
              ...incorrectChoices.map(choice => ({
                option_text: choice,
                is_correct: false
              }))
            ];
            postData.append('options', JSON.stringify(options));
          } else if (this.selectedQuestionType === 'Matching') {
            postData.append('matches', JSON.stringify(
              this.matchingPairs.map(pair => ({
                prompt_text: pair.term,
                match_text: pair.definition
              }))
            ));
          } else if (this.selectedQuestionType === 'Fill in the Blank') {
            postData.append('blanks', JSON.stringify([{ correct_text: this.questionData.answer }]));
          } else if (this.selectedQuestionType === 'Short Answer') {
            postData.append('answer', this.questionData.answer);
          } else if (this.selectedQuestionType === 'Essay') {
            postData.append('grading_instructions', this.questionData.instructions);
          }

          // debugging log
          for (let [key, val] of postData.entries()) {
            console.log(`${key}:`, val);
          }

          config = {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'multipart/form-data'
            }
          };
        } else {
          // JSON fallback when no image is uploaded
          postData = {
            question_text: this.questionData.question,
            default_points: parseInt(this.questionData.points),
            est_time: parseInt(this.questionData.time),
            chapter_number: this.questionData.chapter,
            section_number: this.questionData.section,
            grading_instructions: this.questionData.instructions,
            type: this.selectedQuestionType,
            source: 'manual',
            textbook_id: this.textbookId
          };

          if (this.selectedQuestionType === 'True/False') {
            postData.true_false_answer = this.questionData.answer === 'True';
          } else if (this.selectedQuestionType === 'Multiple Choice') {
            const incorrectChoices = this.questionData.answerChoices
              .split(',')
              .map(c => c.trim())
              .filter(Boolean);

            postData.options = [
              { option_text: this.questionData.answer.trim(), is_correct: true },
              ...incorrectChoices.map(choice => ({ option_text: choice, is_correct: false }))
            ];
            if (isEditing && this.oldMCOptionIds.length > 0) {
              postData.to_delete = this.oldMCOptionIds;
            }
          } else if (this.selectedQuestionType === 'Matching') {
            postData.matches = this.matchingPairs.map(pair => ({
              prompt_text: pair.term,
              match_text: pair.definition
            }));
            if (isEditing && editingQuestion) {
              const oldMatchIds = (editingQuestion.pairs || []).map(p => p.match_id);
              postData.to_delete = oldMatchIds;
            }
          } else if (this.selectedQuestionType === 'Fill in the Blank') {
            postData.blanks = [{ correct_text: this.questionData.answer }];
          } else if (this.selectedQuestionType === 'Short Answer') {
            postData.answer = this.questionData.answer;
          } else if (this.selectedQuestionType === 'Essay') {
            postData.grading_instructions = this.questionData.instructions;
          }

          config = {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          };
        }
        //do correct API request depending on if it is a new question or an edit
        if (isEditing) {
          await api.patch(`/questions/${this.editingQuestionId}`, postData, config);
        } else {
          await api.post('/questions', postData, config);
        }

        //after saving
        this.closeForm();
        this.resetForm();
        this.fetchQuestions(this.selectedQuestionType);

        //if there is an error
      } catch (err) {
        let serverMsg = 'Something went wrong.';
        if (err && err.response && err.response.data) {
          serverMsg = err.response.data.error || err.response.data.message || serverMsg;
        }
        alert('Save failed: ' + serverMsg);
        console.error('Error saving question:', err);
      }
    },

    //This function fetches all of the testbanks for the textbook
    async fetchTestBanks() {
      try {
        const response = await api.get('/testbanks/publisher', {
          params: { textbook_id: this.textbookId },
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        //stores testbanks
        this.testBanks = response.data.testbanks;
        //error handling
      } catch (error) {
        console.error('Error loading test banks:', error);
      }
    },
    //This functions shows the questions of the selected type
    async fetchQuestions(type) {
      //which type of question is being shown
      this.selectedQuestionType = type;
      try {
        const response = await api.get(`/questions`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
          params: { textbook_id: this.textbookId, type: type }
        });
        if (Array.isArray(response.data.questions)) {
          //process the questions
          this.questions = response.data.questions.map((question) => {
            const base = {
              text: question.question_text,
              type: question.type,
              points: question.default_points,
              id: question.id,
              instructions: question.grading_instructions || '',
              time: question.est_time,
              chapter: question.chapter_number,
              section: question.section_number,
              image_url: question.attachment && question.attachment.url ? question.attachment.url : '',
              is_published: question.is_published || false
            };
            //extra information for each question type
            switch (question.type) {
              case 'True/False': return { ...base, answer: question.true_false_answer };
              case 'Multiple Choice': return { ...base, correctOption: question.correct_option || null, incorrectOptions: question.incorrect_options || [] };
              case 'Matching': return { ...base, pairs: (question.matches || []).map(pair => ({ term: pair.prompt_text, definition: pair.match_text })) };
              case 'Fill in the Blank': return { ...base, blanks: question.blanks || [] };
              case 'Short Answer': return base;
              case 'Essay': return base;
              default: return base;
            }
          });
          //if there are no questions, show a message
        } else {
          this.questions = [];
        }
        //error handling
      } catch (error) {
        console.error('Error fetching questions:', error);
        this.questions = [];
      }
    },
    //This function shows the add to testbank modal
    openAddToTestBank(questionId) {
      this.questionToAddToTB = questionId;
      this.showAddToTBModal = true;
    },
    //This function closes the add to testbank modal
    closeAddToTBModal() {
      this.questionToAddToTB = null;
      this.showAddToTBModal = false;
    },
    //This function assigns the question to the draft pool
    async assignQuestionToTestBank(testbankId) {
      //makes sure the question is selected
      if (!this.questionToAddToTB) return;
      try {
        await api.post(`/testbanks/publisher/${testbankId}/questions`, {
          question_ids: [this.questionToAddToTB]
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        //if successful, show a message and close the modal
        alert('Question successfully added to testbank!');
        this.closeAddToTBModal();
        //if unsuccessful, show an error message
      } catch (error) {
        console.error('Failed to add question to testbank:', error);
        let errMsg = 'Failed to add question.';
        if (error.response && error.response.data && error.response.data.error) {
          errMsg = error.response.data.error;
        }
      }
    },
    //This function redirects the user to the selected draft pool page
    selectTestBank(tb) {
      this.$router.push({
        name: 'PubViewTB',
        query: {
          testbank_id: tb.testbank_id,
          name: tb.name,
          title: this.textbookTitle,
          textbook_id: this.textbookId,
          chapter: tb.chapter_number,
          section: tb.section_number
        }
      });
    },
    //This function allows the user to select a question
    toggleQuestionSelection(id) {
      this.selectedQuestionId = this.selectedQuestionId === id ? null : id;
    },
    //This function allows the user to select a question type to show
    selectQuestionType(type) {
      this.selectedQuestionType = type;
      this.edit();
    },
    //This function opens the form to edit or create a question
    edit() {
      this.showForm = true;
    },
    //This function closes the form and resets the data
    closeForm() {
      this.showForm = false;
      this.resetForm();
    },
    //This function adds a new matching pair to the create/edit form
    addPair() {
      this.matchingPairs.push({ term: '', definition: '' });
    },
    //This function removes a matching pair from the create/edit form
    removePair(index) {
      this.matchingPairs.splice(index, 1);
    },
    //This function handles the image upload for the question
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.questionData.imageFile = file;
        const reader = new FileReader();
        // Show a preview of the image
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    //This function rests the fields in the form
    resetForm() {
      this.questionData = {
        chapter: '',
        section: '',
        question: '',
        reference: '',
        answer: '',
        answerChoices: '',
        points: '',
        time: '',
        instructions: '',
        imageFile: null
      };
      this.selectedQuestionType = '';
      this.matchingPairs = [];
      this.imagePreview = '';
      this.editingQuestionId = null;
      this.oldMCOptionIds = [];

      //Clear the file input manually
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) fileInput.value = '';
    },

    //This function allows the the user to edit a question
    async editQuestion(question) {
      try {
        const res = await api.get(`/questions/${question.id}/used_in`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (res.data.is_used) {
          // Question is used in a published/final test
          this.editBlockedReason = `This question is used in a "${res.data.tests[0].status}" test: "${res.data.tests[0].name}".`;
          this.editingQuestionId = question.id;
          this.editBlockedPopup = true;
          return;
        }
      } catch (err) {
        console.error('Error checking question status:', err);
        alert('Could not verify question status.');
        return;
      }

      // If not used, proceed with editing
      this.editingQuestionId = question.id;
      this.questionData.question = question.text;
      this.questionData.chapter = question.chapter;
      this.questionData.section = question.section;
      this.questionData.points = question.points;
      this.questionData.time = question.time;
      this.questionData.instructions = question.instructions;
      this.questionData.answer = question.answer || '';
      this.selectedQuestionType = question.type;

      // Show existing image if editing
      this.imagePreview = question.image_url || '';

      if (question.type === 'Multiple Choice') {
        this.questionData.answer = (question.correctOption && question.correctOption.option_text) || ''; this.questionData.answerChoices = question.incorrectOptions.map(opt => opt.option_text).join(', ');
        this.oldMCOptionIds = [];
        if (question.correctOption && question.correctOption.option_id) {
          this.oldMCOptionIds.push(question.correctOption.option_id);
        }
        if (Array.isArray(question.incorrectOptions)) {
          question.incorrectOptions.forEach(opt => {
            if (opt.option_id) this.oldMCOptionIds.push(opt.option_id);
          });
        }
      } else if (question.type === 'Matching') {
        this.matchingPairs = question.pairs.map(pair => ({
          term: pair.term,
          definition: pair.definition
        }));
      }

      this.showForm = true;
    },
    //This function allows the user to delete a question
    async deleteQuestion(id) {
      if (confirm('Are you sure you want to delete this question?')) {
        try {
          await api.delete(`/questions/${id}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          this.questions = this.questions.filter(q => q.id !== id);
        } catch (err) {
          console.error(err);
          alert('Failed to delete question.');
        }
      }
    },
    //This function creats a copy of the question if it cannot be edited
    async createCopyInstead() {
      try {
        const res = await api.post(`/questions/${this.editingQuestionId}/copy_to_textbook`, {
          textbook_id: this.textbookId
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        alert('A copy of the question was created. You can now edit it.');
        this.editBlockedPopup = false;
        this.fetchQuestions(this.selectedQuestionType); // reload with new question included
      } catch (err) {
        console.error('Failed to create copy:', err);
        alert('Failed to create a copy of this question.');
      }
    }
  },
  //when the page is loaded, it gets the textbook title and id from the URL and fetches the draft pools
  mounted() {
    this.textbookTitle = this.$route.query.title || 'Book Title';
    this.textbookId = this.$route.query.textbook_id || '';
    if (this.textbookId) {
      this.fetchTestBanks();
    }
  }
};
</script>

<style scoped>
/* import publisher styles*/
@import '../assets/publisher_styles.css';
</style>
