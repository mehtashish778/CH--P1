<template>
  <div class="search-bar">
    <input
      type="text"
      :value="searchQuery"
      :placeholder="placeholder"
      class="flex-1 border border-gray-400 rounded-l-lg p-2 shadow-sm focus:ring-2 focus:ring-blue-600 focus:border-blue-600 transition duration-200"
      @input="handleInput"
    />
    <button
      class="bg-blue-700 text-white rounded-r-lg px-4 py-2 hover:bg-blue-800 shadow-md focus:outline-none focus:ring-2 focus:ring-blue-600 transition duration-200"
      @click="performSearch"
    >
      Search
    </button>
  </div>
</template>

<script>
export default {
  props: {
    placeholder: {
      type: String,
      default: 'Search Chemical Name',
    },
    searchQuery: {
      type: String,
      required: true,
    },
    performSearch: {
      type: Function,
      required: true,
    },
    debounceTimeout: {
      type: Number,
      default: 300,
    },
  },
  data() {
    return {
      debounceTimer: null,
    };
  },
  methods: {
    handleInput(event) {
      this.$emit('update:searchQuery', event.target.value);
      this.debounceSearch();
    },
    debounceSearch() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.performSearch();
      }, this.debounceTimeout);
    },
  },
};
</script>

<style scoped>
.search-bar {
  display: flex;
}
</style> 