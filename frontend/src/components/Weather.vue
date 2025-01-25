<template>
  <div class="weather-card">
    <!-- Weather Display -->
    <div class="weather-display" @click="toggleExpand">
      <div class="weather-header">
        <h2 class="text-lg font-semibold">Location and Temperature</h2>
        <button class="expand-button">
          <i :class="isExpanded ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
        </button>
      </div>
      <div class="weather-values">
        <div class="weather-value">
          <i class="fas fa-thermometer-half text-red-500"></i>
          <span>{{ temperature }}°C</span>
        </div>
        <div class="weather-value">
          <i class="fas fa-tint text-blue-500"></i>
          <span>{{ humidity }}%</span>
        </div>
      </div>
    </div>

    <!-- Expandable Input Section -->
    <div v-if="isExpanded" class="weather-inputs">
      <div class="input-group">
        <input 
          v-model="manualTemperature" 
          placeholder="Temperature" 
          type="number" 
          class="weather-input"
        />
        <input 
          v-model="manualHumidity" 
          placeholder="Humidity" 
          type="number"
          class="weather-input"
        />
      </div>
      <button @click="updateValues" class="set-values-button">
        Set Values
      </button>
    </div>

    <!-- Profile Edit Modal -->
    <div v-if="showProfileEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Edit Profile</h3>
          <button @click="showProfileEditModal = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M6 18L18 6M6 6l12 12" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
            </svg>
          </button>
        </div>
        <div class="space-y-4">
          <div v-for="field in profileFields" :key="field.key" class="flex items-center gap-4">
            <span class="font-medium w-32">{{ field.label }}:</span>
            <input 
              v-model="editingProfile[field.key]" 
              :type="field.type"
              :placeholder="field.placeholder"
              class="flex-1 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <span v-if="field.unit" class="text-gray-500">{{ field.unit }}</span>
          </div>
        </div>
        <div class="flex justify-between gap-3 mt-6">
          <button 
            @click="showDeleteConfirm"
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
          >
            Delete Profile
          </button>
          <div class="flex gap-3">
            <button 
              @click="showProfileEditModal = false"
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
            >
              Cancel
            </button>
            <button 
              @click="saveEditProfile"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'WeatherCard',
  setup() {
    const temperature = ref(20);
    const humidity = ref(50);
    const manualTemperature = ref(localStorage.getItem('temperature') || '');
    const manualHumidity = ref(localStorage.getItem('humidity') || '');
    const isExpanded = ref(false);
    const showProfileEditModal = ref(false);
    const editingProfile = ref({});
    const profileFields = [
      { key: 'name', label: 'Profile Name', type: 'text', placeholder: 'Enter profile name' },
      { key: 'location', label: 'Location', type: 'text', placeholder: 'Enter location' },
      { key: 'temperature', label: 'Temperature', type: 'number', placeholder: 'Enter temperature', unit: '°C' },
      { key: 'humidity', label: 'Humidity', type: 'number', placeholder: 'Enter humidity', unit: '%' }
    ];

    onMounted(() => {
      const storedTemperature = localStorage.getItem('temperature');
      const storedHumidity = localStorage.getItem('humidity');
      if (storedTemperature) temperature.value = parseFloat(storedTemperature);
      if (storedHumidity) humidity.value = parseFloat(storedHumidity);
    });

    const toggleExpand = () => {
      isExpanded.value = !isExpanded.value;
    };

    const updateValues = () => {
      if (manualTemperature.value) {
        temperature.value = parseFloat(manualTemperature.value);
        localStorage.setItem('temperature', temperature.value);
      }
      if (manualHumidity.value) {
        humidity.value = parseFloat(manualHumidity.value);
        localStorage.setItem('humidity', humidity.value);
      }
      manualTemperature.value = '';
      manualHumidity.value = '';
      isExpanded.value = false;
      window.location.reload();
    };

    const saveEditProfile = () => {
      // Logic to save the edited profile
      showProfileEditModal.value = false;
    };

    const showDeleteConfirm = () => {
      if (confirm('Are you sure you want to delete this profile?')) {
        // Logic to delete the profile
        showProfileEditModal.value = false;
      }
    };

    return {
      temperature,
      humidity,
      manualTemperature,
      manualHumidity,
      isExpanded,
      toggleExpand,
      updateValues,
      showProfileEditModal,
      editingProfile,
      profileFields,
      saveEditProfile,
      showDeleteConfirm,
    };
  },
};
</script>

<style scoped>
.weather-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.weather-display {
  padding: 12px;
  cursor: pointer;
}

.weather-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.expand-button {
  padding: 4px;
  color: #666;
  transition: transform 0.2s;
}

.weather-values {
  display: flex;
  justify-content: space-around;
  font-size: 0.9rem;
  color: #444;
}

.weather-value {
  display: flex;
  align-items: center;
  gap: 6px;
}

.weather-inputs {
  padding: 12px;
  border-top: 1px solid #eee;
  background-color: #f8f9fa;
}

.input-group {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.weather-input {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.set-values-button {
  width: 100%;
  padding: 8px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.set-values-button:hover {
  background-color: #4338ca;
}

/* Animation for expand/collapse */
.weather-inputs {
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
