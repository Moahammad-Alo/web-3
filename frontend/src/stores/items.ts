/**
 * Pinia store for auction items state.
 */

import { defineStore } from 'pinia';
import type { 
  Item, 
  ItemDetail, 
  ItemsResponse, 
  Bid, 
  Question,
  CreateItemForm,
  PlaceBidForm,
  QuestionForm 
} from '@/types';
import { get, post, del } from '@/services/api';

interface ItemsState {
  items: Item[];
  currentItem: ItemDetail | null;
  searchResults: Item[];
  myItems: Item[];
  loading: boolean;
  error: string | null;
  searchQuery: string;
}

export const useItemsStore = defineStore('items', {
  state: (): ItemsState => ({
    items: [],
    currentItem: null,
    searchResults: [],
    myItems: [],
    loading: false,
    error: null,
    searchQuery: '',
  }),

  getters: {
    activeItems: (state): Item[] => state.items.filter(item => item.is_active),
    hasItems: (state): boolean => state.items.length > 0,
    isSearching: (state): boolean => state.searchQuery.length > 0,
  },

  actions: {
    /**
     * Fetch all active auction items.
     */
    async fetchItems(): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        const response = await get<ItemsResponse>('/api/items/');
        this.items = response.items;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to fetch items';
      } finally {
        this.loading = false;
      }
    },

    /**
     * Search items by keyword.
     */
    async searchItems(query: string): Promise<void> {
      this.searchQuery = query;
      if (!query.trim()) {
        this.searchResults = [];
        return;
      }
      
      this.loading = true;
      this.error = null;
      try {
        const response = await get<ItemsResponse>(`/api/items/?q=${encodeURIComponent(query)}`);
        this.searchResults = response.items;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to search items';
      } finally {
        this.loading = false;
      }
    },

    /**
     * Fetch user's own auction items.
     */
    async fetchMyItems(): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        const response = await get<ItemsResponse>('/api/items/?my=true&all=true');
        this.myItems = response.items;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to fetch your items';
      } finally {
        this.loading = false;
      }
    },

    /**
     * Fetch a single item by ID.
     */
    async fetchItem(itemId: number): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        this.currentItem = await get<ItemDetail>(`/api/items/${itemId}/`);
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to fetch item';
      } finally {
        this.loading = false;
      }
    },

    /**
     * Create a new auction item.
     */
    async createItem(data: CreateItemForm): Promise<Item> {
      this.loading = true;
      this.error = null;
      try {
        const formData = new FormData();
        formData.append('title', data.title);
        formData.append('description', data.description);
        formData.append('starting_price', data.starting_price);
        formData.append('end_datetime', data.end_datetime);
        if (data.image) {
          formData.append('image', data.image);
        }
        
        const item = await post<Item>('/api/items/', formData);
        this.items.unshift(item);
        return item;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to create item';
        throw err;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Delete an item.
     */
    async deleteItem(itemId: number): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        await del<{ success: boolean }>(`/api/items/${itemId}/`);
        this.items = this.items.filter(item => item.id !== itemId);
        this.myItems = this.myItems.filter(item => item.id !== itemId);
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to delete item';
        throw err;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Place a bid on an item.
     */
    async placeBid(itemId: number, data: PlaceBidForm): Promise<Bid> {
      this.loading = true;
      this.error = null;
      try {
        const bid = await post<Bid>(`/api/items/${itemId}/bids/`, data);
        // Refresh the item to get updated price
        await this.fetchItem(itemId);
        return bid;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to place bid';
        throw err;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Ask a question about an item.
     */
    async askQuestion(itemId: number, data: QuestionForm): Promise<Question> {
      this.loading = true;
      this.error = null;
      try {
        const question = await post<Question>(`/api/items/${itemId}/questions/`, data);
        // Refresh the item to get updated questions
        await this.fetchItem(itemId);
        return question;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to ask question';
        throw err;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Answer a question.
     */
    async answerQuestion(questionId: number, data: QuestionForm): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        await post<Question>(`/api/questions/${questionId}/answers/`, data);
        // Refresh the current item to get updated answers
        if (this.currentItem) {
          await this.fetchItem(this.currentItem.id);
        }
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to answer question';
        throw err;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Clear the current item.
     */
    clearCurrentItem(): void {
      this.currentItem = null;
    },

    /**
     * Clear search results.
     */
    clearSearch(): void {
      this.searchQuery = '';
      this.searchResults = [];
    },

    /**
     * Clear any error messages.
     */
    clearError(): void {
      this.error = null;
    },
  },
});
