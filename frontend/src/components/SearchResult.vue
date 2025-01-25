<template>
  <div class="container">
    <h1 class="page-title">Search Chemicals</h1>
    <div class="search-bar">
      <input 
        v-model="search_querry" 
        :placeholder="search_querry || 'Enter chemical name or CAS number...'" 
        @keyup.enter="performSearch_2" 
        class="search-input"
      />
      <button 
        @click="performSearch_2" 
        class="search-button"
      >
        Search
      </button>
    </div>

    <h2 class="subtitle">Search Results</h2>
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
    </div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    
    <ul v-if="searchResults.length" class="search-results">
      <li v-for="result in searchResults" :key="result.name" class="result-item">
        <div class="result-content">
          <div class="result-header">
            <h3 class="result-title">{{ result.name }}</h3>
          </div>
          <div class="result-body">
            <p class="result-description">{{ result.description }}</p>
          </div>
        </div>
      </li>
    </ul>

    <div v-else-if="!loading && !errorMessage" class="no-results">
      No results found for "{{ search_querry }}".
    </div>
  </div>
</template>

<script>


export default {
  data() {
    return {
      search_querry: "",
      searchResults: [],
      errorMessage: '',
      loading: false
    };
  },
  mounted() {
    this.performSearch(); // Call performSearch when the component is mounted
  },
  watch: {
    '$route.params.search_querry': 'performSearch' // Watch for changes in the search query
  },
  methods: {
    async performSearch() {
      this.loading = true;
      this.errorMessage = '';
      this.searchResults = [];
      this.search_querry = this.$route.params.search_querry;

      try {
        const response = await fetch(`http://10.17.18.109:8000/search_2?name_or_CAS=${this.search_querry}`);
        if (!response.ok) {
          throw new Error('Error fetching search results');
        }
        const data = await response.json();
        if (data.status === 'error') {
          this.errorMessage = data.message;
        } else {
          this.searchResults = data.results;
        }
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.loading = false;
      }
    },
    async performSearch_2() {
      if (this.search_querry) {
        this.$router.push({ path: `/search/${this.search_querry}` }); // Navigate to search results
      } else {
        console.log('Please enter a search term'); // Log if no search term is provided
      }
    },
    viewDetails(casNumber) {
      if (casNumber === '60-29-7') {
        this.$router.push('/chemical-profile-dee');
      } else {
        this.$router.push(`/chemical-profile/${casNumber}`);
      }
    },

    addToFavorites(casNumber) {
      alert(`Added CAS Number ${casNumber} to favorites.`);
    }
  }
};
</script>

<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 2em;
  margin-bottom: 10px;
  text-align: center;
  color: #333;
}

.subtitle {
  margin-top: 20px;
  font-size: 1.5em;
  color: #555;
}

.search-input {
  flex: 1;
  margin-right: 10px;
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1em;
}

.search-results {
  list-style-type: none;
  padding: 0;
  margin: 20px 0;
}

.result-item {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 15px;
  padding: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.result-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.result-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.result-title {
  font-size: 1.3em;
  color: #2c3e50;
  margin: 0;
  font-weight: 600;
}

.result-body {
  padding-top: 8px;
}

.result-description {
  color: #666;
  line-height: 1.5;
  margin: 0;
  font-size: 1rem;
}

.action-icons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 1.5em;
  align-items: center;
}

.tooltip {
  position: relative;
  cursor: pointer;
}

.tooltip::after {
  content: attr(title);
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #000;
  color: #fff;
  padding: 5px;
  border-radius: 3px;
  font-size: 0.75em;
  white-space: nowrap;
  display: none;
}

.tooltip:hover::after {
  display: block;
}

.error {
  color: red;
  font-weight: bold;
  margin: 20px 0;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007acc;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-results {
  text-align: center;
  font-size: 1.2em;
  color: #555;
}

.search-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.search-button {
  margin-left: 10px; /* Add some space between the input and button */
  padding: 10px 15px;
  background-color: #007acc;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #005fa3; /* Darker shade on hover */
}

.download-links {
  margin-top: 10px;
}

.download-links ul {
  list-style: none;
  padding-left: 20px;
}

.download-links a {
  color: #007acc;
  text-decoration: none;
}

.download-links a:hover {
  text-decoration: underline;
}
</style>

