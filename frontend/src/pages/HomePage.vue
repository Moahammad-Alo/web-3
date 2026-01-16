<template>
  <div class="home-page">
    <div class="hero-section text-center mb-5">
      <h1 class="page-title">🎯 Find Amazing Deals</h1>
      <p class="lead text-muted">Bid on unique items from sellers around the world</p>
      <SearchBar @search="handleSearch" />
    </div>

    <div v-if="itemsStore.loading" class="loading-spinner">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="itemsStore.error" class="alert alert-danger">
      {{ itemsStore.error }}
    </div>

    <div v-else>
      <!-- Show search results or all items -->
      <div v-if="itemsStore.isSearching" class="mb-4">
        <h4 class="text-muted">
          {{ itemsStore.searchResults.length }} results for "{{ itemsStore.searchQuery }}"
        </h4>
      </div>

      <div class="row g-4">
        <div 
          v-for="item in displayedItems" 
          :key="item.id" 
          class="col-12 col-md-6 col-lg-4 col-xl-3"
        >
          <ItemCard :item="item" />
        </div>
      </div>

      <div v-if="displayedItems.length === 0" class="text-center py-5">
        <div class="empty-state">
          <span class="empty-icon">📦</span>
          <h4>No items found</h4>
          <p class="text-muted">
            {{ itemsStore.isSearching ? 'Try a different search term' : 'Be the first to list an item!' }}
          </p>
          <router-link :to="{ name: 'CreateItem' }" class="btn btn-primary">
            ➕ Create Listing
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from "vue";
import { useItemsStore } from "@/stores/items";
import ItemCard from "@/components/ItemCard.vue";
import SearchBar from "@/components/SearchBar.vue";
import type { Item } from "@/types";

export default defineComponent({
  name: "HomePage",
  components: { ItemCard, SearchBar },
  setup() {
    const itemsStore = useItemsStore();

    onMounted(() => {
      itemsStore.fetchItems();
    });

    const displayedItems = computed((): Item[] => {
      if (itemsStore.isSearching) {
        return itemsStore.searchResults;
      }
      return itemsStore.items;
    });

    const handleSearch = (query: string): void => {
      if (!query) {
        itemsStore.fetchItems();
      }
    };

    return {
      itemsStore,
      displayedItems,
      handleSearch,
    };
  },
});
</script>

<style scoped>
.hero-section {
  padding: 2rem 0;
}

.lead {
  font-size: 1.2rem;
  max-width: 500px;
  margin: 0 auto 2rem;
}

.empty-state {
  padding: 3rem;
}

.empty-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
}
</style>
