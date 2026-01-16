<template>
  <div class="search-bar-container">
    <div class="search-wrapper">
      <span class="search-icon">🔍</span>
      <input
        type="text"
        class="form-control search-input"
        placeholder="Search for items..."
        v-model="searchQuery"
        @input="handleSearch"
      />
      <button 
        v-if="searchQuery" 
        class="clear-btn" 
        @click="clearSearch"
        type="button"
      >
        ✕
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useItemsStore } from "@/stores/items";

export default defineComponent({
  name: "SearchBar",
  emits: ["search"],
  setup(_, { emit }) {
    const itemsStore = useItemsStore();
    const searchQuery = ref<string>("");
    let debounceTimer: ReturnType<typeof setTimeout> | null = null;

    const handleSearch = (): void => {
      // Debounce search to avoid too many API calls
      if (debounceTimer) {
        clearTimeout(debounceTimer);
      }
      
      debounceTimer = setTimeout(() => {
        itemsStore.searchItems(searchQuery.value);
        emit("search", searchQuery.value);
      }, 300);
    };

    const clearSearch = (): void => {
      searchQuery.value = "";
      itemsStore.clearSearch();
      emit("search", "");
    };

    return {
      searchQuery,
      handleSearch,
      clearSearch,
    };
  },
});
</script>

<style scoped>
.search-bar-container {
  margin-bottom: 2rem;
}

.search-wrapper {
  position: relative;
  max-width: 500px;
  margin: 0 auto;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  z-index: 1;
}

.search-input {
  padding: 1rem 3rem;
  border-radius: 50px;
  border: 2px solid #e9ecef;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.search-input:focus {
  border-color: #667eea;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
}

.clear-btn {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1rem;
  color: #adb5bd;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: #f8f9fa;
  color: #667eea;
}
</style>
