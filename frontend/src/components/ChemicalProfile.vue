<template>
  <div class="flex flex-col h-screen">
    <NavBar 
      :isMenuOpen="isMenuOpen" 
      :searchQuery="searchQuery" 
      @update:searchQuery="searchQuery = $event"
      :performSearch="performSearch" 
      class="navbar"
    />

    <main class="flex-grow p-4 mt-16">

      <div class="flex flex-col md:flex-row justify-between items-start">

        <!-- Section 1: Chemical Profile -->

        <div v-if="chemicalDetails" class="chemical-card mt-4 mx-auto shadow-lg">
          <h2 class="chemical-name text-2xl font-semibold">{{ chemicalDetails["Chemical Name"] }}</h2>
          <p class="cas-number text-gray-700">
            <i class="fas fa-vial"></i>
            <strong>CAS No:</strong> {{ chemicalDetails["CAS Number"] }}
          </p>
          <p class="common-names text-gray-600">
            <i class="fas fa-tags"></i>
            <strong>Common Names:</strong> {{ chemicalDetails["Synonyms"].join(', ') }}
          </p>
        </div>

        <!-- Weather Component -->
        <Weather class="mt-4 md:mt-0 md:ml-4" />

      </div>

      <!-- Section 3: Instructions -->
      <div class="mt-4">
        <h3 class="text-lg font-bold text-center text-blue-600 border-b-2 border-blue-600 pb-2">Instructions</h3>
        <div class="tabs grid grid-cols-2 md:flex md:flex-nowrap mt-2 gap-2">
          <button @click="toggleInstruction('handling')" :class="{'active': expandedInstruction === 'handling'}" class="tab-button transition-transform transform hover:scale-105">
            <i class="fas fa-hand-holding"></i> Handling
          </button>
          <button @click="toggleInstruction('storage')" :class="{'active': expandedInstruction === 'storage'}" class="tab-button transition-transform transform hover:scale-105">
            <i class="fas fa-warehouse"></i> Storage
          </button>
          <button @click="toggleInstruction('ppe')" :class="{'active': expandedInstruction === 'ppe'}" class="tab-button transition-transform transform hover:scale-105">
            <i class="fas fa-shield-alt"></i> PPE
          </button>
          <button @click="toggleInstruction('flammability')" :class="{'active': expandedInstruction === 'flammability'}" class="tab-button transition-transform transform hover:scale-105">
            <i class="fas fa-fire"></i> Flammability
          </button>
          <button @click="toggleInstruction('toxicity')" :class="{'active': expandedInstruction === 'toxicity'}" class="tab-button transition-transform transform hover:scale-105">
            <i class="fas fa-skull-crossbones"></i> Toxicity
          </button>
          <button @click="toggleInstruction('fireExtinguisher')" :class="{'active': expandedInstruction === 'fireExtinguisher'}" class="tab-button transition-transform transform hover:scale-105">
            <i class="fas fa-fire-extinguisher"></i> Fire Extinguisher
          </button>
          <button @click="toggleInstruction('reactivityAndStability')" :class="{'active': expandedInstruction === 'reactivityAndStability'}" class="tab-button transition-transform transform hover:scale-105">
            <i class="fas fa-exclamation-triangle"></i> Reactivity and Stability
          </button>
          <button @click="toggleInstruction('firstAidMeasures')" :class="{'active': expandedInstruction === 'firstAidMeasures'}" class="tab-button transition-transform transform hover:scale-105">
            <i class="fas fa-plus-circle"></i> First Aid Measures
          </button>
          <button @click="toggleInstruction('transportation')" :class="{'active': expandedInstruction === 'transportation'}" class="tab-button transition-transform transform hover:scale-105">
            <i class="fas fa-truck"></i> Transportation
          </button>
        </div>

        <!-- Expandable Instruction Details -->
        <div v-if="expandedInstruction" class="mt-4 p-4 bg-gray-100 rounded-lg border border-gray-300">
          <h4 class="font-bold text-lg">{{ expandedInstruction }} Instruction</h4>
          <p v-if="expandedInstruction === 'handling' && chemicalDetails" v-html="formatInstruction(chemicalDetails['Handling Instruction'])"></p>
          <p v-if="expandedInstruction === 'storage' && chemicalDetails">{{ formatInstruction(chemicalDetails["Storage Instruction"]) }}</p>
          <p v-if="expandedInstruction === 'ppe' && chemicalDetails">{{ formatPPE(chemicalDetails["PPE Instruction"]) }}</p>
          <p v-if="expandedInstruction === 'flammability' && chemicalDetails">{{ formatInstruction(chemicalDetails["Flammability Instruction"]?.Precautions) }}</p>
          <p v-if="expandedInstruction === 'toxicity' && chemicalDetails">{{ formatInstruction(chemicalDetails["Toxicity Instruction"]?.["Acute Toxicity"]) }}</p>
          <p v-if="expandedInstruction === 'fireExtinguisher' && chemicalDetails">{{ formatInstruction(chemicalDetails["Fire Extinguisher Instruction"]) }}</p>
          <button @click="expandedInstruction = null" class="mt-2 text-red-500 hover:underline">Close</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import NavBar from './NavBar.vue';
