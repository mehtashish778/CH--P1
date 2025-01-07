<template>
  <div class="weather-card">
    <h2>Weather Information</h2>
    <p>Temperature: {{ temperature }} °C</p>
    <p>Humidity: {{ humidity }} %</p>
    <input v-model="manualTemperature" placeholder="Set Temperature" type="number" />
    <input v-model="manualHumidity" placeholder="Set Humidity" type="number" />
    <button @click="updateValues">Set Values</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'WeatherCard',
  setup() {
    const temperature = ref(20); // Default temperature
    const humidity = ref(50); // Default humidity
    const manualTemperature = ref(localStorage.getItem('temperature') || ''); // Use cached value if available
    const manualHumidity = ref(localStorage.getItem('humidity') || ''); // Use cached value if available

    // Load values from localStorage on component mount
    onMounted(() => {
      const storedTemperature = localStorage.getItem('temperature');
      const storedHumidity = localStorage.getItem('humidity');
      if (storedTemperature) {
        temperature.value = parseFloat(storedTemperature);
      }
      if (storedHumidity) {
        humidity.value = parseFloat(storedHumidity);
      }
    });

    const updateValues = () => {
      if (manualTemperature.value) {
        const newTemperature = parseFloat(manualTemperature.value);
        if (newTemperature !== temperature.value) { // Check if the value is updated
          temperature.value = newTemperature;
          localStorage.setItem('temperature', temperature.value); // Store in localStorage
          console.log(`Temperature updated to: ${temperature.value}`); // Log the updated temperature
        }
      }
      if (manualHumidity.value) {
        const newHumidity = parseFloat(manualHumidity.value);
        if (newHumidity !== humidity.value) { // Check if the value is updated
          humidity.value = newHumidity;
          localStorage.setItem('humidity', humidity.value); // Store in localStorage
          console.log(`Humidity updated to: ${humidity.value}`); // Log the updated humidity
        }
      }
      manualTemperature.value = '';
      manualHumidity.value = '';
    };

    return {
      temperature,
      humidity,
      manualTemperature,
      manualHumidity,
      updateValues,
    };
  },
};
</script>

<style scoped>
.weather-card {
  border: 1px solid #ccc;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  opacity: 0;
  animation: fadeIn 0.5s forwards;
}

.weather-card h2 {
  margin-bottom: 10px;
}

.weather-card input {
  margin: 5px 0;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.weather-card button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: transform 0.2s;
}

.weather-card button:hover {
  transform: scale(1.05);
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}
</style>
