<template>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container">
      <router-link class="navbar-brand" :to="{ name: 'Home' }">
        🎯 AuctionHub
      </router-link>
      
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Home' }">
              🏠 Browse
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'CreateItem' }">
              ➕ Sell Item
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'MyAuctions' }">
              📦 My Auctions
            </router-link>
          </li>
        </ul>
        
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a 
              class="nav-link dropdown-toggle user-dropdown" 
              href="#" 
              role="button" 
              data-bs-toggle="dropdown"
            >
              <img 
                v-if="userStore.profileImage" 
                :src="userStore.profileImage" 
                class="profile-img-sm"
                alt="Profile"
              />
              <span v-else class="profile-placeholder">👤</span>
              {{ userStore.username }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <router-link class="dropdown-item" :to="{ name: 'Profile' }">
                  ⚙️ Profile Settings
                </router-link>
              </li>
              <li><hr class="dropdown-divider" /></li>
              <li>
                <a class="dropdown-item" href="#" @click.prevent="handleLogout">
                  🚪 Logout
                </a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUserStore } from "@/stores/user";

export default defineComponent({
  name: "NavBar",
  setup() {
    const userStore = useUserStore();

    const handleLogout = (): void => {
      userStore.logout();
    };

    return {
      userStore,
      handleLogout,
    };
  },
});
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem 0;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.nav-link {
  font-weight: 500;
  padding: 0.5rem 1rem !important;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.15);
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.profile-img-sm {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.profile-placeholder {
  font-size: 1.2rem;
}

.dropdown-menu {
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border: none;
  padding: 0.5rem;
}

.dropdown-item {
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
</style>
