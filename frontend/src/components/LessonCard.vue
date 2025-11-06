<template>
  <div class="lesson-card" @click="$emit('click')">
    <h3>{{ lesson.title }}</h3>
    <p>{{ lesson.description }}</p>
    <button>Start Lesson</button>
  </div>
</template>

<script>
export default {
  props: { lesson: Object }
}
</script>

<style scoped>
.lesson-card {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}
.lesson-card:hover {
  transform: translateY(-5px);
  box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
}
.lesson-card h3 { margin-bottom: 10px; color: #1e40af; }
.lesson-card p { color: #4b5563; margin-bottom: 15px; }
.lesson-card button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background-color: #2563eb;
  color: white;
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
  transition: 0.3s;
}
.lesson-card button:hover { background-color: #1d4ed8; }

/* Mobile tweaks */
@media (max-width: 480px) {
  .lesson-card h3 { font-size: 1.2rem; }
  .lesson-card p { font-size: 0.9rem; }
  .lesson-card button { font-size: 0.9rem; padding: 10px; }
}
</style>
