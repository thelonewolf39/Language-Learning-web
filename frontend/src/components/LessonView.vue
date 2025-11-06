<template>
  <div class="lesson-view">
    <button class="back-button" @click="$emit('back')">← Back to Lessons</button>

    <div class="lesson-header">
      <h1>{{ lesson.title }}</h1>
      <p class="description">{{ lesson.description }}</p>
      <span class="difficulty-badge">{{ lesson.difficulty }}</span>
    </div>

    <!-- Tab Navigation -->
    <div class="tabs">
      <button
        :class="['tab', { active: activeTab === 'vocabulary' }]"
        @click="activeTab = 'vocabulary'"
      >
        Vocabulary
      </button>
      <button
        :class="['tab', { active: activeTab === 'practice' }]"
        @click="activeTab = 'practice'"
      >
        Practice Quiz
      </button>
    </div>

    <!-- Vocabulary Section -->
    <div v-if="activeTab === 'vocabulary'" class="vocabulary-section">
      <div v-for="(word, index) in lesson.vocabulary" :key="index" class="vocab-card">
        <div class="vocab-spanish">{{ word.spanish }}</div>
        <div class="vocab-pronunciation">{{ word.pronunciation }}</div>
        <div class="vocab-english">{{ word.english }}</div>
      </div>
    </div>

    <!-- Practice Quiz Section -->
    <div v-if="activeTab === 'practice'" class="quiz-section">
      <div v-if="!quizCompleted" class="quiz-container">
        <div class="quiz-progress">
          Question {{ currentQuestionIndex + 1 }} of {{ lesson.exercises.length }}
        </div>

        <div class="question-card">
          <h3>{{ currentQuestion.question }}</h3>

          <div class="options">
            <button
              v-for="(option, index) in currentQuestion.options"
              :key="index"
              @click="selectAnswer(option)"
              :class="[
                'option-button',
                {
                  correct: selectedAnswer === option && option === currentQuestion.answer,
                  incorrect: selectedAnswer === option && option !== currentQuestion.answer,
                  disabled: selectedAnswer !== null
                }
              ]"
              :disabled="selectedAnswer !== null"
            >
              {{ option }}
            </button>
          </div>

          <div v-if="selectedAnswer" class="feedback">
            <p v-if="selectedAnswer === currentQuestion.answer" class="correct-feedback">
              ✓ Correct! Great job!
            </p>
            <p v-else class="incorrect-feedback">
              ✗ Incorrect. The correct answer is: {{ currentQuestion.answer }}
            </p>
          </div>

          <button
            v-if="selectedAnswer"
            @click="nextQuestion"
            class="next-button"
          >
            {{ currentQuestionIndex < lesson.exercises.length - 1 ? 'Next Question' : 'Finish Quiz' }}
          </button>
        </div>
      </div>

      <!-- Quiz Results -->
      <div v-else class="quiz-results">
        <h2>Quiz Complete!</h2>
        <div class="score">
          <div class="score-circle">
            <span class="score-text">{{ score }}/{{ lesson.exercises.length }}</span>
          </div>
          <p class="score-percentage">{{ scorePercentage }}%</p>
        </div>
        <p class="score-message">{{ scoreMessage }}</p>
        <div class="result-buttons">
          <button @click="retakeQuiz" class="retry-button">Retake Quiz</button>
          <button @click="$emit('back')" class="done-button">Back to Lessons</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    lesson: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      activeTab: 'vocabulary',
      currentQuestionIndex: 0,
      selectedAnswer: null,
      score: 0,
      quizCompleted: false,
      answers: []
    }
  },
  computed: {
    currentQuestion() {
      return this.lesson.exercises[this.currentQuestionIndex]
    },
    scorePercentage() {
      return Math.round((this.score / this.lesson.exercises.length) * 100)
    },
    scoreMessage() {
      const percentage = this.scorePercentage
      if (percentage === 100) return 'Perfect! You mastered this lesson!'
      if (percentage >= 80) return 'Excellent work! Keep it up!'
      if (percentage >= 60) return 'Good job! Practice makes perfect.'
      return 'Keep practicing! You\'ll get better.'
    }
  },
  methods: {
    selectAnswer(answer) {
      this.selectedAnswer = answer
      if (answer === this.currentQuestion.answer) {
        this.score++
      }
      this.answers.push({
        question: this.currentQuestion.question,
        selected: answer,
        correct: this.currentQuestion.answer,
        isCorrect: answer === this.currentQuestion.answer
      })
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.lesson.exercises.length - 1) {
        this.currentQuestionIndex++
        this.selectedAnswer = null
      } else {
        this.quizCompleted = true
      }
    },
    retakeQuiz() {
      this.currentQuestionIndex = 0
      this.selectedAnswer = null
      this.score = 0
      this.quizCompleted = false
      this.answers = []
    }
  }
}
</script>

