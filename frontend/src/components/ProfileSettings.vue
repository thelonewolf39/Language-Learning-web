<template>
  <div class="profile-settings">
    <button class="back-button" @click="$emit('back')">← Back</button>

    <div class="profile-header">
      <div class="avatar-section">
        <div class="avatar-large">
          <img v-if="user.avatar_style && user.avatar_seed"
               :src="`https://api.dicebear.com/7.x/${user.avatar_style}/svg?seed=${user.avatar_seed}`"
               :alt="user.username" />
          <div v-else class="identicon">{{ getIdenticon(user.username) }}</div>
        </div>
        <button @click="$emit('open-shop')" class="customize-btn">🎨 Customize Avatar</button>
      </div>

      <div class="user-info">
        <h1>{{ user.username }}</h1>
        <div class="stats-grid">
          <div class="stat-box">
            <span class="stat-value">💎 {{ user.total_points }}</span>
            <span class="stat-label">Points</span>
          </div>
          <div class="stat-box">
            <span class="stat-value">🏆 {{ achievementsCount }}</span>
            <span class="stat-label">Achievements</span>
          </div>
          <div class="stat-box">
            <span class="stat-value">📚 {{ lessonsCompleted }}</span>
            <span class="stat-label">Lessons Done</span>
          </div>
        </div>
      </div>
    </div>

    <!-- API Keys Section -->
    <div class="settings-section">
      <h2>🔑 Developer API Keys</h2>
      <p class="section-description">Create API keys to access your learning data from external applications.</p>

      <div class="api-keys-list">
        <div v-if="apiKeys.length === 0" class="empty-state">
          <p>No API keys yet. Create one to get started!</p>
        </div>

        <div v-for="key in apiKeys" :key="key.id" class="api-key-card">
          <div class="key-info">
            <div class="key-header">
              <h3>{{ key.name }}</h3>
              <span :class="['status-badge', key.is_active ? 'active' : 'inactive']">
                {{ key.is_active ? '✓ Active' : '✗ Revoked' }}
              </span>
            </div>
            <div class="key-details">
              <div class="key-value">
                <code>{{ key.key }}</code>
                <button @click="copyToClipboard(key.key)" class="copy-btn" title="Copy to clipboard">
                  📋
                </button>
              </div>
              <div class="key-meta">
                <span>Created: {{ formatDate(key.created_at) }}</span>
                <span v-if="key.last_used">Last used: {{ formatDate(key.last_used) }}</span>
              </div>
            </div>
          </div>
          <button
            v-if="key.is_active"
            @click="revokeKey(key.id)"
            class="revoke-btn"
            :disabled="revoking"
          >
            Revoke
          </button>
        </div>
      </div>

      <!-- Create New Key Form -->
      <div class="create-key-form">
        <h3>Create New API Key</h3>
        <div class="form-row">
          <input
            v-model="newKeyName"
            placeholder="Key name (e.g., 'My Mobile App')"
            maxlength="50"
            @keyup.enter="createApiKey"
          />
          <button @click="createApiKey" :disabled="!newKeyName || creating" class="create-btn">
            {{ creating ? 'Creating...' : 'Create Key' }}
          </button>
        </div>
      </div>

      <!-- API Documentation Link -->
      <div class="api-docs-box">
        <h3>📚 API Documentation</h3>
        <p>Learn how to use your API keys to build integrations.</p>
        <div class="docs-links">
          <a :href="`${apiUrl}/docs`" target="_blank" class="docs-link">
            Interactive API Docs
          </a>
          <a href="https://github.com/yourusername/language-learning-web/blob/main/API_DOCUMENTATION.md" target="_blank" class="docs-link">
            Full Documentation
          </a>
        </div>
      </div>
    </div>

    <!-- Notification -->
    <div v-if="notification" :class="['notification', notification.type]">
      {{ notification.message }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      required: true
    },
    authToken: {
      type: String,
      required: true
    },
    achievementsCount: {
      type: Number,
      default: 0
    },
    lessonsCompleted: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      apiKeys: [],
      newKeyName: '',
      creating: false,
      revoking: false,
      notification: null,
      apiUrl: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
    }
  },
  async mounted() {
    await this.loadApiKeys()
  },
  methods: {
    getIdenticon(username) {
      // Generate emoji-based identicon from username
      const emojis = ['😀', '😎', '🤓', '🥳', '🤩', '😇', '🥰', '😊', '🙂', '😋',
                      '🤗', '🥺', '😺', '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻',
                      '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐸', '🐵', '🦄', '🌟',
                      '⭐', '✨', '💫', '🔥', '💎', '🎨', '🎭', '🎪', '🎯', '🎲']

      let hash = 0
      for (let i = 0; i < username.length; i++) {
        hash = username.charCodeAt(i) + ((hash << 5) - hash)
      }
      return emojis[Math.abs(hash) % emojis.length]
    },
    async loadApiKeys() {
      try {
        const response = await fetch(`${this.apiUrl}/api/v1/api-keys`, {
          headers: {
            'Authorization': `Bearer ${this.authToken}`
          }
        })
        if (response.ok) {
          this.apiKeys = await response.json()
        }
      } catch (error) {
        console.error('Failed to load API keys:', error)
      }
    },
    async createApiKey() {
      if (!this.newKeyName) return

      this.creating = true
      try {
        const response = await fetch(`${this.apiUrl}/api/v1/api-keys`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.authToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: this.newKeyName })
        })

        if (response.ok) {
          const newKey = await response.json()
          this.apiKeys.push(newKey)
          this.newKeyName = ''
          this.showNotification(`✓ API key "${newKey.name}" created!`, 'success')
        } else {
          this.showNotification('Failed to create API key', 'error')
        }
      } catch (error) {
        this.showNotification('Failed to create API key', 'error')
      } finally {
        this.creating = false
      }
    },
    async revokeKey(keyId) {
      if (!confirm('Are you sure you want to revoke this API key? This cannot be undone.')) {
        return
      }

      this.revoking = true
      try {
        const response = await fetch(`${this.apiUrl}/api/v1/api-keys/${keyId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${this.authToken}`
          }
        })

        if (response.ok) {
          const key = this.apiKeys.find(k => k.id === keyId)
          if (key) {
            key.is_active = false
          }
          this.showNotification('✓ API key revoked', 'success')
        } else {
          this.showNotification('Failed to revoke API key', 'error')
        }
      } catch (error) {
        this.showNotification('Failed to revoke API key', 'error')
      } finally {
        this.revoking = false
      }
    },
    copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        this.showNotification('✓ API key copied to clipboard!', 'success')
      })
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    },
    showNotification(message, type) {
      this.notification = { message, type }
      setTimeout(() => {
        this.notification = null
      }, 3000)
    }
  }
}
</script>

