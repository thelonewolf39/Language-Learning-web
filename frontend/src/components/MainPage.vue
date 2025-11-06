<template>
  <div class="container">
    <!-- Header / Navigation -->
    <header>
      <nav class="nav-bar">
        <h1>Language-Learning-Web</h1>
        <div v-if="user" class="nav-user-section">
          <div class="user-info">
            <div class="user-avatar">
              <img v-if="user.avatar_style && user.avatar_seed"
                   :src="`https://api.dicebear.com/7.x/${user.avatar_style}/svg?seed=${user.avatar_seed}`"
                   :alt="user.username">
              <span v-else class="identicon">{{ getIdenticon(user.username) }}</span>
            </div>
            <div class="user-details">
              <span class="username">{{ user.username }}</span>
              <span class="points">💎 {{ user.total_points }} pts</span>
            </div>
          </div>
          <ul class="nav-links">
            <li><a @click="currentView = 'lessons'" :class="{ active: currentView === 'lessons' }">Lessons</a></li>
            <li><a @click="currentView = 'achievements'" :class="{ active: currentView === 'achievements' }">Achievements</a></li>
            <li><a @click="currentView = 'shop'" :class="{ active: currentView === 'shop' }">Shop</a></li>
            <li><a @click="currentView = 'profile'" :class="{ active: currentView === 'profile' }">Profile</a></li>
            <li><a @click="logout" class="logout-btn">Logout</a></li>
          </ul>
        </div>
        <ul v-else class="nav-links">
          <li><a href="#about">About</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>
    </header>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Auth Section -->
      <div v-if="!user" class="auth-box">
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="success" class="success-message">{{ success }}</div>

        <h2>Login</h2>
        <input v-model="loginData.username" placeholder="Username" autocomplete="username" autocapitalize="none" @keyup.enter="login">
        <input v-model="loginData.password" type="password" placeholder="Password" autocomplete="current-password" @keyup.enter="login">
        <button @click="login" :disabled="loading">{{ loading ? 'Loading...' : 'Login' }}</button>
        <hr>
        <h2>Register</h2>
        <input v-model="registerData.username" placeholder="Username" autocomplete="username" autocapitalize="none" @keyup.enter="register">
        <input v-model="registerData.password" type="password" placeholder="Password" autocomplete="new-password" @keyup.enter="register">
        <button @click="register" :disabled="loading">{{ loading ? 'Loading...' : 'Register' }}</button>
      </div>

      <!-- Logged In Views -->
      <div v-else class="app-views">
        <!-- Lessons View -->
        <div v-if="currentView === 'lessons'" class="view-content">
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

        <!-- Achievements View -->
        <AchievementsView
          v-if="currentView === 'achievements'"
          :authToken="authToken"
        />

        <!-- Avatar Shop View -->
        <AvatarShop
          v-if="currentView === 'shop'"
          :userPoints="user.total_points"
          :currentStyle="user.avatar_style"
          :authToken="authToken"
          @points-updated="updateUserPoints"
          @avatar-changed="updateUserAvatar"
          @back="currentView = 'lessons'"
        />

        <!-- Profile Settings View -->
        <ProfileSettings
          v-if="currentView === 'profile'"
          :user="user"
          :authToken="authToken"
          @back="currentView = 'lessons'"
        />
      </div>
    </div>

    <!-- About Section -->
    <section v-if="!user" id="about" class="about-section">
      <h2>About this Project</h2>
      <p>
        Language-Learning-Web is a private, self-hosted language learning platform built with Vue and FastAPI.
        Our goal is to provide a safe, threat-free, and fully responsive environment to practice languages at your own pace.
      </p>
      <p>
        Features include user registration, lesson tracking, achievements system, avatar shop, and developer API with comprehensive statistics.
      </p>
    </section>

    <!-- Contact Section -->
    <section v-if="!user" id="contact" class="contact-section">
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
import AchievementsView from './AchievementsView.vue'
import AvatarShop from './AvatarShop.vue'
import ProfileSettings from './ProfileSettings.vue'

