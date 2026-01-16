<template>
  <div class="app-container">
    <NavBar />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
import { useUserStore } from "./stores/user";

export default defineComponent({
  name: "App",
  components: { RouterView, NavBar },
  setup() {
    const userStore = useUserStore();

    onMounted(() => {
      userStore.fetchUser();
    });

    return {};
  },
});
</script>

<style>
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --text-primary: #2d3748;
  --text-secondary: #718096;
  --bg-light: #f8f9fa;
  --card-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  --card-hover-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  min-height: 100vh;
  color: var(--text-primary);
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.card {
  background: white;
  border-radius: 16px;
  box-shadow: var(--card-shadow);
  border: none;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: var(--card-hover-shadow);
  transform: translateY(-2px);
}

.btn-primary {
  background: var(--primary-gradient);
  border: none;
  padding: 12px 28px;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
}

.btn-outline-primary {
  border: 2px solid var(--primary-color);
  color: var(--primary-color);
  padding: 10px 26px;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
  background: transparent;
}

.btn-outline-primary:hover {
  background: var(--primary-gradient);
  border-color: transparent;
  color: white;
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 2rem;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.alert {
  border-radius: 12px;
  border: none;
}
</style>
