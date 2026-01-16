<template>
  <div class="profile-page">
    <h1 class="page-title">⚙️ Profile Settings</h1>

    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card profile-card">
          <div class="card-body p-4">
            <div v-if="userStore.loading" class="loading-spinner">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <form v-else @submit.prevent="handleSubmit">
              <!-- Profile Image -->
              <div class="profile-image-section text-center mb-4">
                <div class="profile-image-container">
                  <img 
                    v-if="previewImage || userStore.profileImage" 
                    :src="previewImage || userStore.profileImage || ''" 
                    class="profile-image"
                    alt="Profile"
                  />
                  <div v-else class="profile-placeholder-large">
                    <span>👤</span>
                  </div>
                </div>
                <label class="btn btn-outline-primary mt-3">
                  📷 Change Photo
                  <input 
                    type="file" 
                    accept="image/*" 
                    @change="handleImageChange"
                    hidden
                  />
                </label>
              </div>

              <!-- Username (read-only) -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Username</label>
                <input 
                  type="text" 
                  class="form-control" 
                  :value="userStore.username"
                  disabled
                />
                <small class="text-muted">Username cannot be changed</small>
              </div>

              <!-- Email -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Email Address</label>
                <input 
                  type="email" 
                  class="form-control" 
                  v-model="formData.email"
                  required
                />
              </div>

              <!-- Date of Birth -->
              <div class="mb-4">
                <label class="form-label fw-semibold">Date of Birth</label>
                <input 
                  type="date" 
                  class="form-control" 
                  v-model="formData.date_of_birth"
                />
              </div>

              <!-- Success/Error Messages -->
              <div v-if="successMessage" class="alert alert-success">
                {{ successMessage }}
              </div>
              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>

              <!-- Submit Button -->
              <button 
                type="submit" 
                class="btn btn-primary w-100 py-3"
                :disabled="saving"
              >
                <span v-if="saving">
                  <span class="spinner-border spinner-border-sm me-2"></span>
                  Saving...
                </span>
                <span v-else>💾 Save Changes</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import type { UpdateProfileForm } from "@/types";

export default defineComponent({
  name: "ProfilePage",
  setup() {
    const userStore = useUserStore();

    const formData = reactive<UpdateProfileForm>({
      email: "",
      date_of_birth: "",
    });

    const selectedImage = ref<File | null>(null);
    const previewImage = ref<string>("");
    const saving = ref<boolean>(false);
    const successMessage = ref<string>("");
    const errorMessage = ref<string>("");

    onMounted(() => {
      if (userStore.user) {
        formData.email = userStore.user.email;
        formData.date_of_birth = userStore.user.date_of_birth || "";
      }
    });

    const handleImageChange = (event: Event): void => {
      const target = event.target as HTMLInputElement;
      const file = target.files?.[0];
      
      if (file) {
        selectedImage.value = file;
        // Create preview URL
        const reader = new FileReader();
        reader.onload = (e) => {
          previewImage.value = e.target?.result as string;
        };
        reader.readAsDataURL(file);
      }
    };

    const handleSubmit = async (): Promise<void> => {
      saving.value = true;
      successMessage.value = "";
      errorMessage.value = "";

      try {
        const updateData: UpdateProfileForm = {
          email: formData.email,
          date_of_birth: formData.date_of_birth,
        };

        if (selectedImage.value) {
          updateData.profile_image = selectedImage.value;
        }

        await userStore.updateProfile(updateData);
        successMessage.value = "Profile updated successfully!";
        selectedImage.value = null;
        // Refresh the preview from store
        previewImage.value = "";
      } catch (err) {
        errorMessage.value = err instanceof Error ? err.message : "Failed to update profile";
      } finally {
        saving.value = false;
      }
    };

    return {
      userStore,
      formData,
      previewImage,
      saving,
      successMessage,
      errorMessage,
      handleImageChange,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.profile-card {
  max-width: 600px;
  margin: 0 auto;
}

.profile-image-section {
  padding: 2rem 0;
}

.profile-image-container {
  width: 150px;
  height: 150px;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-placeholder-large {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.profile-placeholder-large span {
  font-size: 4rem;
}

.form-label {
  color: #2d3748;
}

.form-control:disabled {
  background-color: #f8f9fa;
}
</style>
