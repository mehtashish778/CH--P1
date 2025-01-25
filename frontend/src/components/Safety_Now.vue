<template>
  <div class="flex flex-col h-screen bg-white">
    <nav class="bg-white border-gray-200 dark:bg-gray-900">
      <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <a href="https://flowbite.com/" class="flex items-center space-x-3 rtl:space-x-reverse">
          <img src="@/assets/logo3.png" class="h-20" alt="Logo" />
          <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">ChemSafe</span>
        </a>
        <div class="hidden md:flex items-center md:order-2">
          <img src="@/assets/iitm_logo.png" class="h-20" alt="IITM Logo" />
        </div>
        <button 
          @click="toggleMenu"
          data-collapse-toggle="navbar-default" 
          type="button" 
          class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" 
          aria-controls="navbar-default" 
          :aria-expanded="isMenuOpen"
        >
          <span class="sr-only">Open main menu</span>
          <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
          </svg>
        </button>
        <div 
          class="hidden w-full md:block md:w-auto" 
          :class="{ 'block': isMenuOpen }"
          id="navbar-default"
        >
          <ul class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
            <li>
              <a href="#" class="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500" aria-current="page">Home</a>
            </li>
            <li>
              <a href="#" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">About</a>
            </li>
            <li>
              <a href="#" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Resources</a>
            </li>

          </ul>
        </div>
      </div>
    </nav>
    
    <!-- Hero Poster -->
    <div class="mx-5 my-2">
      <div class="rounded-lg overflow-hidden max-w-4xl mx-auto px-3">
        <img src="@/assets/Section_3.png" alt="Hero Poster" class="w-full object-cover" />
      </div>
    </div>
    <div class="bg-gradient-to-b from-[#1a237e]/90 to-[#0d47a1]/90 border-t border-blue-400/30 rounded-t-[2.5rem] w-full h-[65vh] shadow-[0_-10px_50px_rgba(30,64,175,0.25)] p-10">

      <!-- Sidebar for Enhanced Tab Buttons -->
      <div class="flex">

        <main class="flex-grow ml-0">
          <!-- Display Selected Tab Name -->
          <div class="flex justify-between">
            <div class="w-2/3">
              <h1 class="text-3xl font-bold mb-4 text-white flex justify-center">{{ selectedTab }}</h1>
            </div>
            <div class="w-1/3">
              <div class="relative">
                <div v-if="isDropdownOpen" class="absolute z-10 w-full bg-white border rounded-lg shadow-lg">
                  <ul class="max-h-60 overflow-y-auto">
                    <li 
                      v-for="option in dropdownOptions" 
                      :key="option.value" 
                      @click="selectOption(option)"
                      class="p-2 hover:bg-gray-100 cursor-pointer"
                    >
                      {{ option.label }}
                    </li>
                  </ul>
                </div>
              </div>
              <!-- Display Selected Location, Temperature, and Humidity -->
              <div>
                <button 
                    @click="isDetailsVisible = !isDetailsVisible; showDetailsModal = true" 
                    class="text-blue-500 flex justify-start"
                  >
                    <div class="p-4 border rounded-lg bg-gray-100">
                      <p class="text-lg font-semibold">Location: {{ selectedLocation.location }}</p>
                      <p class="text-md">Temperature: {{ selectedLocation.temperature }}°C</p>
                    </div>
                  </button>
                <div v-if="isDetailsVisible && selectedLocation" class="mt-4">






                  <div class="flex flex-col p-4 leading-normal">
                    <template v-if="selectedTab === 'Safety Now'">
                      <div class="space-y-4">
                        
                      </div>
                    </template>
                  </div>






                </div>
              </div>
            </div>
          </div>

          <!-- Main Content Area -->
          <div class="rounded-t-[2.5rem] w-full h-[65vh] p-10 bg-transparent">
            <!-- Enhanced Cards Container -->       
            <div class="flex justify-center gap-10">
              <!-- Updated First Card -->
              <div v-if="selectedTab === 'Safety Now'" 
                  class="flex-grow h-auto bg-gradient-to-b from-blue-500 to-blue-700 rounded-xl border border-white/20 shadow-lg transition-all duration-300 hover:bg-blue-600 cursor-pointer">
                <div class="flex flex-col justify-between p-6 h-full">
                  <div>
                    <h2 class="text-2xl font-bold mb-3 text-white">Search by Name/Formula</h2>
                    <p class="text-white/80 mb-6">Find detailed information about any chemical compound using its name or formula</p>
                  </div>
                  <SearchBar 
                    :search-query="searchQuery"
                    @update:searchQuery="searchQuery = $event"
                    :perform-search="performSearch"
                    placeholder="Enter chemical name or formula"
                    class="mt-auto p-2 rounded-lg border border-white/30 bg-white text-gray-800 focus:ring-2 focus:ring-blue-300"
                  />
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>

  <!-- Data Edit Modal -->
  <div v-if="showDataEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xl font-bold">Edit Data</h3>
        <button @click="showDataEditModal = false" class="text-gray-500 hover:text-gray-700">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M6 18L18 6M6 6l12 12" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
          </svg>
        </button>
      </div>
      <div class="space-y-4">
        <div v-for="field in displayFields" :key="field.key" class="flex items-center gap-4">
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
      <div class="flex justify-end gap-3 mt-6">
        <button 
          @click="showDataEditModal = false"
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

  <!-- Add this somewhere in your template to use selectedLocationProfile -->
  <div v-if="selectedLocation" class="text-sm text-gray-500 mt-2">
    Selected Profile: {{ selectedLocation.name }}
  </div>

  <!-- Details Modal -->
  <div v-if="showDetailsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md">
      <div class="flex justify-between items-center mb-4">
        <button @click="showDetailsModal = false" class="text-gray-500 hover:text-gray-700">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M6 18L18 6M6 6l12 12" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
          </svg>
        </button>
      </div>

      <!-- Location Profile Selector -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
              <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
            </svg>
            Location
          </h2>
        </div>

        <div class="flex gap-2">
          <div class="relative flex-grow">
            <select 
              v-model="selectedLocation" 
              @change="handleLocationChange"
              class="w-full p-3 pl-4 pr-10 border rounded-lg appearance-none bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-700 transition-all duration-200"
            >
              <option value="" disabled>Select Location Profile</option>
              <option 
                v-for="profile in locationProfiles" 
                :key="profile.id" 
                :value="profile"
                class="py-2"
              >
                {{ profile.name }} {{ profile.id === 1 && profile.location !== 'Auto Detect' ? `(${profile.location})` : '' }}
              </option>
              <option value="add_new" class="text-blue-500 font-medium">+ Add New Location</option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none text-gray-500">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
              </svg>
            </div>
          </div>

          <button 
            v-if="selectedLocation && selectedLocation !== 'add_new'"
            @click="openProfileEditModal"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-all duration-200 flex items-center gap-2 whitespace-nowrap"
            title="Edit Profile"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
            </svg>
            <span class="hidden sm:inline">Edit</span>
          </button>
        </div>
      </div>

      <!-- New Profile Modal -->
      <div v-if="showNewProfileModal" class="fixed inset-0 bg-black bg-opacity-100 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold">Create New Profile</h3>
            <button @click="showNewProfileModal = false" class="text-gray-500 hover:text-gray-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M6 18L18 6M6 6l12 12" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
              </svg>
            </button>
          </div>
          <div class="space-y-4">
            <div v-for="field in profileFields" :key="field.key" class="flex items-center gap-4">
              <span class="font-medium w-32">{{ field.label }}:</span>
              <input 
                v-model="newProfile[field.key]" 
                :type="field.type"
                :placeholder="field.placeholder"
                class="flex-1 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <span v-if="field.unit" class="text-gray-500">{{ field.unit }}</span>
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button 
              @click="showNewProfileModal = false"
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
            >
              Cancel
            </button>
            <button 
              @click="saveNewProfile"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              Save Profile
            </button>
          </div>
        </div>
      </div>



      <!-- Selected Location Details -->
      <div v-if="selectedLocation && selectedLocation !== 'add_new'" class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
        <!-- Location Header -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
              <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
            </svg>
            <span class="font-medium text-lg">{{ selectedLocation.location }}</span>
          </div>
          <div class="flex gap-2">
            <button 
              @click="openDataEditModal"
              class="p-2 text-blue-500 hover:bg-blue-50 rounded-full transition-all duration-200"
              title="Edit Data Manually"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
              </svg>
            </button>
            <button 
              @click="fetchLocationData"
              class="p-2 text-green-500 hover:bg-green-50 rounded-full transition-all duration-200"
              title="Fetch Latest Data"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Environment Data Cards -->
        <div class="grid grid-cols-2 gap-4">
          <!-- Temperature Card -->
          <div class="bg-gradient-to-br from-orange-50 to-red-50 p-4 rounded-lg border border-orange-100">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
                </svg>
                <span class="text-sm font-medium text-gray-600">Temperature</span>
              </div>
              <span class="text-2xl font-bold text-gray-800">{{ selectedLocation.temperature }}°C</span>
            </div>
          </div>

          <!-- Humidity Card -->
          <div class="bg-gradient-to-br from-blue-50 to-cyan-50 p-4 rounded-lg border border-blue-100">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"/>
                </svg>
                <span class="text-sm font-medium text-gray-600">Humidity</span>
              </div>
              <span class="text-2xl font-bold text-gray-800">{{ selectedLocation.humidity }}%</span>
            </div>
          </div>
        </div>

        <!-- Last Updated Info -->
        <div class="mt-4 text-xs text-gray-500 text-right">
          Last updated: {{ new Date().toLocaleString() }}
        </div>
      </div>


      <div class="flex justify-end gap-3 mt-6">
        <button @click="showDetailsModal = false" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import SearchBar from './SearchBar.vue';
