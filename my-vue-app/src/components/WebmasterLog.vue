<!-- WebmasterLog
    This is the page where the webmaster logs in-->
<template>
  <div class="theme-webmaster">
    <div class="top-banner">
      <!-- banner content-->
      <div class="banner-title">Webmaster Login</div>
    </div>
    <!--page content-->
    <div class="center large-paragraph" style="color: #222;">
      Please enter your webmaster username and password:
      <br />
      <br />
      <form @submit.prevent="submitForm">
        <!-- create username text box-->
        <label for="uname">Username:</label><br />
        <input type="text" id="uname" v-model="username" /><br />
        <br />
        <!-- create password textbox-->
        <label for="pass">Password:</label><br />
        <input type="password" id="pass" v-model="password" /><br /><br />
        <!-- submit button, when pressed it takes user to url specified-->
        <input type="submit" value="Submit" :disabled="loading" />
      </form>

      <!-- Show error message if user and password are entered incorrectly -->
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <!-- Show loading spinner if the form is submitting -->
      <div v-if="loading" class="loading-message">Logging in...</div>
    </div>
  </div>
</template>

<script>
//import necessary libraries and components
import api from '@/api';
import jwtDecode from 'jwt-decode';

export default {
  data() {
    //data used in the page
    return {
      username: '',
      password: '',
      errorMessage: '',
      loading: false
    };
  },
  mounted() {
    //Check if token exists and redirect if still valid
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        const currentTime = Date.now() / 1000;

        if (decoded.exp > currentTime && decoded.role === 'webmaster') {
          this.$router.push('/WebmasterHome');
        }
      } catch (error) {
        console.error('Invalid token', error);
      }
    }
  },
  methods: {
    //This function is used to submit the username and password
    async submitForm() {
      //verify the username and password are entered
      if (!this.username || !this.password) {
        this.errorMessage = "Please enter both username and password.";
        return;
      }
      //validate the username and password length
      if (this.username.trim().length < 3 || this.password.trim().length < 6) {
        this.errorMessage = "Username must be at least 3 characters and password at least 6 characters.";
        return;
      }

      this.loading = true;
      this.errorMessage = "";

      try {
        // Send login request 
        const res = await api.post('/auth/login', {
          username: this.username.toLowerCase(),
          password: this.password
        });

        const { token, user_id, role } = res.data;

        // Store token and identity in localStorage
        localStorage.setItem('token', token);
        localStorage.setItem('user_id', user_id);
        localStorage.setItem('role', role);

        // Redirect based on role
        if (role === 'webmaster') {
          this.$router.push('/WebmasterHome');
        } else {
          this.errorMessage = "Only webmasters can log in here.";
          localStorage.clear(); // Clear stored data for non-webmasters
        }
        //if login fails
      } catch (error) {
        if (!error.response) {
          this.errorMessage = "Network error. Please check your connection.";
        } else if (error.response.status === 401) {
          this.errorMessage = "Invalid username or password.";
        } else {
          this.errorMessage = (error.response && error.response.data && error.response.data.message) || "An error occurred during login.";
        }
        //stop loading spinner
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* import webmaster styling*/
@import '../assets/webmaster_styles.css';

/* styling for the login page*/

.error-message {
  color: rgb(174, 38, 38);
  margin-top: 10px;
}

.loading-message {
  color: #ffffff;
  margin-top: 10px;
}

input[type="submit"] {
  background-color: rgb(84, 178, 150);
  color: black;
  font-size: 20px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

input[type="submit"]:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

input[type="text"],
input[type="password"] {
  padding: 10px;
  font-size: 16px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.center {
  text-align: center;
}

.large-heading {
  font-size: 2em;
}

.large-paragraph {
  font-size: 1.2em;
}
</style>