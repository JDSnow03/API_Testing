<!--PubNewTb
    This is the page where publishes create new draft pools-->
<template>
  <div class="theme-publisher">
    <div class="top-banner">
      <!--banner content-->
      <div class="banner-title">Create New Draft Pool</div>
      <div class="banner-actions">
        <router-link to="/PubHome" class="p_banner-btn">Home</router-link>
        <router-link to="/" class="p_banner-btn">Log Out</router-link>
      </div>
    </div>
    <!--page content-->
    <div class="center large-paragraph" style="color:#222">
      <form @submit.prevent="saveTestBank">
        <!-- all required info to make a draft pool-->
        <label for="bankName">Name of Draft Pool:</label>
        <input type="text" id="bankName" v-model="bankName" style="height:20px" required /><br>

        <label for="bankCh">Textbook Chapter:</label>
        <input type="text" id="bankCh" v-model="bankChapter" /><br>

        <label for="bankSec">Textbook Section:</label>
        <input type="text" id="bankSec" v-model="bankSection" /><br>

        <input type="submit" value="Submit" />
      </form>

      <div v-if="error" style="color: red; margin-top: 10px;">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  name: 'PublisherNewTB',
  data() {
    // data for the page
    return {
      bankName: '',
      bankChapter: '',
      bankSection: '',
      textbookId: this.$route.query.textbook_id || '',
      textbookTitle: this.$route.query.title || '',
      error: null
    };
  },
  methods: {
    //This function is used to save the new draft pool to the database
    async saveTestBank() {
      //makes sure all the fields are filled out
      if (this.bankName && this.bankChapter && this.bankSection && this.textbookId) {
        const testBankData = {
          //builds the draft pool object
          testbank_name: this.bankName,
          chapter_number: this.bankChapter,
          section_number: this.bankSection,
          textbook_id: this.textbookId
        };

        try {
          const response = await api.post('/testbanks/publisher', testBankData, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          // if successful, redirct to the questions page
          console.log('Test bank saved successfully:', response.data);
          this.$router.push({
            path: '/PubQuestions',
            query: {
              title: this.textbookTitle,
              textbook_id: this.textbookId
            }
          });
          // if unsuccessful, show error message
        } catch (error) {
          console.error('Error saving test bank:', error);
        }
        //if any fields are empty
      } else {
      }
    }
  }
};
</script>

<style scoped>
/* import publisher styling*/
@import '../assets/publisher_styles.css';

/* styling for this page*/
input[type="submit"] {
  background-color: rgb(48, 191, 223);
  color: black;
  font-size: 20px;
  padding: 10px 20px;
}

.form-row {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

input[type="text"] {
  width: 300px;
  padding: 10px 12px;
  font-size: 18px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  margin-left: 10px;
}

input[type="text"]:focus {
  border-color: rgb(48, 191, 223);
  box-shadow: 0 0 5px rgba(48, 191, 223, 0.5);
  outline: none;
}
</style>
