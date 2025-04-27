<!--WebmasterHome
    This is where is webmaser can download database information-->
<template>
  <div class="theme-webmaster">
    <div class="top-banner">
      <!--banner content-->
      <div class="banner-title">Database Downloads</div>
      <div class="banner-actions">
        <router-link to="/" class="banner-btn">Log Out</router-link>
      </div>
    </div>
    <!--page content-->
    <div class="center large-paragraph" style="color: #222;">
      <div class="page-wrapper" style="font-size: 24px; text-align: center;">
        <h1>Select a dataset to download:</h1>
        <br>
        <strong>Note:</strong> Download All will download each file separately for readability.
        <hr>
        <!--buttons for each type of download-->
        <div class="button-row">
          <button class="button" @click="downloadData('users')">Download Users</button>
          <button class="button" @click="downloadData('textbook')">Download Textbooks</button>
          <button class="button" @click="downloadData('courses')">Download Courses</button>
          <button class="button" @click="downloadData('questions')">Download Questions</button>
          <button class="button" @click="downloadData('all')">Download All</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Importing the API module 
import api from '@/api';

export default {
  name: 'WebmasterHome',
  methods: {
    //This function lets the user download the selected dataset
    async downloadData(type) {
      //define the endpoints for api routes
      const endpoints = {
        users: 'users',
        courses: 'courses',
        textbook: 'textbook',
        questions: 'questions'
      };
      //loops through the endpoints and downloads each one
      if (type === 'all') {
        for (const [key, endpoint] of Object.entries(endpoints)) {
          await this.fetchAndDownload(endpoint, `${key}.csv`);
        }
        return;
      }
      //download the selected endpoint
      const endpoint = endpoints[type];
      if (!endpoint) {
        alert(`Unsupported download type: ${type}`);
        return;
      }

      await this.fetchAndDownload(endpoint, `${type}.csv`);
    },
    //This function fetches the data and downloads it as a CSV file
    async fetchAndDownload(endpoint, filename) {
      try {
        const response = await api.get(`/download/${endpoint}`, {
          responseType: 'blob'
        });
        //create a download link and click it to download the file
        const url = window.URL.createObjectURL(response.data);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error(`Download error for ${endpoint}:`, error);
      }
    }
  }
};
</script>


<style scoped>
/* import webmaster styling*/
@import '../assets/webmaster_styles.css';
</style>