import Weather from './Weather.vue';
import 'font-awesome/css/font-awesome.css';

export default {
  name: 'ChemicalProfile',
  components: {
    NavBar,
    Weather
  },
  data() {
    return {
      isMenuOpen: false,
      expandedInstruction: null,
      chemicalDetails: null,
      searchQuery: '',
      chemicalAmount: 1, // Default amount

    };
  },
  created() {
    this.fetchChemicalDetails();
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    performSearch() {
      if (this.searchQuery) {
        this.$router.push({ path: `/search/${this.searchQuery}` });
      } else {
        console.log("Please enter a search term");
      }
    },
    toggleInstruction(instruction) {
      this.expandedInstruction = this.expandedInstruction === instruction ? null : instruction;
    },
    async fetchChemicalDetails() {
      const CAS_number = this.$route.params.CAS_number;
      console.log("Fetching details for CAS number:", CAS_number);
      try {
        const response = await axios.get('http://127.0.0.1:8000/chemical', {
          params: { CAS_number: CAS_number }
        });
        console.log("API Response:", response.data);
        this.chemicalDetails = response.data;
      } catch (error) {
        console.error("Error fetching chemical details:", error);
      }
    },
    formatPPE(instructions) {
      return Object.entries(instructions).map(([key, value]) => `${key}: ${value}`).join(', ');
    },
    formatInstruction(instructions) {
      return instructions.map(item => `• ${item}`).join('<br/>');
    }
  },
  props: {
  },
  head: {
    link: [
      { rel: 'stylesheet', href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css' }
    ]
  }
};
</script>

<style>
.chemical-card {
  max-width: 600px;
  padding: 20px;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-align: left;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.chemical-name {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.cas-number,
.common-names {
  font-size: 1rem;
  color: #555;
  margin-bottom: 8px;
}

.tabs {
  margin-top: 20px;
}

.tab-button {
  padding: 12px 20px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-weight: bold;
  color: #555;
  transition: background 0.3s, color 0.3s;
  flex: 1;
  min-width: 120px;
  border-radius: 5px;
  margin: 0 5px;
}

.tab-button:hover {
  background: #e0e0e0;
  color: #000;
}

.tab-button.active {
  background: #007bff;
  color: white;
  border-radius: 5px 5px 0 0;
}

.tab-button i {
  margin-right: 5px;
}

@media (max-width: 768px) {
  .chemical-card {
    padding: 15px;
  }
  .chemical-name {
    font-size: 1.5rem;
  }
  .cas-number,
  .common-names {
    font-size: 0.875rem;
  }
}

.chemical-card:hover {
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.navbar {
  position: relative;
  z-index: 10;
}

.square-container {
  width: 100px; /* Set the width of the square */
  height: 100px; /* Set the height of the square */
  background-color: #007bff; /* Set the background color */
  margin: 0 auto; /* Center the square horizontally */
}

.section-amount {
  flex: 1; /* Allow the section to grow */
  margin-right: 20px; /* Add some space between sections on desktop */
}

@media (max-width: 768px) {
  .section-amount {
    margin-right: 0; /* Remove margin on mobile */
  }
}
</style>