import { useRouter } from 'vue-router';
import { useLocationStore } from '../composables/useLocationStore';

export default defineComponent({
  name: 'Safety_Now',
  components: {
    SearchBar
  },
  setup() {
    const router = useRouter();
    const { 
      selectedLocationProfile, 
      locationProfiles,
      setSelectedLocation, 
      getSelectedLocation,
      addProfile,
      updateProfile,
      deleteProfile,
      fetchCurrentLocationData
    } = useLocationStore();

    const selectedLocation = ref(selectedLocationProfile.value);
    const showNewProfileModal = ref(false);
    const showDataEditModal = ref(false);
    const showProfileEditModal = ref(false);
    const editingProfile = ref({});
    const showActionsDropdown = ref(false);
    const newProfile = ref({
      name: '',
      location: '',
      temperature: '',
      humidity: ''
    });
    const isMenuOpen = ref(false);
    const searchQuery = ref('');
    const selectedTab = ref('Safety Now');
    const tabs = ['Safety Now', 'Safety Pro', 'Safety Guru'];
    const isDropdownOpen = ref(false);
    const isDetailsVisible = ref(false);
    const showDetailsModal = ref(false);

    const profileFields = [
      { key: 'name', label: 'Profile Name', type: 'text', placeholder: 'Enter profile name' },
      { key: 'location', label: 'Location', type: 'text', placeholder: 'Enter location' },
      { key: 'temperature', label: 'Temperature', type: 'number', placeholder: 'Enter temperature', unit: '°C' },
      { key: 'humidity', label: 'Humidity', type: 'number', placeholder: 'Enter humidity', unit: '%' }
    ];

    // New computed array for display fields (excluding profile name)
    const displayFields = [
      { key: 'location', label: 'Location', type: 'text', placeholder: 'Enter location' },
      { key: 'temperature', label: 'Temperature', type: 'number', placeholder: 'Enter temperature', unit: '°C' },
      { key: 'humidity', label: 'Humidity', type: 'number', placeholder: 'Enter humidity', unit: '%' }
    ];

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
    };

    const performSearch = () => {
      if (searchQuery.value) {
        // Navigate to search results page
        router.push({ path: `/search/${searchQuery.value}` });
      }
    };

    const fetchLocationData = async () => {
      try {
        const response = await new Promise(resolve => setTimeout(() => {
          resolve({
            temperature: Math.round(25 + Math.random() * 10),
            humidity: Math.round(60 + Math.random() * 30)
          });
        }, 1000));

        if (selectedLocation.value) {
          const updatedProfile = {
            ...selectedLocation.value,
            temperature: response.temperature,
            humidity: response.humidity
          };
          updateProfile(updatedProfile);
          selectedLocation.value = updatedProfile;
          setSelectedLocation(updatedProfile);
        }
      } catch (error) {
        console.error('Error fetching location data:', error);
      }
    };

    const openDataEditModal = () => {
      editingProfile.value = { ...selectedLocation.value };
      showDataEditModal.value = true;
      showActionsDropdown.value = false; // Close dropdown when opening modal
    };

    const saveEditProfile = () => {
      if (editingProfile.value.id) {
        updateProfile(editingProfile.value);
        selectedLocation.value = editingProfile.value;
        setSelectedLocation(editingProfile.value);
      }
      showDataEditModal.value = false;
    };

    const saveNewProfile = () => {
      if (!newProfile.value.name || !newProfile.value.location) {
        alert('Please fill in at least the profile name and location');
        return;
      }

      const profile = {
        id: Date.now(),
        name: newProfile.value.name,
        location: newProfile.value.location,
        temperature: Number(newProfile.value.temperature) || 0,
        humidity: Number(newProfile.value.humidity) || 0
      };

      addProfile(profile);
      selectedLocation.value = profile;
      setSelectedLocation(profile);
      showNewProfileModal.value = false;
      newProfile.value = {
        name: '',
        location: '',
        temperature: '',
        humidity: ''
      };
    };

    const handleLocationChange = async () => {
      if (selectedLocation.value === 'add_new') {
        selectedLocation.value = '';
        showNewProfileModal.value = true;
      } else if (selectedLocation.value) {
        if (selectedLocation.value.id === 1) { // Current Location profile
          try {
            const currentLocationData = await fetchCurrentLocationData();
            selectedLocation.value = currentLocationData;
            setSelectedLocation(currentLocationData);
          } catch (error) {
            console.error('Failed to fetch current location:', error);
            // Optionally show an error message to the user
          }
        } else {
          setSelectedLocation(selectedLocation.value);
        }
      }
    };

    const showDeleteConfirm = () => {
      if (confirm('Are you sure you want to delete this profile?')) {
        deleteProfile(editingProfile.value.id);
        showDataEditModal.value = false;
      }
    };

    const openProfileEditModal = () => {
      editingProfile.value = { ...selectedLocation.value };
      showProfileEditModal.value = true;
    };

    // Load profiles from localStorage when component mounts
    onMounted(() => {
      const savedProfiles = localStorage.getItem('locationProfiles');
      if (savedProfiles) {
        locationProfiles.value = JSON.parse(savedProfiles);
        
        // If there's a saved selected location, find it in the profiles
        const savedLocation = getSelectedLocation();
        if (savedLocation) {
          const foundProfile = locationProfiles.value.find(p => p.id === savedLocation.id);
          if (foundProfile) {
            selectedLocation.value = foundProfile;
          }
        }
      } else {
        // Set default profiles if none exist
        locationProfiles.value = [
          {
            id: 1,
            name: 'Chennai Lab',
            location: 'Chennai, India',
            temperature: 30,
            humidity: 75
          },
          {
            id: 2,
            name: 'Mumbai Facility',
            location: 'Mumbai, India',
            temperature: 28,
            humidity: 80
          }
        ];
        // Save default profiles to localStorage
        localStorage.setItem('locationProfiles', JSON.stringify(locationProfiles.value));
      }
    });

    return {
      selectedLocation,
      locationProfiles,
      showNewProfileModal,
      showDataEditModal,
      showProfileEditModal,
      editingProfile,
      showActionsDropdown,
      newProfile,
      handleLocationChange,
      saveNewProfile,
      saveEditProfile,
      showDeleteConfirm,
      fetchLocationData,
      openDataEditModal,
      isMenuOpen,
      toggleMenu,
      searchQuery,
      performSearch,
      selectedTab,
      tabs,
      profileFields,
      displayFields,
      openProfileEditModal,
      isDropdownOpen,
      isDetailsVisible,
      showDetailsModal
    };
  }
});
</script>

<style>
body {
  font-family: 'Inter', sans-serif;
  background-color: #ffffff;
  color: #1a202c;
}
</style>
