<template>
  <div class="item-detail-page">
    <div v-if="itemsStore.loading" class="loading-spinner">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="!item" class="alert alert-warning">
      Item not found
    </div>

    <div v-else class="row g-4">
      <!-- Main Item Info -->
      <div class="col-lg-8">
        <div class="card item-main-card">
          <div class="item-image-container">
            <img 
              v-if="item.image" 
              :src="item.image" 
              :alt="item.title" 
              class="item-image"
            />
            <div v-else class="no-image-large">
              <span>📷</span>
              <p>No image available</p>
            </div>
          </div>
          
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h1 class="item-title">{{ item.title }}</h1>
              <span class="badge" :class="item.is_active ? 'bg-success' : 'bg-secondary'">
                {{ item.is_active ? '🔥 Active' : '⏰ Ended' }}
              </span>
            </div>
            
            <p class="item-description">{{ item.description }}</p>
            
            <div class="seller-info">
              <small class="text-muted">Seller:</small>
              <span class="seller-name">{{ item.owner.username }}</span>
            </div>
          </div>
        </div>

        <!-- Questions Section -->
        <div class="card mt-4 questions-card">
          <div class="card-header">
            <h5 class="mb-0">💬 Questions & Answers</h5>
          </div>
          <div class="card-body">
            <!-- Ask Question Form -->
            <div v-if="item.is_active && !isOwner" class="mb-4">
              <form @submit.prevent="submitQuestion">
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Ask a question about this item..."
                    v-model="questionText"
                    required
                  />
                  <button class="btn btn-primary" type="submit" :disabled="itemsStore.loading">
                    Ask
                  </button>
                </div>
              </form>
            </div>

            <!-- Questions List -->
            <div v-if="item.questions && item.questions.length > 0">
              <div 
                v-for="question in item.questions" 
                :key="question.id" 
                class="question-item"
              >
                <div class="question-header">
                  <strong>{{ question.asker.username }}</strong>
                  <small class="text-muted">{{ formatDate(question.timestamp) }}</small>
                </div>
                <p class="question-text">{{ question.text }}</p>
                
                <!-- Answers -->
                <div v-if="question.answers.length > 0" class="answers-list">
                  <div 
                    v-for="answer in question.answers" 
                    :key="answer.id" 
                    class="answer-item"
                  >
                    <div class="answer-header">
                      <span class="seller-badge">Seller</span>
                      <strong>{{ answer.responder.username }}</strong>
                      <small class="text-muted">{{ formatDate(answer.timestamp) }}</small>
                    </div>
                    <p class="answer-text">{{ answer.text }}</p>
                  </div>
                </div>

                <!-- Answer Form (for owner) -->
                <div v-if="isOwner && !question.answers.length" class="mt-2">
                  <form @submit.prevent="submitAnswer(question.id)">
                    <div class="input-group input-group-sm">
                      <input
                        type="text"
                        class="form-control"
                        placeholder="Reply to this question..."
                        v-model="answerTexts[question.id]"
                        required
                      />
                      <button class="btn btn-outline-primary" type="submit">
                        Reply
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>

            <p v-else class="text-muted text-center py-3">
              No questions yet. Be the first to ask!
            </p>
          </div>
        </div>
      </div>

      <!-- Sidebar - Bidding -->
      <div class="col-lg-4">
        <div class="card bidding-card sticky-top">
          <div class="card-body">
            <div class="current-bid-section">
              <small class="text-muted">Current Bid</small>
              <div class="current-price">£{{ item.current_price }}</div>
              <small class="text-muted">{{ item.bid_count }} bids</small>
            </div>

            <div class="time-section my-4">
              <small class="text-muted d-block">
                {{ item.is_active ? 'Ends' : 'Ended' }}
              </small>
              <span class="end-time">{{ formatEndTime }}</span>
            </div>

            <!-- Bid Form -->
            <div v-if="item.is_active && !isOwner">
              <form @submit.prevent="submitBid">
                <div class="mb-3">
                  <label class="form-label">Your Bid (£)</label>
                  <input
                    type="number"
                    class="form-control form-control-lg"
                    v-model="bidAmount"
                    :min="minBid"
                    step="0.01"
                    required
                    :placeholder="`Min: £${minBid}`"
                  />
                </div>
                <button 
                  class="btn btn-primary w-100 py-3" 
                  type="submit"
                  :disabled="itemsStore.loading"
                >
                  🔨 Place Bid
                </button>
              </form>
              
              <div v-if="bidError" class="alert alert-danger mt-3">
                {{ bidError }}
              </div>
              <div v-if="bidSuccess" class="alert alert-success mt-3">
                Bid placed successfully!
              </div>
            </div>

            <div v-else-if="isOwner" class="alert alert-info">
              This is your listing
            </div>

            <div v-else class="alert alert-secondary">
              This auction has ended
            </div>

            <!-- Bid History -->
            <div v-if="item.bids && item.bids.length > 0" class="bid-history mt-4">
              <h6>Recent Bids</h6>
              <ul class="list-unstyled">
                <li 
                  v-for="bid in item.bids.slice(0, 5)" 
                  :key="bid.id" 
                  class="bid-item"
                >
                  <span class="bidder">{{ bid.bidder.username }}</span>
                  <span class="bid-amount">£{{ bid.amount }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref, onMounted, reactive } from "vue";
