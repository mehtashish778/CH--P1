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
      <div class="grid grid-cols-3 gap-4">
        <router-link to="/safety-now" class="no-underline text-black">
          <div class="bg-white p-6 rounded-lg shadow-lg transition-transform transform hover:scale-105 text-center h-48 flex items-center justify-center">
            <h1 class="text-2xl font-semibold">Safety Now</h1>
          </div>
        </router-link>
        <div class="bg-white p-6 rounded-lg shadow-lg transition-transform transform hover:scale-105 text-center h-48 flex items-center justify-center">
          <div>
            <h1 class="text-2xl font-semibold">Safety Pro</h1>
            <h2 class="text-lg font-semibold mt-2">(Upcoming features)</h2>
          </div>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-lg transition-transform transform hover:scale-105 text-center h-48 flex items-center justify-center">
          <div>
            <h1 class="text-2xl font-semibold">Safety Guru</h1>
            <h2 class="text-lg font-semibold mt-2">(Upcoming features)</h2>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomePage',
  setup() {
    return {};
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
