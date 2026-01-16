<template>
  <div class="my-auctions-page">
    <h1 class="page-title">📦 My Auctions</h1>

    <div v-if="itemsStore.loading" class="loading-spinner">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="itemsStore.error" class="alert alert-danger">
      {{ itemsStore.error }}
    </div>

    <div v-else>
      <div v-if="itemsStore.myItems.length === 0" class="text-center py-5">
        <div class="empty-state">
          <span class="empty-icon">📦</span>
          <h4>No auctions yet</h4>
          <p class="text-muted">Start selling by creating your first listing!</p>
          <router-link :to="{ name: 'CreateItem' }" class="btn btn-primary">
            ➕ Create Listing
          </router-link>
        </div>
      </div>

      <div v-else class="auctions-list">
        <div 
          v-for="item in itemsStore.myItems" 
          :key="item.id" 
          class="card auction-card mb-3"
        >
          <div class="row g-0">
            <div class="col-md-3">
              <div class="item-image-container">
                <img 
                  v-if="item.image" 
                  :src="item.image" 
                  :alt="item.title"
                  class="item-image"
                />
                <div v-else class="no-image">📷</div>
              </div>
            </div>
            <div class="col-md-9">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <h5 class="card-title">{{ item.title }}</h5>
                    <p class="card-text text-muted">{{ truncateDescription(item.description) }}</p>
                  </div>
                  <span class="badge" :class="item.is_active ? 'bg-success' : 'bg-secondary'">
                    {{ item.is_active ? '🔥 Active' : '⏰ Ended' }}
                  </span>
                </div>
                
                <div class="auction-stats mt-3">
                  <div class="stat">
                    <small class="text-muted">Current Price</small>
                    <span class="stat-value">£{{ item.current_price }}</span>
                  </div>
                  <div class="stat">
                    <small class="text-muted">Bids</small>
                    <span class="stat-value">{{ item.bid_count }}</span>
                  </div>
                  <div class="stat">
                    <small class="text-muted">{{ item.is_active ? 'Ends' : 'Ended' }}</small>
                    <span class="stat-value">{{ formatDate(item.end_datetime) }}</span>
                  </div>
                </div>

                <div class="mt-3">
                  <router-link 
                    :to="{ name: 'ItemDetail', params: { id: item.id } }"
                    class="btn btn-primary btn-sm me-2"
                  >
                    View Details
                  </router-link>
                  <button 
                    v-if="item.is_active"
                    class="btn btn-outline-danger btn-sm"
                    @click="handleDelete(item.id)"
                    :disabled="deleting === item.id"
                  >
                    {{ deleting === item.id ? 'Deleting...' : '🗑️ Delete' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useItemsStore } from "@/stores/items";

export default defineComponent({
  name: "MyAuctionsPage",
  setup() {
    const itemsStore = useItemsStore();
    const deleting = ref<number | null>(null);

    onMounted(() => {
      itemsStore.fetchMyItems();
    });

    const truncateDescription = (text: string): string => {
      if (text.length > 150) {
        return text.substring(0, 150) + "...";
      }
      return text;
    };

    const formatDate = (dateStr: string): string => {
      const date = new Date(dateStr);
      return date.toLocaleDateString();
    };

    const handleDelete = async (itemId: number): Promise<void> => {
      if (!confirm("Are you sure you want to delete this listing?")) {
        return;
      }
      
      deleting.value = itemId;
      try {
        await itemsStore.deleteItem(itemId);
      } catch (err) {
        console.error("Failed to delete item:", err);
      } finally {
        deleting.value = null;
      }
    };

    return {
      itemsStore,
      deleting,
      truncateDescription,
      formatDate,
      handleDelete,
    };
  },
});
</script>

<style scoped>
.empty-state {
  padding: 3rem;
}

.empty-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
}

.auction-card {
  overflow: hidden;
  transition: all 0.3s ease;
}

.auction-card:hover {
  transform: translateX(5px);
}

.item-image-container {
  height: 100%;
  min-height: 180px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  font-size: 3rem;
  color: #adb5bd;
}

.auction-stats {
  display: flex;
  gap: 2rem;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-weight: 600;
  color: #667eea;
}
</style>
