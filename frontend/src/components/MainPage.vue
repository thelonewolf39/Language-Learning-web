<template>
  <div class="container">
    <!-- Header / Navigation -->
    <header>
      <nav class="nav-bar">
        <h1>Language-Learning-Web</h1>
        <ul>
          <li><a href="#lessons">Lessons</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>
    </header>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Auth Section -->
      <div v-if="!user" class="auth-box">
        <h2>Login</h2>
        <input v-model="loginData.username" placeholder="Username" autocomplete="username" autocapitalize="none">
        <input v-model="loginData.password" type="password" placeholder="Password" autocomplete="current-password">
        <button @click="login">Login</button>
        <hr>
        <h2>Register</h2>
        <input v-model="registerData.username" placeholder="Username" autocomplete="username" autocapitalize="none">
        <input v-model="registerData.password" type="password" placeholder="Password" autocomplete="new-password">
        <button @click="register">Register</button>
      </div>

      <!-- Lessons Section -->
      <div v-else id="lessons">
        <LessonView v-if="selectedLesson" :lesson="selectedLesson" @back="selectedLesson = null" />
        <div v-else class="lessons-grid">
          <LessonCard
            v-for="lesson in lessons"
            :key="lesson.id"
            :lesson="lesson"
            @click="selectLesson(lesson)"
          />
        </div>
      </div>
    </div>

    <!-- About Section -->
    <section id="about" class="about-section">
      <h2>About this Project</h2>
      <p>
        Language-Learning-Web is a private, self-hosted language learning platform built with Vue and FastAPI.
        Our goal is to provide a safe, threat-free, and fully responsive environment to practice languages at your own pace.
      </p>
      <p>
        Features include user registration, lesson tracking, and fully responsive layouts with a polished, modern design.
      </p>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact-section">
      <h2>Contact</h2>
      <p>Have questions or feedback? You can reach out via your preferred method — this project is just for learning and testing!</p>
    </section>

    <!-- Footer -->
    <footer>
      &copy; 2025 Language-Learning-Web — Learning is fun! 🌿
    </footer>
  </div>
</template>

<script>
import LessonCard from './LessonCard.vue'
import LessonView from './LessonView.vue'

export default {
  components: { LessonCard, LessonView },
  data() {
    return {
      user: null,
      lessons: [],
      selectedLesson: null,
      registerData: { username: '', password: '' },
      loginData: { username: '', password: '' },
      apiUrl: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
    }
  },
  methods: {
    async register() { /* implement registration call */ },
    async login() {
      this.user = { username: this.loginData.username }
      const res = await fetch(`${this.apiUrl}/api/v1/lessons`)
      this.lessons = await res.json()
    },
    selectLesson(lesson) {
      this.selectedLesson = lesson
    }
  }
}
</script>

<style scoped>
/* Import modern font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* General container */
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(to bottom, #d0ebff, #ffffff);
  font-family: 'Inter', sans-serif;
  scroll-behavior: smooth;
}

/* Header Navigation */
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 1400px;
  margin-bottom: 40px;
}
.nav-bar h1 {
  font-size: 2.5rem;
  color: #1e40af;
}
.nav-bar ul {
  display: flex;
  gap: 25px;
  list-style: none;
}
.nav-bar a {
  text-decoration: none;
  color: #1e40af;
  font-weight: 600;
  transition: 0.3s;
}
.nav-bar a:hover { color: #2563eb; }

/* Main Content */
.main-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 30px;
}

/* Auth Box */
.auth-box {
  width: 90%;
  max-width: 400px;
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
}
.auth-box h2 { margin-bottom: 15px; color: #1e40af; }
.auth-box input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
  transition: 0.3s;
}
.auth-box input:focus {
  border-color: #2563eb;
  outline: none;
  box-shadow: 0 0 5px rgba(37,99,235,0.5);
}
.auth-box button {
  width: 100%;
  padding: 12px;
  border: none;
  background: linear-gradient(to right, #2563eb, #1e40af);
  color: white;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: 0.3s;
}
.auth-box button:hover { background: linear-gradient(to right, #1e40af, #2563eb); }

/* Lessons Grid */
.lessons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  width: 100%;
  max-width: 1000px;
  padding: 0 10px;
}

/* About Section */
.about-section {
  max-width: 900px;
  margin: 60px auto;
  padding: 25px;
  background-color: #f0f9ff;
  border-radius: 12px;
  box-shadow: 0px 10px 25px rgba(0,0,0,0.08);
  text-align: center;
}
.about-section h2 { font-size: 2rem; color: #1e40af; margin-bottom: 15px; }
.about-section p { color: #334155; font-size: 1.1rem; line-height: 1.6; margin-bottom: 10px; }

/* Contact Section */
.contact-section {
  max-width: 900px;
  margin: 60px auto;
  padding: 25px;
  background-color: #e0f2fe;
  border-radius: 12px;
  box-shadow: 0px 10px 25px rgba(0,0,0,0.08);
  text-align: center;
}
.contact-section h2 { font-size: 2rem; color: #1e40af; margin-bottom: 15px; }
.contact-section p { color: #334155; font-size: 1.1rem; line-height: 1.6; }

/* Footer */
footer {
  margin-top: 60px;
  color: #6b7280;
  font-size: 0.9rem;
  text-align: center;
}

/* Desktop Layout */
@media (min-width: 1024px) {
  .main-content {
    flex-direction: row;
    align-items: flex-start;
    gap: 50px;
  }
  .auth-box { flex: 1; }
  .lessons-grid { flex: 3; }
}

/* Tablet */
@media (max-width: 768px) {
  header h1 { font-size: 2rem; }
  .auth-box { padding: 20px; }
  .auth-box input, .auth-box button { font-size: 0.95rem; }
}

/* Mobile */
@media (max-width: 480px) {
  header h1 { font-size: 1.8rem; }
  .auth-box input, .auth-box button { font-size: 0.9rem; padding: 10px; }
}
</style>
