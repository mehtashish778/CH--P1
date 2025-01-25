<template>
  <nav class="bg-gray-900 text-white shadow-lg fixed top-0 left-0 w-full z-50">
    <div class="container mx-auto px-4 py-3 flex items-center justify-between">
      <!-- Logo -->
      <div class="flex items-center justify-start w-1/4">
        <h1 class="text-2xl font-bold tracking-wide">ChemEasy</h1>
      </div>

      <!-- Search Bar -->
      <div class="hidden md:flex items-center w-1/2 justify-center">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search Chemical Name"
          class="flex-1 border border-gray-400 rounded-l-lg p-2 shadow-sm focus:ring-2 focus:ring-blue-600 focus:border-blue-600 transition duration-200 text-black"
        />
        <button
          class="bg-blue-700 text-white rounded-r-lg px-4 py-2 hover:bg-blue-800 shadow-md focus:outline-none focus:ring-2 focus:ring-blue-600 transition duration-200"
          @click="performSearch"
        >
          Search
        </button>
      </div>

      <!-- Navigation Menu -->
      <div class="hidden md:flex items-center justify-end w-1/4 space-x-8">
        <a href="/" class="text-white hover:text-blue-400 transition">Home</a>
        <a href="#resources" class="text-white hover:text-blue-400 transition">Resources</a>
      </div>

      <!-- Mobile Menu Button -->
      <button
        @click="toggleMenu"
        class="text-white md:hidden focus:outline-none"
        aria-label="Toggle Menu"
        :aria-expanded="isMenuOpen.toString()"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            v-if="!isMenuOpen"
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M4 6h16M4 12h16m-7 6h7"
          />
          <path
            v-if="isMenuOpen"
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <div
      :class="`absolute top-0 left-0 w-3/4 h-screen bg-gray-800 shadow-lg transition-transform transform ${
        isMenuOpen ? 'translate-x-0' : '-translate-x-full'
      } md:hidden`"
    >
      <ul class="flex flex-col items-start space-y-6 py-6 px-4" role="menu">
        <li role="menuitem">
          <a href="/" class="block text-white hover:text-blue-400 transition">Home</a>
        </li>
        <li role="menuitem">
          <a href="#about" class="block text-white hover:text-blue-400 transition">About</a>
        </li>
        <li role="menuitem">
          <a href="#resources" class="block text-white hover:text-blue-400 transition">Resources</a>
        </li>
      </ul>
    </div>

    <!-- Mobile Search Bar -->
    <div class="md:hidden mt-4 flex bg-gray-700 px-4">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search for a chemical..."
        class="flex-1 border border-gray-600 bg-white text-black rounded-l-lg p-2 shadow-md transition duration-200 focus:ring-2 focus:ring-blue-500"
      />
      <button
        class="bg-blue-600 text-white rounded-r-lg px-4 py-1 hover:bg-blue-700 focus:outline-none transition duration-200"
        @click="performSearch"
      >
        Search
      </button>
    </div>
  </nav>
</template>

<script>
export default {
  props: {
    isMenuOpen: {
      type: Boolean,
      required: true,
    },
    toggleMenu: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      searchQuery: '',
      debounceTimeout: null,
    };
  },
  methods: {
    performSearch() {
      if (this.searchQuery) {
        this.$router.push({ path: `/search/${this.searchQuery}` });
      } else {
        console.log('Please enter a search term');
      }
    },
    debounceSearch() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.performSearch();
      }, 300);
    },
  },
};
</script>

<style scoped>
nav {
  transition: background-color 0.3s;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

li a {
  text-decoration: none;
  padding: 0.5rem 1rem;
  color: inherit;
}

li a:focus {
  outline: 2px dashed white;
  outline-offset: 2px;
}

/* Responsive Search Bar Alignment */
@media (max-width: 768px) {
  .hidden.md\:flex {
    display: none;
  }
}
</style>