export default {
  components: {
    LessonCard,
    LessonView,
    AchievementsView,
    AvatarShop,
    ProfileSettings
  },
  data() {
    return {
      user: null,
      authToken: null,
      lessons: [],
      selectedLesson: null,
      currentView: 'lessons',
      registerData: { username: '', password: '' },
      loginData: { username: '', password: '' },
      loading: false,
      error: null,
      success: null,
      apiUrl: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
    }
  },
  async mounted() {
    // Check for stored auth token
    const storedToken = localStorage.getItem('authToken')
    const storedUser = localStorage.getItem('user')

    if (storedToken && storedUser) {
      this.authToken = storedToken
      this.user = JSON.parse(storedUser)
      await this.loadLessons()
    }
  },
  methods: {
    async register() {
      this.error = null
      this.success = null
      this.loading = true

      try {
        const response = await fetch(`${this.apiUrl}/api/v1/users/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.registerData)
        })

        if (!response.ok) {
          const error = await response.json()
          this.error = error.detail || 'Registration failed'
          return
        }

        this.success = 'Registration successful! Please login.'
        this.registerData = { username: '', password: '' }
      } catch (err) {
        this.error = 'Network error. Please try again.'
      } finally {
        this.loading = false
      }
    },

    async login() {
      this.error = null
      this.success = null
      this.loading = true

      try {
        const response = await fetch(`${this.apiUrl}/api/v1/users/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.loginData)
        })

        if (!response.ok) {
          const error = await response.json()
          this.error = error.detail || 'Login failed'
          return
        }

        const data = await response.json()
        this.authToken = data.access_token
        this.user = data.user

        // Store in localStorage
        localStorage.setItem('authToken', this.authToken)
        localStorage.setItem('user', JSON.stringify(this.user))

        // Load lessons
        await this.loadLessons()

        this.loginData = { username: '', password: '' }
      } catch (err) {
        this.error = 'Network error. Please try again.'
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        await fetch(`${this.apiUrl}/api/v1/users/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.authToken}`
          }
        })
      } catch (err) {
        console.error('Logout error:', err)
      }

      // Clear local data
      this.user = null
      this.authToken = null
      this.lessons = []
      this.currentView = 'lessons'
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
    },

    async loadLessons() {
      try {
        const response = await fetch(`${this.apiUrl}/api/v1/lessons`)
        this.lessons = await response.json()
      } catch (err) {
        console.error('Failed to load lessons:', err)
      }
    },

    selectLesson(lesson) {
      this.selectedLesson = lesson
    },

    updateUserPoints(newPoints) {
      this.user.total_points = newPoints
      localStorage.setItem('user', JSON.stringify(this.user))
    },

    updateUserAvatar({ style, seed }) {
      this.user.avatar_style = style
      this.user.avatar_seed = seed
      localStorage.setItem('user', JSON.stringify(this.user))
    },

    getIdenticon(username) {
      const emojis = ['😀', '😎', '🤓', '🥳', '🤩', '😇', '🥰', '😊', '🤗', '😺', '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐸', '🐵']
      let hash = 0
      for (let i = 0; i < username.length; i++) {
        hash = username.charCodeAt(i) + ((hash << 5) - hash)
      }
      return emojis[Math.abs(hash) % emojis.length]
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
  flex-wrap: wrap;
  gap: 20px;
}
.nav-bar h1 {
  font-size: 2.5rem;
  color: #1e40af;
}

/* User Section in Nav */
.nav-user-section {
  display: flex;
  align-items: center;
  gap: 30px;
  flex-wrap: wrap;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  padding: 8px 16px;
  border-radius: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  display: flex;
  align-items: center;
  justify-content: center;
}
.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.identicon {
  font-size: 1.5rem;
}
.user-details {
  display: flex;
  flex-direction: column;
}
.username {
  font-weight: 700;
  color: #1e40af;
  font-size: 0.95rem;
}
.points {
  font-size: 0.85rem;
  color: #f59e0b;
  font-weight: 600;
}

/* Nav Links */
.nav-links {
  display: flex;
  gap: 25px;
  list-style: none;
  align-items: center;
}
.nav-links a {
  text-decoration: none;
  color: #1e40af;
  font-weight: 600;
  transition: 0.3s;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
}
.nav-links a:hover {
  color: #2563eb;
  background: rgba(37, 99, 235, 0.1);
}
.nav-links a.active {
  background: #2563eb;
  color: white;
}
.logout-btn {
  background: #ef4444 !important;
  color: white !important;
}
.logout-btn:hover {
  background: #dc2626 !important;
}

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
  margin: 0 auto;
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
  box-sizing: border-box;
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
.auth-box button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Error and Success Messages */
.error-message {
  background: #fecaca;
  color: #991b1b;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
  border: 1px solid #fca5a5;
  font-weight: 600;
}
.success-message {
  background: #bbf7d0;
  color: #166534;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
  border: 1px solid #86efac;
  font-weight: 600;
}

/* App Views */
.app-views {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}
.view-content {
  width: 100%;
}

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
  .nav-bar h1 { font-size: 2rem; }
  .nav-user-section {
    width: 100%;
    justify-content: space-between;
  }
  .nav-links {
    gap: 15px;
    font-size: 0.9rem;
  }
  .nav-links a {
    padding: 6px 10px;
  }
  .auth-box { padding: 20px; }
  .auth-box input, .auth-box button { font-size: 0.95rem; }
}

/* Mobile */
@media (max-width: 480px) {
  .nav-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .nav-bar h1 {
    font-size: 1.8rem;
    text-align: center;
  }
  .nav-user-section {
    flex-direction: column;
    gap: 15px;
  }
  .user-info {
    width: 100%;
    justify-content: center;
  }
  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
  }
  .nav-links a {
    padding: 8px 12px;
    font-size: 0.85rem;
  }
  .auth-box input, .auth-box button { font-size: 0.9rem; padding: 10px; }
}
</style>