import { useRoute } from "vue-router";
import { useItemsStore } from "@/stores/items";
import { useUserStore } from "@/stores/user";
import type { ItemDetail } from "@/types";

export default defineComponent({
  name: "ItemDetailPage",
  setup() {
    const route = useRoute();
    const itemsStore = useItemsStore();
    const userStore = useUserStore();

    const bidAmount = ref<string>("");
    const bidError = ref<string>("");
    const bidSuccess = ref<boolean>(false);
    const questionText = ref<string>("");
    const answerTexts = reactive<Record<number, string>>({});

    const itemId = computed((): number => {
      return parseInt(route.params.id as string, 10);
    });

    const item = computed((): ItemDetail | null => {
      return itemsStore.currentItem;
    });

    const isOwner = computed((): boolean => {
      if (!item.value || !userStore.user) return false;
      return item.value.owner.id === userStore.user.id;
    });

    const minBid = computed((): string => {
      if (!item.value) return "0.01";
      return (parseFloat(item.value.current_price) + 0.01).toFixed(2);
    });

    const formatEndTime = computed((): string => {
      if (!item.value) return "";
      const endDate = new Date(item.value.end_datetime);
      return endDate.toLocaleString();
    });

    const formatDate = (dateStr: string): string => {
      const date = new Date(dateStr);
      return date.toLocaleDateString();
    };

    const submitBid = async (): Promise<void> => {
      bidError.value = "";
      bidSuccess.value = false;
      
      try {
        await itemsStore.placeBid(itemId.value, { amount: bidAmount.value });
        bidSuccess.value = true;
        bidAmount.value = "";
        setTimeout(() => { bidSuccess.value = false; }, 3000);
      } catch (err) {
        bidError.value = err instanceof Error ? err.message : "Failed to place bid";
      }
    };

    const submitQuestion = async (): Promise<void> => {
      if (!questionText.value.trim()) return;
      
      try {
        await itemsStore.askQuestion(itemId.value, { text: questionText.value });
        questionText.value = "";
      } catch (err) {
        console.error("Failed to ask question:", err);
      }
    };

    const submitAnswer = async (questionId: number): Promise<void> => {
      const text = answerTexts[questionId];
      if (!text?.trim()) return;
      
      try {
        await itemsStore.answerQuestion(questionId, { text });
        answerTexts[questionId] = "";
      } catch (err) {
        console.error("Failed to answer question:", err);
      }
    };

    onMounted(() => {
      itemsStore.fetchItem(itemId.value);
    });

    return {
      itemsStore,
      item,
      isOwner,
      minBid,
      formatEndTime,
      formatDate,
      bidAmount,
      bidError,
      bidSuccess,
      questionText,
      answerTexts,
      submitBid,
      submitQuestion,
      submitAnswer,
    };
  },
});
</script>

<style scoped>
.item-main-card {
  overflow: hidden;
}

.item-image-container {
  height: 400px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.no-image-large {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #adb5bd;
}

.no-image-large span {
  font-size: 4rem;
}

.item-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2d3748;
}

.item-description {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #4a5568;
}

.seller-info {
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.seller-name {
  font-weight: 600;
  margin-left: 0.5rem;
}

.bidding-card {
  top: 2rem;
}

.current-bid-section {
  text-align: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  border-radius: 12px;
}

.current-price {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
}

.time-section {
  text-align: center;
}

.end-time {
  font-size: 1.1rem;
  font-weight: 600;
}

.bid-history h6 {
  font-weight: 600;
  margin-bottom: 1rem;
}

.bid-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e9ecef;
}

.bid-amount {
  font-weight: 600;
  color: #667eea;
}

.question-item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.question-header {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.5rem;
}

.question-text {
  margin: 0;
}

.answers-list {
  margin-top: 1rem;
  padding-left: 1rem;
  border-left: 3px solid #667eea;
}

.answer-item {
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.answer-header {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.25rem;
}

.seller-badge {
  background: #667eea;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.answer-text {
  margin: 0;
}
</style>
