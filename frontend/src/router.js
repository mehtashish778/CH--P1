// frontend/src/router.js
import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './components/Home.vue'
import ChemicalProfile from './components/ChemicalProfile.vue'
import SearchResult from './components/SearchResult.vue'
import { reactive } from 'vue'
import axios from 'axios'

// Load recent profiles from localStorage if available
const loadCacheFromLocalStorage = () => {
    const storedProfiles = localStorage.getItem('recentProfiles');
    return storedProfiles ? JSON.parse(storedProfiles) : [];
};

//A reactive cache to store recently visited chemical profiles
const cache = reactive({
    recentProfiles: loadCacheFromLocalStorage()  // Load from localStorage
});

// Function to save the cache to localStorage
const saveCacheToLocalStorage = () => {
    localStorage.setItem('recentProfiles', JSON.stringify(cache.recentProfiles));
};

// Function to fetch chemical details from the API
async function fetchChemicalDetails(CAS_number) {
    try {
        const response = await axios.get('http://127.0.0.1:8000/chemical', {
            params: { CAS_number: CAS_number }
        });
        return response.data;  // Return the fetched chemical details
    } catch (error) {
        console.error("Error fetching chemical details:", error);
        return null;  // Return null in case of error
    }
}

const routes = [
    { path: '/', component: HomePage },
    { path: '/search/:search_querry', component: SearchResult },
    { path: '/chemical-profile/:CAS_number', component: ChemicalProfile }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Add a navigation guard to update the cache when visiting a chemical profile
router.beforeEach(async (to, from, next) => {
    if (to.path.startsWith('/chemical-profile/')) {  // Check if the path matches the chemical profile route
        const CAS_number = to.params.CAS_number;
        const chemical = await fetchChemicalDetails(CAS_number);  // Fetch the chemical details
        if (chemical && !cache.recentProfiles.some(profile => profile["CAS Number"] === chemical["CAS Number"])) {
            cache.recentProfiles.push(chemical);  // Store the full chemical details
            saveCacheToLocalStorage();  // Save the updated cache to localStorage
        }
    }
    next();
});

export { cache };  // Export the cache for use in components
export default router