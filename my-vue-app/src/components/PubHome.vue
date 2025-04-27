<!--Pub Home
  This page is where the publisher chooses what textbook to work in-->
<template>
  <!--Banner contents-->
  <div class="theme-publisher">
    <div class="top-banner">
      <div class="banner-title">Textbook Selection</div>

      <div class="banner-actions">
        <router-link to="/" class="p_banner-btn">Log Out</router-link>
      </div>
    </div>
    <!-- page contents-->
    <div class="center large-paragraph" style="color:#222">
      <div class="page-wrapper">

        Please select or add a textbook:

        <div class="button-row">
          <!--selecting a textbook will be a drop down menu with all previous books-->
          <!--If else that ensures there are textbooks to select from-->
          <div class="p_dropdown" v-if="textbooks.length">
            <button class="p_dropbtn">Select Textbook</button>
            <div class="p_dropdown-content">
              <!-- link will take user to correct questions page when textbook is selectd-->
              <router-link v-for="textbook in textbooks" :key="textbook.id"
                :to="{ path: 'PubQuestions', query: { title: textbook.title, textbook_id: textbook.id } }">
                {{ textbook.title }}
              </router-link>
            </div>
          </div>
          <!--if there are no textbooks-->
          <div v-else>
            No courses available.
          </div>
          <!--creating a new textbook will take user to new page-->
          <router-link to="PubNewBook">
            <button class="p_button">Add New Textbook</button>
          </router-link>
          <br>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Importing necessary modules and components
import api from '@/api';
import jwtDecode from 'jwt-decode';

export default {
  name: 'PublisherHome',
  data() {
    return {
      textbooks: [],
      error: null,
    };
  },
  created() {
    this.fetchTextbooks();
  },
  methods: {
    //This function fetches the textbooks from the database
    async fetchTextbooks() {
      try {
        console.log('Fetching textbooks...'); // Debugging log

        const response = await api.get('/textbooks', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        console.log('Textbooks fetched:', response.data); // Debugging log that shows the textbooks

        if (response.data && response.data.textbooks) {
          //stores data if properly fetched
          this.textbooks = response.data.textbooks;
        } else {
          // error message if improperly fetched
          this.error = 'Failed to fetch textbooks data.';
        }
        //error handling
      } catch (error) {
        console.error('Error fetching textbooks:', error);

        // Check if error has a response from the backend
        if (error.response) {
          this.error = `Error: ${error.response.status} - ${error.response.data.message || error.response.statusText}`;
        } else {
          this.error = 'Network error or server is not responding.';
        }
      }
    }
  }
};
</script>

<style scoped>
/* import publisher styles */
@import '../assets/publisher_styles.css';

/* Dropdown styling*/
.dropbtn {
  background-color: rgb(48, 191, 223);
  color: black;
  padding: 10px;
  font-size: 20px;
  border: none;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 10px 15px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: rgb(48, 191, 223);
}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown:hover .dropbtn {
  background-color: rgb(40, 151, 176);
}
</style>