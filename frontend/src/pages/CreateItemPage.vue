<template>
  <div class="create-item-page">
    <h1 class="page-title">➕ Create New Listing</h1>

    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card">
          <div class="card-body p-4">
            <form @submit.prevent="handleSubmit">
              <!-- Title -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Title *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="formData.title"
                  placeholder="What are you selling?"
                  required
                  maxlength="200"
                />
              </div>

              <!-- Description -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Description *</label>
                <textarea 
                  class="form-control" 
                  v-model="formData.description"
                  placeholder="Describe your item in detail..."
                  rows="5"
                  required
                ></textarea>
              </div>

              <!-- Starting Price -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Starting Price (£) *</label>
                <input 
                  type="number" 
                  class="form-control" 
                  v-model="formData.starting_price"
                  placeholder="0.00"
                  min="0.01"
                  step="0.01"
                  required
                />
              </div>

              <!-- End Date/Time -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Auction End Date & Time *</label>
                <input 
                  type="datetime-local" 
                  class="form-control" 
                  v-model="formData.end_datetime"
                  :min="minDateTime"
                  required
                />
                <small class="text-muted">Must be at least 1 hour in the future</small>
              </div>

              <!-- Image -->
              <div class="mb-4">
                <label class="form-label fw-semibold">Item Image *</label>
                <div class="image-upload-container">
                  <div v-if="previewImage" class="image-preview">
                    <img :src="previewImage" alt="Preview" />
                    <button 
                      type="button" 
                      class="btn btn-sm btn-danger remove-image"
                      @click="removeImage"
                    >
                      ✕
                    </button>
                  </div>
                  <label v-else class="upload-placeholder">
                    <span class="upload-icon">📷</span>
                    <span>Click to upload an image</span>
                    <input 
                      type="file" 
                      accept="image/*" 
                      @change="handleImageChange"
                      hidden
                      required
                    />
                  </label>
                </div>
              </div>

              <!-- Error Message -->
              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>

              <!-- Submit Button -->
              <button 
                type="submit" 
                class="btn btn-primary w-100 py-3"
                :disabled="submitting"
              >
                <span v-if="submitting">
                  <span class="spinner-border spinner-border-sm me-2"></span>
                  Creating...
                </span>
                <span v-else>🚀 Create Listing</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed } from "vue";
import { useRouter } from "vue-router";
import { useItemsStore } from "@/stores/items";
import type { CreateItemForm } from "@/types";

export default defineComponent({
  name: "CreateItemPage",
  setup() {
    const router = useRouter();
    const itemsStore = useItemsStore();

    const formData = reactive<CreateItemForm>({
      title: "",
      description: "",
      starting_price: "",
      end_datetime: "",
      image: null,
    });

    const previewImage = ref<string>("");
    const submitting = ref<boolean>(false);
    const errorMessage = ref<string>("");

    const minDateTime = computed((): string => {
      const now = new Date();
      now.setHours(now.getHours() + 1);
      return now.toISOString().slice(0, 16);
    });

    const handleImageChange = (event: Event): void => {
      const target = event.target as HTMLInputElement;
      const file = target.files?.[0];
      
      if (file) {
        formData.image = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          previewImage.value = e.target?.result as string;
        };
        reader.readAsDataURL(file);
      }
    };

    const removeImage = (): void => {
      formData.image = null;
      previewImage.value = "";
    };

    const handleSubmit = async (): Promise<void> => {
      submitting.value = true;
      errorMessage.value = "";

      try {
        const item = await itemsStore.createItem(formData);
        router.push({ name: "ItemDetail", params: { id: item.id } });
      } catch (err) {
        errorMessage.value = err instanceof Error ? err.message : "Failed to create listing";
      } finally {
        submitting.value = false;
      }
    };

    return {
      formData,
      previewImage,
      submitting,
      errorMessage,
      minDateTime,
      handleImageChange,
      removeImage,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.image-upload-container {
  border: 2px dashed #e9ecef;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.image-upload-container:hover {
  border-color: #667eea;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  cursor: pointer;
  color: #adb5bd;
  transition: all 0.3s ease;
}

.upload-placeholder:hover {
  color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.image-preview {
  position: relative;
  height: 300px;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #f8f9fa;
}

.remove-image {
  position: absolute;
  top: 10px;
  right: 10px;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  padding: 0;
}
</style>
