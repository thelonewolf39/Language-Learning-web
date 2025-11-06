<template>
  <div class="avatar-shop">
    <button class="back-button" @click="$emit('back')">← Back</button>

    <div class="shop-header">
      <h1>🎨 Avatar Shop</h1>
      <div class="points-display">
        <span class="points-icon">💎</span>
        <span class="points-text">{{ userPoints }} Points</span>
      </div>
    </div>

    <p class="shop-subtitle">Unlock custom avatar styles with your earned points!</p>

    <!-- Avatar Styles Grid -->
    <div class="avatars-grid">
      <div
        v-for="style in avatarStyles"
        :key="style.id"
        :class="['avatar-card', { owned: style.is_owned, locked: !style.is_owned }]"
      >
        <div class="avatar-preview">
          <img :src="style.preview_url" :alt="style.name" />
          <div v-if="style.is_premium" class="premium-badge">⭐ PREMIUM</div>
        </div>

        <div class="avatar-info">
          <h3>{{ style.name }}</h3>
          <p>{{ style.description }}</p>

          <div class="avatar-footer">
            <div class="cost">
              <span v-if="style.cost === 0" class="free-badge">FREE</span>
              <span v-else class="points-cost">💎 {{ style.cost }} pts</span>
            </div>

            <button
              v-if="!style.is_owned && style.cost > 0"
              @click="purchaseStyle(style)"
              :disabled="userPoints < style.cost || purchasing"
              :class="['purchase-btn', { disabled: userPoints < style.cost }]"
            >
              {{ userPoints < style.cost ? 'Not Enough Points' : 'Purchase' }}
            </button>

            <button
              v-if="style.is_owned"
              @click="selectStyle(style)"
              :class="['use-btn', { active: currentStyle === style.style_type }]"
            >
              {{ currentStyle === style.style_type ? '✓ Using' : 'Use This' }}
            </button>
          </div>
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
    userPoints: {
      type: Number,
      default: 0
    },
    currentStyle: {
      type: String,
      default: 'avataaars'
    },
    authToken: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      avatarStyles: [],
      purchasing: false,
      notification: null,
      apiUrl: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
    }
  },
  async mounted() {
    await this.loadAvatarStyles()
  },
  methods: {
    async loadAvatarStyles() {
      try {
        const response = await fetch(`${this.apiUrl}/api/v1/avatar-styles`, {
          headers: {
            'Authorization': `Bearer ${this.authToken}`
          }
        })
        this.avatarStyles = await response.json()
      } catch (error) {
        console.error('Failed to load avatar styles:', error)
      }
    },
    async purchaseStyle(style) {
      this.purchasing = true
      try {
        const response = await fetch(`${this.apiUrl}/api/v1/avatar-styles/purchase`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.authToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ avatar_style_id: style.id })
        })

        if (response.ok) {
          const data = await response.json()
          this.showNotification(`✓ Purchased ${style.name}!`, 'success')
          this.$emit('points-updated', data.remaining_points)
          await this.loadAvatarStyles()
        } else {
          const error = await response.json()
          this.showNotification(error.detail || 'Purchase failed', 'error')
        }
      } catch (error) {
        this.showNotification('Purchase failed', 'error')
      } finally {
        this.purchasing = false
      }
    },
    async selectStyle(style) {
      try {
        // Generate random seed for customization
        const seed = Math.random().toString(36).substring(7)

        const response = await fetch(`${this.apiUrl}/api/v1/users/avatar`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${this.authToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            avatar_style: style.style_type,
            avatar_seed: seed
          })
        })

        if (response.ok) {
          this.showNotification(`✓ Now using ${style.name}!`, 'success')
          this.$emit('avatar-changed', { style: style.style_type, seed })
        }
      } catch (error) {
        this.showNotification('Failed to update avatar', 'error')
      }
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
.avatar-shop {
  max-width: 1200px;
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

.shop-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.shop-header h1 {
  font-size: 2.5rem;
  color: #1e40af;
}

.points-display {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: white;
  padding: 12px 24px;
  border-radius: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  font-size: 1.2rem;
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
}

.points-icon {
  font-size: 1.5rem;
}

.shop-subtitle {
  color: #6b7280;
  font-size: 1.1rem;
  margin-bottom: 30px;
  text-align: center;
}

.avatars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 60px;
}

.avatar-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  border: 3px solid transparent;
}

.avatar-card.owned {
  border-color: #10b981;
}

.avatar-card.locked:not(.owned) {
  opacity: 0.8;
}

.avatar-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.avatar-preview {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto 15px;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.avatar-preview img {
  width: 120px;
  height: 120px;
}

.premium-badge {
  position: absolute;
  top: 5px;
  right: 5px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: white;
  font-size: 0.7rem;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: bold;
}

.avatar-info {
  text-align: center;
}

.avatar-info h3 {
  color: #1e40af;
  font-size: 1.3rem;
  margin-bottom: 8px;
}

.avatar-info p {
  color: #6b7280;
  margin-bottom: 15px;
  min-height: 40px;
}

.avatar-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  gap: 10px;
}

.cost {
  font-weight: bold;
}

.free-badge {
  background: #10b981;
  color: white;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
}

.points-cost {
  color: #f59e0b;
  font-size: 1.1rem;
}

.purchase-btn,
.use-btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.purchase-btn {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  color: white;
}

.purchase-btn:hover:not(.disabled) {
  background: linear-gradient(135deg, #1d4ed8, #1e3a8a);
  transform: scale(1.05);
}

.purchase-btn.disabled {
  background: #9ca3af;
  cursor: not-allowed;
  opacity: 0.6;
}

.use-btn {
  background: #e5e7eb;
  color: #374151;
}

.use-btn:hover {
  background: #d1d5db;
}

.use-btn.active {
  background: #10b981;
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
  .shop-header {
    flex-direction: column;
    gap: 15px;
  }

  .avatars-grid {
    grid-template-columns: 1fr;
  }

  .avatar-footer {
    flex-direction: column;
  }

  .purchase-btn,
  .use-btn {
    width: 100%;
  }
}
</style>
