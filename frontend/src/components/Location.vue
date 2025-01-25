<template>
  <div class="bg-white p-6 rounded-xl shadow-lg">
    <div class="flex justify-between items-center mb-6">
      <div class="flex items-center space-x-4">
        <h2 class="text-2xl font-semibold text-gray-900">Locations</h2>
        <!-- Added Location Selector Dropdown -->
        <div class="relative">
          <button 
            @click="toggleDropdown"
            class="bg-blue-100 text-blue-800 px-4 py-2 rounded-lg hover:bg-blue-200 flex items-center"
          >
            {{ selectedLocation ? selectedLocation.name : 'Select Location' }}
            <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
            </svg>
          </button>
          <div 
            v-if="showDropdown" 
            class="absolute z-10 mt-2 bg-white divide-y divide-gray-100 rounded-lg shadow w-44"
          >
            <ul class="py-2 text-sm text-gray-700">
              <li v-for="(location, index) in locations" :key="index">
                <a 
                  href="#" 
                  @click.prevent="selectLocation(location)"
                  class="block px-4 py-2 hover:bg-gray-100"
                >
                  {{ location.name }}
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <button
        @click="showAddLocationModal = true"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
      >
        Add Location
      </button>
    </div>

    <!-- Locations List -->
    <div class="space-y-4">
      <div
        v-for="(location, index) in locations"
        :key="index"
        class="p-4 border rounded-lg flex justify-between items-center"
      >
        <div>
          <h3 class="text-lg font-medium">{{ location.name }}</h3>
          <div class="text-sm text-gray-600">
            <p>Temperature: {{ location.temperature }}°C</p>
            <p>Humidity: {{ location.humidity }}%</p>
          </div>
        </div>
        <button
          @click="removeLocation(index)"
          class="text-red-600 hover:text-red-800"
        >
          Remove
        </button>
      </div>
    </div>

    <!-- Add Location Modal -->
    <div v-if="showAddLocationModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-xl w-96">
        <h3 class="text-xl font-semibold mb-4">Add New Location</h3>
        <form @submit.prevent="addLocation" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Location Name</label>
            <input
              v-model="newLocation.name"
              type="text"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Temperature (°C)</label>
            <input
              v-model="newLocation.temperature"
              type="number"
              step="0.1"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Humidity (%)</label>
            <input
              v-model="newLocation.humidity"
              type="number"
              min="0"
              max="100"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="showAddLocationModal = false"
              class="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Add Location
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';

export default defineComponent({
  name: 'LocationManager',
  setup() {
    const locations = ref([]);
    const showAddLocationModal = ref(false);
    const newLocation = ref({
      name: '',
      temperature: '',
      humidity: ''
    });
    const showDropdown = ref(false);
    const selectedLocation = ref(null);

    const addLocation = () => {
      locations.value.push({
        name: newLocation.value.name,
        temperature: parseFloat(newLocation.value.temperature),
        humidity: parseFloat(newLocation.value.humidity)
      });
      
      // Save to localStorage
      localStorage.setItem('locations', JSON.stringify(locations.value));
      
      // Reset form
      newLocation.value = {
        name: '',
        temperature: '',
        humidity: ''
      };
      showAddLocationModal.value = false;
    };

    const removeLocation = (index) => {
      locations.value.splice(index, 1);
      localStorage.setItem('locations', JSON.stringify(locations.value));
    };

    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value;
    };

    const selectLocation = (location) => {
      selectedLocation.value = location;
      showDropdown.value = false;
      
      // Update weather values in localStorage
      localStorage.setItem('temperature', location.temperature);
      localStorage.setItem('humidity', location.humidity);
      localStorage.setItem('selectedLocation', JSON.stringify(location));
      
      // Trigger weather component refresh
      window.location.reload();
    };

    onMounted(() => {
      const savedLocations = localStorage.getItem('locations');
      if (savedLocations) {
        locations.value = JSON.parse(savedLocations);
      }
      
      // Load selected location
      const savedSelectedLocation = localStorage.getItem('selectedLocation');
      if (savedSelectedLocation) {
        selectedLocation.value = JSON.parse(savedSelectedLocation);
      }
    });

    return {
      locations,
      showAddLocationModal,
      newLocation,
      addLocation,
      removeLocation,
      showDropdown,
      selectedLocation,
      toggleDropdown,
      selectLocation,
    };
  }
});
</script>
