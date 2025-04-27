<!-- PubNewBook
    This is the page where publisher create a new textbook -->
<template>
  <div class="theme-publisher">
    <div class="top-banner">
      <!--banner contents-->
      <div class="banner-title">Add New Textbook</div>
      <div class="banner-actions">
        <router-link to="/PubHome" class="p_banner-btn">Home</router-link>
        <router-link to="/" class="p_banner-btn">Log Out</router-link>
      </div>
    </div>
    <!--page contents-->
    <div class="center large-paragraph" style="color:#222">
      <!-- textboxes for each of the required sections of information-->
      <form @submit.prevent="saveBook">
        <label for="textbookTitle">Textbook Title:</label>
        <input type="text" id="textbookTitle" v-model="textbookTitle" style="height:20px"><br>

        <label for="author">Author:</label>
        <input type="text" id="author" v-model="author" style="height:20px"><br>

        <label for="ISBN">ISBN:</label>
        <input type="text" id="ISBN" v-model="ISBN" style="height:20px"><br>

        <label for="version">Version:</label>
        <input type="text" id="version" v-model="version" style="height:20px"><br>

        <label for="websiteLink">Website Link:</label>
        <input type="text" id="websiteLink" v-model="websiteLink" style="height:20px"><br>

        <div class="center large-heading">
          <input type="submit" value="Save">
        </div>
      </form>
    </div>
  </div>
</template>
<script>
// Importing the necessary modules and components
import api from '@/api'

export default {
  name: 'PublisherNewBook',
  data() {
    //data used in the page
    return {
      textbookTitle: '',
      author: '',
      ISBN: '',
      version: '',
      websiteLink: ''
    };
  },
  methods: {
    //This function is used to save the textbook to the database
    async saveBook() {
      // verify all fields are filled out
      if (this.textbookTitle && this.author && this.ISBN && this.version) {
        const bookData = {
          //create new book object with the data from the textboxes
          textbook_title: this.textbookTitle,
          textbook_author: this.author,
          textbook_isbn: this.ISBN,
          textbook_version: this.version,
          websiteLink: this.websiteLink
        };

        // try to save the book
        try {
          const response = await api.post('/textbooks', bookData, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          });
          //if successful, sends user to the home page
          console.log('Book saved successfully:', response.data);
          this.$router.push({
            path: '/PubHome'
          }
          );
          //if not successful, alert the user
        }
        catch (error) {
          console.error('Error saving book:', error);
          alert('Failed to save the book. Please try again.');
        }
        //if fields are missing
      } else {
        alert('Please fill out all fields.');
      }
    }
  }
};
</script>

<style scoped>
/* Import styles*/
@import '../assets/publisher_styles.css';

/* custom font size */
.small-font {
  font-size: 15x;
}
</style>