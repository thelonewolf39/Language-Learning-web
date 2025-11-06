<template>
  <div class="achievements-view">
    <div class="achievements-header">
      <h1>🏆 Achievements</h1>
      <div class="progress-bar-container">
        <div class="progress-info">
          <span>{{ earnedCount }} / {{ totalCount }} Unlocked</span>
          <span>{{ progressPercentage }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
      </div>
    </div>

    <div class="filter-tabs">
      <button
        v-for="category in categories"
        :key="category.value"
        @click="selectedCategory = category.value"
        :class="['filter-tab', { active: selectedCategory === category.value }]"
      >
        {{ category.label }}
      </button>
    </div>

    <div class="achievements-grid">
      <div
        v-for="achievement in filteredAchievements"
        :key="achievement.id"
        :class="['achievement-card', { earned: achievement.earned, locked: !achievement.earned }]"
      >
        <div class="achievement-icon">{{ achievement.icon }}</div>
        <div class="achievement-info">
          <h3>{{ achievement.name }}</h3>
          <p>{{ achievement.description }}</p>
          <div class="achievement-footer">
            <span class="points">💎 {{ achievement.points }} pts</span>
            <span v-if="achievement.earned" class="earned-badge">✓ Earned</span>
            <span v-else class="locked-badge">🔒 Locked</span>
          </div>
          <div v-if="achievement.earned && achievement.earned_at" class="earned-date">
            Earned: {{ formatDate(achievement.earned_at) }}
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredAchievements.length === 0" class="no-achievements">
      <p>No achievements in this category yet.</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    authToken: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      allAchievements: [],
      userAchievements: [],
      selectedCategory: 'all',
      categories: [
        { label: 'All', value: 'all' },
        { label: 'Lessons', value: 'lessons' },
        { label: 'Scores', value: 'scores' },
        { label: 'Streak', value: 'streak' },
        { label: 'Points', value: 'points' }
      ],
      apiUrl: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
    }
  },
  computed: {
    filteredAchievements() {
      if (this.selectedCategory === 'all') {
        return this.allAchievements
      }
      return this.allAchievements.filter(a => a.category === this.selectedCategory)
    },
    earnedCount() {
      return this.allAchievements.filter(a => a.earned).length
    },
    totalCount() {
      return this.allAchievements.length
    },
    progressPercentage() {
      if (this.totalCount === 0) return 0
      return Math.round((this.earnedCount / this.totalCount) * 100)
    }
  },
  async mounted() {
    await this.loadAchievements()
  },
  methods: {
    async loadAchievements() {
      try {
        // Load all available achievements
        const allResponse = await fetch(`${this.apiUrl}/api/v1/achievements`)
        const allData = await allResponse.json()

        // Load user's earned achievements using session token
        let earnedIds = new Set()
        try {
          const userResponse = await fetch(`${this.apiUrl}/api/v1/achievements/me`, {
            headers: {
              'Authorization': `Bearer ${this.authToken}`
            }
          })
          if (userResponse.ok) {
            const userData = await userResponse.json()
            earnedIds = new Set(userData.map(a => a.id))
            this.userAchievements = userData
          }
        } catch (err) {
          console.log('Could not load user achievements:', err)
        }

        // Combine data
        this.allAchievements = allData.map(achievement => ({
          ...achievement,
          earned: earnedIds.has(achievement.id),
          earned_at: this.userAchievements.find(ua => ua.id === achievement.id)?.earned_at
        }))
      } catch (error) {
        console.error('Failed to load achievements:', error)
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    }
  }
}
</script>

<style scoped>
.achievements-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.achievements-header {
  text-align: center;
  margin-bottom: 30px;
}

.achievements-header h1 {
  font-size: 2.5rem;
  color: #1e40af;
  margin-bottom: 20px;
}

.progress-bar-container {
  max-width: 600px;
  margin: 0 auto;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
}

.progress-bar {
  height: 20px;
  background: #e5e7eb;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #10b981, #059669);
  transition: width 0.5s ease;
  border-radius: 10px;
}

.filter-tabs {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.filter-tab {
  padding: 10px 20px;
  border: none;
  background: #e5e7eb;
  color: #374151;
  font-weight: 600;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-tab:hover {
  background: #d1d5db;
}

.filter-tab.active {
  background: #2563eb;
  color: white;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.achievement-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  border: 3px solid transparent;
  display: flex;
  gap: 15px;
}

.achievement-card.earned {
  border-color: #10b981;
}

.achievement-card.locked {
  opacity: 0.6;
}

.achievement-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.achievement-icon {
  font-size: 3rem;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.achievement-info {
  flex: 1;
}

.achievement-info h3 {
  color: #1e40af;
  font-size: 1.3rem;
  margin-bottom: 8px;
}

.achievement-info p {
  color: #6b7280;
  margin-bottom: 12px;
  line-height: 1.4;
}

.achievement-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.points {
  color: #f59e0b;
  font-weight: bold;
  font-size: 1.1rem;
}

.earned-badge {
  background: #10b981;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.locked-badge {
  background: #9ca3af;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.earned-date {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 8px;
  font-style: italic;
}

.no-achievements {
  text-align: center;
  padding: 60px 20px;
  color: #6b7280;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .achievements-header h1 {
    font-size: 2rem;
  }

  .achievements-grid {
    grid-template-columns: 1fr;
  }

  .achievement-card {
    flex-direction: column;
    text-align: center;
  }

  .achievement-icon {
    font-size: 2.5rem;
  }

  .achievement-footer {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
