<template>
  <div class="item-card card h-100">
    <div class="card-img-wrapper">
      <img 
        v-if="item.image" 
        :src="item.image" 
        class="card-img-top" 
        :alt="item.title"
      />
      <div v-else class="no-image">
        <span>📷</span>
        <small>No Image</small>
      </div>
      <div class="status-badge" :class="{ 'ended': !item.is_active }">
        {{ item.is_active ? '🔥 Active' : '⏰ Ended' }}
      </div>
    </div>
    
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">{{ item.title }}</h5>
      <p class="card-text text-muted description">{{ truncatedDescription }}</p>
      
      <div class="price-section mt-auto">
        <div class="current-price">
          <small class="text-muted">Current Bid</small>
          <span class="price">£{{ item.current_price }}</span>
        </div>
        <div class="bid-count">
          <span class="badge bg-primary">{{ item.bid_count }} bids</span>
        </div>
      </div>
      
      <div class="time-remaining mt-2">
        <small class="text-muted">
          {{ item.is_active ? `Ends ${formatTimeRemaining}` : 'Auction ended' }}
        </small>
      </div>
      
      <router-link 
        :to="{ name: 'ItemDetail', params: { id: item.id } }" 
        class="btn btn-primary mt-3"
      >
        View Details
      </router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import type { PropType } from "vue";
import type { Item } from "@/types";

export default defineComponent({
  name: "ItemCard",
  props: {
    item: {
      type: Object as PropType<Item>,
      required: true,
    },
  },
  setup(props) {
    const truncatedDescription = computed((): string => {
      if (props.item.description.length > 100) {
        return props.item.description.substring(0, 100) + "...";
      }
      return props.item.description;
    });

    const formatTimeRemaining = computed((): string => {
      const endDate = new Date(props.item.end_datetime);
      const now = new Date();
      const diff = endDate.getTime() - now.getTime();

      if (diff <= 0) return "ended";

      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

      if (days > 0) return `in ${days}d ${hours}h`;
      if (hours > 0) return `in ${hours}h ${minutes}m`;
      return `in ${minutes}m`;
    });

    return {
      truncatedDescription,
      formatTimeRemaining,
    };
  },
});
</script>

<style scoped>
.item-card {
  overflow: hidden;
  transition: all 0.3s ease;
}

.item-card:hover {
  transform: translateY(-8px);
}

.card-img-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #adb5bd;
}

.no-image span {
  font-size: 3rem;
}

.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(40, 167, 69, 0.9);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge.ended {
  background: rgba(108, 117, 125, 0.9);
}

.card-body {
  padding: 1.25rem;
}

.card-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2d3748;
}

.description {
  font-size: 0.9rem;
  line-height: 1.5;
}

.price-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.current-price {
  display: flex;
  flex-direction: column;
}

.price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
}

.time-remaining {
  font-size: 0.85rem;
}
</style>