<style scoped>
.profile-settings {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.back-button {
  background: none;
  border: none;
  color: #2563eb;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 20px;
  padding: 8px 0;
  transition: 0.2s;
}
.back-button:hover {
  color: #1d4ed8;
}

.profile-header {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.avatar-large {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.avatar-large img {
  width: 130px;
  height: 130px;
}

.identicon {
  font-size: 5rem;
}

.customize-btn {
  padding: 10px 20px;
  border: none;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
}

.customize-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.user-info {
  flex: 1;
}

.user-info h1 {
  color: #1e40af;
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.stat-box {
  background: #f3f4f6;
  padding: 15px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1e40af;
}

.stat-label {
  font-size: 0.9rem;
  color: #6b7280;
}

.settings-section {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.settings-section h2 {
  color: #1e40af;
  font-size: 2rem;
  margin-bottom: 10px;
}

.section-description {
  color: #6b7280;
  margin-bottom: 25px;
}

.api-keys-list {
  margin-bottom: 30px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #9ca3af;
  font-style: italic;
}

.api-key-card {
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
}

.key-info {
  flex: 1;
}

.key-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.key-header h3 {
  color: #1e40af;
  font-size: 1.2rem;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.inactive {
  background: #fee2e2;
  color: #991b1b;
}

.key-value {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.key-value code {
  background: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: #2563eb;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}

.copy-btn {
  background: #e5e7eb;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s;
  font-size: 1.2rem;
}

.copy-btn:hover {
  background: #d1d5db;
}

.key-meta {
  display: flex;
  gap: 20px;
  font-size: 0.85rem;
  color: #6b7280;
}

.revoke-btn {
  padding: 10px 20px;
  border: 2px solid #ef4444;
  background: white;
  color: #ef4444;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
}

.revoke-btn:hover {
  background: #ef4444;
  color: white;
}

.create-key-form {
  background: #f0f9ff;
  padding: 25px;
  border-radius: 12px;
  margin-bottom: 25px;
}

.create-key-form h3 {
  color: #1e40af;
  margin-bottom: 15px;
}

.form-row {
  display: flex;
  gap: 10px;
}

.form-row input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: 0.3s;
}

.form-row input:focus {
  outline: none;
  border-color: #2563eb;
}

.create-btn {
  padding: 12px 24px;
  border: none;
  background: linear-gradient(135deg, #2563eb, #1e40af);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
}

.create-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8, #1e3a8a);
  transform: scale(1.05);
}

.create-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.api-docs-box {
  background: #fffbeb;
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #fbbf24;
}

.api-docs-box h3 {
  color: #92400e;
  margin-bottom: 10px;
}

.api-docs-box p {
  color: #78350f;
  margin-bottom: 15px;
}

.docs-links {
  display: flex;
  gap: 10px;
}

.docs-link {
  padding: 10px 20px;
  background: white;
  color: #92400e;
  border: 2px solid #fbbf24;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: 0.3s;
}

.docs-link:hover {
  background: #fbbf24;
  color: white;
}

.notification {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 16px 24px;
  border-radius: 12px;
  font-weight: 600;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.3s ease;
  z-index: 1000;
}

.notification.success {
  background: #10b981;
  color: white;
}

.notification.error {
  background: #ef4444;
  color: white;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .api-key-card {
    flex-direction: column;
    align-items: stretch;
  }

  .form-row {
    flex-direction: column;
  }

  .docs-links {
    flex-direction: column;
  }
}
</style>
