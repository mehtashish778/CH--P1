<template>
  <div class="flex flex-col h-screen bg-gray-50">
    <!-- Main Content -->
    <main class="flex-grow p-6 mt-20 flex flex-col space-y-6">
      <!-- Navigation Bar -->
      <NavBar 
        :isMenuOpen="isMenuOpen" 
        :searchQuery="searchQuery" 
        @update:searchQuery="searchQuery = $event"
        :performSearch="performSearch" 
        :toggleMenu="toggleMenu"
      />
      
      <!-- Weather Card Component -->
      <WeatherCard />
      
      <!-- Recently Visited Section -->
      <section v-if="recentProfiles.length > 0" class="bg-white p-6 rounded-xl shadow-lg flex flex-col space-y-4">
        <h2 class="text-2xl font-semibold text-gray-900 border-b-2 border-gray-200 pb-3">Recently Visited Chemical Profiles</h2>
        <ul class="divide-y divide-gray-300">
          <li 
            v-for="profile in recentProfiles" 
            :key="profile['CAS Number']" 
            class="py-4 flex flex-col md:flex-row justify-between items-start md:items-center"
          >
            <div class="mb-2 md:mb-0">
              <p class="text-lg font-medium text-gray-900">Chemical Name: {{ profile['Chemical Name'] || 'N/A' }}</p>
              <p class="text-sm text-gray-600">CAS Number: {{ profile['CAS Number'] || 'N/A' }}</p>
              <p class="text-sm text-gray-600">Synonyms: {{ profile['Synonyms'].join(', ') || 'N/A' }}</p>
            </div>
            <router-link 
              :to="{ path: `/chemical-profile/${profile['CAS Number']}` }" 
              class="text-blue-600 hover:text-blue-800 font-medium underline"
            >
              View Profile
            </router-link>
          </li>
        </ul>
      </section>
    </main>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { defineComponent, ref, onMounted } from 'vue';
import NavBar from './NavBar.vue';
import WeatherCard from './Weather.vue';
import { cache } from '../router';

export default defineComponent({
  name: 'HomePage',
  components: {
    NavBar,
    WeatherCard
  },
  setup() {
    const router = useRouter();
    const isMenuOpen = ref(true);
    const searchQuery = ref('');
    const recentProfiles = ref(cache.recentProfiles || []);
    const areaLocation = ref('');
    const locationAccessDenied = ref(false);
    const manualCity = ref(localStorage.getItem('manualCity') || '');
    const temperature = ref(localStorage.getItem('temperature') ? parseFloat(localStorage.getItem('temperature')) : null);
    const humidity = ref(localStorage.getItem('humidity') ? parseFloat(localStorage.getItem('humidity')) : null);
    const errorMessage = ref('');
    const showModal = ref(false);
    const showTempModal = ref(false);
    const manualTemperature = ref(localStorage.getItem('manualTemperature') ? parseFloat(localStorage.getItem('manualTemperature')) : null);
    const manualHumidity = ref(localStorage.getItem('manualHumidity') ? parseFloat(localStorage.getItem('manualHumidity')) : null);
    const isAreaLocationOpen = ref(false);

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
    };

    const performSearch = () => {
      if (searchQuery.value) {
        router.push({ path: `/search/${searchQuery.value}` });
      } else {
        console.log("Please enter a search term");
      }
    };

    const fetchWeather = async (city) => {
      const apiKey = 'e2043ea21ec654dd007b0b3e14f48a12';
      try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}`);
        if (!response.ok) {
          throw new Error(`Weather data not found for the city: ${city}`);
        }
        const data = await response.json();
        if (data.main) {
          temperature.value = data.main.temp;
          errorMessage.value = '';
        }
      } catch (error) {
        console.error(error);
        errorMessage.value = error.message;
      }
    };

    const getLocation = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const { latitude, longitude } = position.coords;
            areaLocation.value = `Latitude: ${latitude}, Longitude: ${longitude}`;
            await fetchWeather(`${latitude},${longitude}`);
            cache.areaLocation = areaLocation.value;
            locationAccessDenied.value = false;
          },
          (error) => {
            console.error("Error getting location:", error);
            if (error.code === error.PERMISSION_DENIED) {
              areaLocation.value = "Location access denied. Please allow location access in your browser settings.";
            } else if (error.code === error.POSITION_UNAVAILABLE) {
              areaLocation.value = "Location information is unavailable.";
            } else if (error.code === error.TIMEOUT) {
              areaLocation.value = "The request to get user location timed out.";
            } else {
              areaLocation.value = "An unknown error occurred.";
            }
            locationAccessDenied.value = true;
          }
        );
      } else {
        areaLocation.value = "Geolocation is not supported by this browser.";
      }
    };

    const setManualLocation = async () => {
      if (manualCity.value) {
        areaLocation.value = `City: ${manualCity.value}`;
        await fetchWeather(manualCity.value);
        cache.areaLocation = areaLocation.value;
        localStorage.setItem('areaLocation', areaLocation.value);
        manualCity.value = '';
      } else {
        console.log("Please enter a city name");
      }
    };

    const setManualWeather = () => {
      if (manualTemperature.value != null && manualHumidity.value != null) {
        temperature.value = manualTemperature.value;
        humidity.value = manualHumidity.value;

        localStorage.setItem('temperature', manualTemperature.value);
        localStorage.setItem('humidity', manualHumidity.value);

        manualTemperature.value = null;
        manualHumidity.value = null;

        console.log("Manual weather data saved to localStorage");
      } else {
        console.log("Please enter both temperature and humidity values");
      }
    };

    onMounted(() => {
      getLocation();

      const cachedTemperature = localStorage.getItem('temperature');
      const cachedHumidity = localStorage.getItem('humidity');
      const cachedAreaLocation = localStorage.getItem('areaLocation');
      const cachedRecentProfiles = JSON.parse(localStorage.getItem('recentProfiles')) || [];

      if (cachedTemperature !== null) {
        temperature.value = parseFloat(cachedTemperature);
      }
      if (cachedHumidity !== null) {
        humidity.value = parseFloat(cachedHumidity);
      }
      if (cachedAreaLocation) {
        areaLocation.value = cachedAreaLocation;
      }
      recentProfiles.value = cachedRecentProfiles;
    });

    return {
      isMenuOpen,
      searchQuery,
      toggleMenu,
      performSearch,
      recentProfiles,
      areaLocation,
      locationAccessDenied,
      getLocation,
      manualCity,
      setManualLocation,
      errorMessage,
      showModal,
      showTempModal,
      manualTemperature,
      manualHumidity,
      setManualWeather,
      isAreaLocationOpen,
      temperature,
      humidity
    };
  }
});
</script>

<style>
body {
  font-family: 'Inter', sans-serif;
  background-color: #f9fafb;
  color: #1a202c;
}

section {
  margin-top: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #2d3748;
}

input[type="text"] {
  transition: border-color 0.3s, box-shadow 0.3s;
}

input[type="text"]:focus {
  outline: none;
  border-color: #3182ce;
  box-shadow: 0 0 0 2px rgba(49, 130, 206, 0.25);
}

button {
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  transform: translateY(-1px);
}

.bg-blue-600 {
  background-color: #2563eb;
}

.bg-blue-600:hover {
  background-color: #1d4ed8;
}

.bg-red-600 {
  background-color: #dc2626;
}

.bg-red-600:hover {
  background-color: #b91c1c;
}

.text-blue-600:hover {
  color: #1d4ed8;
}
</style>