<style scoped>
.lesson-view {
  max-width: 900px;
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

.lesson-header {
  text-align: center;
  margin-bottom: 30px;
}
.lesson-header h1 {
  color: #1e40af;
  font-size: 2.5rem;
  margin-bottom: 10px;
}
.description {
  color: #4b5563;
  font-size: 1.1rem;
  margin-bottom: 10px;
}
.difficulty-badge {
  display: inline-block;
  background: linear-gradient(to right, #10b981, #059669);
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: capitalize;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-bottom: 2px solid #e5e7eb;
}
.tab {
  flex: 1;
  padding: 15px;
  border: none;
  background: none;
  color: #6b7280;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
  border-bottom: 3px solid transparent;
}
.tab:hover {
  color: #2563eb;
}
.tab.active {
  color: #2563eb;
  border-bottom-color: #2563eb;
}

/* Vocabulary Section */
.vocabulary-section {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}
.vocab-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s;
}
.vocab-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}
.vocab-spanish {
  font-size: 2rem;
  font-weight: bold;
  color: #1e40af;
  margin-bottom: 8px;
}
.vocab-pronunciation {
  font-size: 0.9rem;
  color: #6b7280;
  font-style: italic;
  margin-bottom: 12px;
}
.vocab-english {
  font-size: 1.2rem;
  color: #4b5563;
}

/* Quiz Section */
.quiz-section {
  min-height: 400px;
}
.quiz-container {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.quiz-progress {
  text-align: center;
  color: #6b7280;
  font-size: 0.9rem;
  margin-bottom: 20px;
  font-weight: 600;
}
.question-card h3 {
  color: #1e40af;
  font-size: 1.5rem;
  margin-bottom: 30px;
  text-align: center;
}
.options {
  display: grid;
  gap: 15px;
  margin-bottom: 20px;
}
.option-button {
  padding: 15px 20px;
  border: 2px solid #e5e7eb;
  background: white;
  color: #374151;
  font-size: 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
  text-align: left;
}
.option-button:hover:not(.disabled) {
  border-color: #2563eb;
  background: #eff6ff;
}
.option-button.correct {
  border-color: #10b981;
  background: #d1fae5;
  color: #065f46;
}
.option-button.incorrect {
  border-color: #ef4444;
  background: #fee2e2;
  color: #991b1b;
}
.option-button.disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
.feedback {
  margin: 20px 0;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  font-weight: 600;
}
.correct-feedback {
  background: #d1fae5;
  color: #065f46;
}
.incorrect-feedback {
  background: #fee2e2;
  color: #991b1b;
}
.next-button {
  width: 100%;
  padding: 15px;
  border: none;
  background: linear-gradient(to right, #2563eb, #1e40af);
  color: white;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}
.next-button:hover {
  background: linear-gradient(to right, #1d4ed8, #1e3a8a);
}

/* Quiz Results */
.quiz-results {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}
.quiz-results h2 {
  color: #1e40af;
  font-size: 2rem;
  margin-bottom: 30px;
}
.score {
  margin: 30px 0;
}
.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #1e40af);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
}
.score-text {
  color: white;
  font-size: 2.5rem;
  font-weight: bold;
}
.score-percentage {
  font-size: 1.5rem;
  color: #1e40af;
  font-weight: bold;
}
.score-message {
  font-size: 1.2rem;
  color: #4b5563;
  margin: 20px 0;
}
.result-buttons {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}
.retry-button, .done-button {
  flex: 1;
  padding: 15px;
  border: none;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}
.retry-button {
  background: #e5e7eb;
  color: #374151;
}
.retry-button:hover {
  background: #d1d5db;
}
.done-button {
  background: linear-gradient(to right, #2563eb, #1e40af);
  color: white;
}
.done-button:hover {
  background: linear-gradient(to right, #1d4ed8, #1e3a8a);
}

/* Responsive */
@media (max-width: 768px) {
  .lesson-header h1 {
    font-size: 2rem;
  }
  .vocab-spanish {
    font-size: 1.5rem;
  }
  .vocabulary-section {
    grid-template-columns: 1fr;
  }
  .result-buttons {
    flex-direction: column;
  }
}
</style>
