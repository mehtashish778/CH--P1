<template>
  <div class="flex flex-col h-screen">
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

    <main class="flex-grow p-4 mt-16">
      <!-- Mobile View Order Container -->
      <div class="block lg:hidden mb-4">
        <!-- Chemical Profile Card (Mobile - First) -->
        <div v-if="chemicalDetails" class="chemical-card mb-4 shadow-lg relative bg-white p-6 rounded-lg">
          <h2 class="chemical-name text-2xl font-semibold text-indigo-700 mb-4">{{ chemicalDetails["Chemical Name"] }}</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p class="cas-number text-indigo-600 mb-3">
                <i class="fas fa-vial mr-2"></i>
                <strong>CAS No:</strong> {{ chemicalDetails["CAS Number"] }}
              </p>
              <p class="common-names text-gray-600 mb-3">
                <i class="fas fa-tags mr-2"></i>
                <strong>Common Names:</strong> {{ chemicalDetails["Synonyms"].join(', ') }}
              </p>
            </div>
            <div>
              <!-- Icons Section -->
              <div class="flex items-center space-x-4 mb-3">
                <div class="flex items-center text-red-600">
                  <i class="fas fa-fire text-xl mr-2"></i>
                  <span class="font-semibold">Flammable</span>
                </div>
                <div class="flex items-center text-yellow-600">
                  <i class="fas fa-exclamation-triangle text-xl mr-2"></i>
                  <span class="font-semibold">Warning</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Weather Widget (Mobile - Second) -->
        <Weather class="weather-widget mb-4" />


        <!-- Recommendations Card (Mobile - Third) -->
        <div v-if="chemicalDetails" class="recommendations-card mb-4 shadow-lg relative bg-white p-6 rounded-lg border-l-4 border-red-500">
          <h3 class="text-xl font-bold text-red-600 mb-4">
            <i class="fas fa-exclamation-circle mr-2"></i>
            Important Recommendations
          </h3>
          
          <!-- Immediate Actions -->
          <div class="mb-4">
            <h4 class="text-lg font-semibold text-red-700 mb-2">
              <i class="fas fa-bolt mr-2"></i>
              Immediate Actions Required:
            </h4>
            <ul class="list-disc list-inside text-gray-700 space-y-2">
              <li v-if="isTemperatureAboveFlashpoint" class="text-red-600 font-medium">
                Temperature Warning: Current temperature is above flash point!
              </li>
              <li>Ensure proper ventilation in storage area</li>
              <li>Verify PPE availability before handling</li>
              <li>Check fire extinguisher accessibility</li>
            </ul>
          </div>

          <!-- Key Warnings -->
          <div class="mb-4">
            <h4 class="text-lg font-semibold text-yellow-600 mb-2">
              <i class="fas fa-exclamation-triangle mr-2"></i>
              Key Warnings:
            </h4>
            <ul class="list-disc list-inside text-gray-700 space-y-2">
              <li v-if="chemicalDetails.Flammability?.['Flammable/Explosive Concentration']">
                Flammability: {{ chemicalDetails.Flammability['Flammable/Explosive Concentration'] }}
              </li>
              <li v-if="chemicalDetails['Reactivity and Stability']?.['Conditions to Avoid']">
                Avoid: {{ chemicalDetails['Reactivity and Stability']['Conditions to Avoid'].join(', ') }}
              </li>
              <li v-if="chemicalDetails['Storage']?.['Source of Ignition Precautions']">
                {{ chemicalDetails['Storage']['Source of Ignition Precautions'] }}
              </li>
            </ul>
          </div>

          <!-- Required PPE Summary -->
          <div>
            <h4 class="text-lg font-semibold text-blue-600 mb-2">
              <i class="fas fa-shield-alt mr-2"></i>
              Required PPE:
            </h4>
            <div class="flex flex-wrap gap-3">
              <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                <i class="fas fa-glasses mr-2"></i>
                Eye Protection
              </span>
              <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                <i class="fas fa-hand-paper mr-2"></i>
                Gloves
              </span>
              <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                <i class="fas fa-tshirt mr-2"></i>
                Protective Clothing
              </span>
              <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                <i class="fas fa-head-side-mask mr-2"></i>
                Respiratory Protection
              </span>
            </div>
          </div>
        </div>

        <!-- Instructions Section (Mobile - Last) -->
        <div class="mt-4 bg-white rounded-lg shadow-lg p-4">
          <h3 class="text-lg font-bold text-center text-indigo-600 border-b-2 border-indigo-600 pb-2">Instructions</h3>
          <div class="tabs grid grid-cols-2 md:flex md:flex-nowrap mt-2 gap-2">
            <button @click="toggleInstruction('handling')" 
              :class="{
                'bg-indigo-600 text-white': expandedInstruction === 'handling',
                'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'handling'
              }" 
              class="tab-button transition-transform transform hover:scale-105">
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
            <h4 class="font-bold text-xl mb-4 text-gray-800 flex items-center justify-center border-b pb-2">
              <i :class="getInstructionIcon" class="mr-2"></i>
              {{ formatInstructionTitle(expandedInstruction) }} Guidelines
            </h4>
            <div v-if="expandedInstruction === 'handling'" class="handling-instruction">
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-hands-wash mr-2"></i>Safe Handling:
                </strong>
                <span>{{ chemicalDetails["Handling"]["Safe Handling"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-user-shield mr-2"></i>Hygiene Measures:
                </strong>
                <span>{{ chemicalDetails["Handling"]["Hygiene Measures"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-exclamation-circle mr-2"></i>Precautions:
                </strong>
                <ul class="list-disc list-inside text-gray-700">
                  <li v-for="precaution in chemicalDetails['Handling']['Precautions']" :key="precaution">
                    {{ precaution }}
                  </li>
                </ul>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-shield-alt mr-2"></i>Spill Protection:
                </strong>
                <span>{{ chemicalDetails["Handling"]["Spill Protection"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-fire-extinguisher mr-2"></i>Protection Against Fire and Explosion:
                </strong>
                <span>{{ chemicalDetails["Handling"]["Protection Against Fire and Explosion"] }}</span>
              </div>
            </div>


            <div v-if="expandedInstruction === 'storage'" class="storage-instruction">
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-thermometer-half mr-2"></i>Flash Point:
                </strong>
                <span>{{ chemicalDetails["Storage"]["Flash Point"] }}</span>
                <div v-if="isTemperatureAboveFlashpoint" class="mt-2 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                  <i class="fas fa-exclamation-triangle mr-2"></i>
                  <strong>Warning:</strong> Be careful! The current room temperature ({{ currentTemperature }}°C) is higher than the flash point.
                </div>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-warehouse mr-2"></i>Storage Conditions:
                </strong>
                <span>{{ chemicalDetails["Storage"]["Storage Conditions"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-ban mr-2"></i>Source of Ignition Precautions:
                </strong>
                <span>{{ chemicalDetails["Storage"]["Source of Ignition Precautions"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-vial mr-2"></i>Precautions:
                </strong>
                <span>{{ chemicalDetails["Storage"]["Precautions"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-check-circle mr-2"></i>Stability:
                </strong>
                <span>{{ chemicalDetails["Storage"]["Stability"] }}</span>
              </div>
            </div>
            <div v-if="expandedInstruction === 'ppe'" class="ppe-instruction">
              <div class="tabs">
                <!-- Tab Buttons -->
                <div class="tab-buttons flex">
                  <button
                    v-for="(tab, index) in ppeTabs"
                    :key="index"
                    :class="['tab-button', { active: activeTab === tab.key }]"
                    @click="activeTab = tab.key"
                  >
                    <i :class="tab.icon" class="mr-2"></i>{{ tab.label }}
                  </button>
                </div>
                <!-- Tab Content -->
                <div class="tab-content mt-4">
                  <div v-if="activeTab === 'eyeFace'" class="mb-4">
                    <strong class="block text-lg text-red-600">
                      <i class="fas fa-glasses mr-2"></i>Eye/Face Protection:
                    </strong>
                    <span>{{ chemicalDetails["Personal Protective Equipment"]["Eye/Face Protection"] }}</span>
                  </div>
                  <div v-if="activeTab === 'skin'" class="mb-4">
                    <strong class="block text-lg text-red-600">
                      <i class="fas fa-hand-paper mr-2"></i>Skin Protection:
                    </strong>
                    <ul class="list-disc list-inside text-gray-700">
                      <li><strong>Material:</strong> {{ chemicalDetails["Personal Protective Equipment"]["Skin Protection"]["Material"] }}</li>
                      <li><strong>Minimum Layer Thickness:</strong> {{ chemicalDetails["Personal Protective Equipment"]["Skin Protection"]["Minimum Layer Thickness"] }}</li>
                    </ul>
                  </div>
                  <div v-if="activeTab === 'body'" class="mb-4">
                    <strong class="block text-lg text-red-600">
                      <i class="fas fa-tshirt mr-2"></i>Body Protection:
                    </strong>
                    <span>{{ chemicalDetails["Personal Protective Equipment"]["Body Protection"] }}</span>
                  </div>
                  <div v-if="activeTab === 'respiratory'" class="mb-4">
                    <strong class="block text-lg text-red-600">
                      <i class="fas fa-head-side-mask mr-2"></i>Respiratory Protection:
                    </strong>
                    <span>{{ chemicalDetails["Personal Protective Equipment"]["Respiratory Protection"] }}</span>
                  </div>
                </div>
              </div>
            </div>



            <div v-if="expandedInstruction === 'flammability'" class="flammability-instruction">
              <div class="mb-4">
                <strong class="block text-lg text-orange-600">
                  <i class="fas fa-fire mr-2"></i>Flammable/Explosive Concentration:
                </strong>
                <span>{{ chemicalDetails["Flammability"]["Flammable/Explosive Concentration"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-orange-600">
                  <i class="fas fa-thermometer-three-quarters mr-2"></i>Flash Point:
                </strong>
                <span>{{ chemicalDetails["Flammability"]["Flash Point and Flammability"]["Flash Point"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-orange-600">
                  <i class="fas fa-temperature-high mr-2"></i>Flammability at Storage Temperature:
                </strong>
                <span>{{ chemicalDetails["Flammability"]["Flash Point and Flammability"]["Flammability at Storage Temperature"] }}</span>
              </div>
            </div>

            <div v-if="expandedInstruction === 'reactivityAndStability'" class="reactivity-stability-instruction">
              <div class="mb-4">
                <strong class="block text-lg text-yellow-600">
                  <i class="fas fa-check-circle mr-2"></i>Stability:
                </strong>
                <span>{{ chemicalDetails["Reactivity and Stability"]["Stability"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-yellow-600">
                  <i class="fas fa-exclamation-triangle mr-2"></i>Reactivity:
                </strong>
                <span>{{ chemicalDetails["Reactivity and Stability"]["Reactivity"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-yellow-600">
                  <i class="fas fa-ban mr-2"></i>Conditions to Avoid:
                </strong>
                <ul class="list-disc list-inside text-gray-700">
                  <li v-for="condition in chemicalDetails['Reactivity and Stability']['Conditions to Avoid']" :key="condition">
                    {{ condition }}
                  </li>
                </ul>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-yellow-600">
                  <i class="fas fa-times-circle mr-2"></i>Incompatible Materials:
                </strong>
                <ul class="list-disc list-inside text-gray-700">
                  <li v-for="material in chemicalDetails['Reactivity and Stability']['Incompatible Materials']" :key="material">
                    {{ material }}
                  </li>
                </ul>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-yellow-600">
                  <i class="fas fa-burn mr-2"></i>Decomposition Products:
                </strong>
                <span>{{ chemicalDetails["Reactivity and Stability"]["Decomposition Products"] }}</span>
              </div>
            </div>

            <div v-if="expandedInstruction === 'toxicity'" class="toxicity-instruction">
              <!-- Acute Toxicity Section -->
              <div class="mb-4" v-if="chemicalDetails?.['Toxic Release Measures']?.['Acute Toxicity']">
                <strong class="block text-lg text-red-600">
                  <i class="fas fa-skull-crossbones mr-2"></i>Acute Toxicity:
                </strong>
                <div class="ml-4">
                  <p v-if="chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']">
                    <strong>LC50:</strong> {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']['Value'] }}
                    ({{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']['Method'] }}, 
                    {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']['Species'] }}, 
                    {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']['Duration'] }})
                  </p>
                  <p v-if="chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50 Matrix Assessment']">
                    <strong>LC50 Assessment:</strong> {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50 Matrix Assessment'] }}
                  </p>
                  <p v-if="chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50']">
                    <strong>LD50:</strong> {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50']['Value'] }}
                    ({{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50']['Method'] }}, 
                    {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50']['Species'] }})
                  </p>
                  <p v-if="chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50 Matrix Assessment']">
                    <strong>LD50 Assessment:</strong> {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50 Matrix Assessment'] }}
                  </p>
                </div>
              </div>

              <!-- Chronic Toxicity Section -->
              <div class="mb-4" v-if="chemicalDetails?.['Toxic Release Measures']?.['Chronic Toxicity']">
                <strong class="block text-lg text-red-600">
                  <i class="fas fa-dna mr-2"></i>Chronic Toxicity:
                </strong>
                <div class="ml-4">
                  <p v-if="chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Germ Cell Mutagenicity']">
                    <strong>Germ Cell Mutagenicity:</strong> {{ chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Germ Cell Mutagenicity'] }}
                  </p>
                  <p v-if="chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Carcinogenicity']">
                    <strong>Carcinogenicity:</strong> {{ chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Carcinogenicity'] }}
                  </p>
                  <p v-if="chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Reproductive Toxicity']">
                    <strong>Reproductive Toxicity:</strong> {{ chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Reproductive Toxicity'] }}
                  </p>
                  <p v-if="chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Specific Target Organ Toxicity (Repeated Exposure)']">
                    <strong>Specific Target Organ Toxicity (Repeated Exposure):</strong> 
                    {{ chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Specific Target Organ Toxicity (Repeated Exposure)'] }}
                  </p>
                </div>
              </div>

              <!-- Possible Medical Effects Section -->
              <div class="mb-4" v-if="chemicalDetails?.['Toxic Release Measures']?.['Possible Medical Effects']">
                <strong class="block text-lg text-red-600">
                  <i class="fas fa-user-injured mr-2"></i>Possible Medical Effects:
                </strong>
                <div class="ml-4">
                  <p v-if="chemicalDetails['Toxic Release Measures']['Possible Medical Effects']['Acute Effects']">
                    <strong>Acute Effects:</strong> {{ chemicalDetails['Toxic Release Measures']['Possible Medical Effects']['Acute Effects'] }}
                  </p>
                  <p v-if="chemicalDetails['Toxic Release Measures']['Possible Medical Effects']['Chronic Effects']">
                    <strong>Chronic Effects:</strong> {{ chemicalDetails['Toxic Release Measures']['Possible Medical Effects']['Chronic Effects'] }}
                  </p>
                </div>
              </div>
            </div>

            <div v-if="expandedInstruction === 'fireExtinguisher'" class="fire-extinguisher-instruction">
              <div class="mb-4">
                <strong class="block text-lg text-red-600">
                  <i class="fas fa-fire-extinguisher mr-2"></i>Fire Extinguisher to be Used:
                </strong>
                <ul class="list-disc list-inside text-gray-700">
                  <li v-for="extinguisher in chemicalDetails['Fire Extinguisher']['Fire Extinguisher to be Used']" :key="extinguisher">
                    {{ extinguisher }}
                  </li>
                </ul>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-red-600">
                  <i class="fas fa-user-shield mr-2"></i>Precautions for Firefighters:
                </strong>
                <span>{{ chemicalDetails["Fire Extinguisher"]["Precautions for Firefighters"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-red-600">
                  <i class="fas fa-exclamation-circle mr-2"></i>Specific Precautions:
                </strong>
                <span>{{ chemicalDetails["Fire Extinguisher"]["Specific Precautions"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-red-600">
                  <i class="fas fa-ban mr-2"></i>Fire Extinguisher Never to be Used:
                </strong>
                <span>{{ chemicalDetails["Fire Extinguisher"]["Fire Extinguisher Never to be Used"] }}</span>
              </div>
            </div>

            <div v-if="expandedInstruction === 'firstAidMeasures'" class="first-aid-instruction">
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-file-medical-alt mr-2"></i>General:
                </strong>
                <span>{{ chemicalDetails["First Aid Measures"]["General"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-wind mr-2"></i>Inhalation:
                </strong>
                <span>{{ chemicalDetails["First Aid Measures"]["Inhalation"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-hand-holding-water mr-2"></i>Skin Contact:
                </strong>
                <span>{{ chemicalDetails["First Aid Measures"]["Skin Contact"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-eye-dropper mr-2"></i>Eye Contact:
                </strong>
                <span>{{ chemicalDetails["First Aid Measures"]["Eye Contact"] }}</span>
              </div>
              <div class="mb-4">
                <strong class="block text-lg text-indigo-600">
                  <i class="fas fa-prescription-bottle mr-2"></i>Ingestion:
                </strong>
                <span>{{ chemicalDetails["First Aid Measures"]["Ingestion"] }}</span>
              </div>
            </div>

            <p v-if="expandedInstruction === 'transportation'">
               {{ chemicalDetails["Transportation"] }}
            </p>
            <button @click="expandedInstruction = null" class="mt-2 text-red-500 hover:underline">Close</button>
          </div>
        </div>
      </div>

      <!-- Desktop View Container -->
      <div class="hidden lg:flex lg:flex-row gap-4">
        <!-- Left Column: Weather and Recommendations -->
        <div class="lg:w-[25%]">
          <!-- Weather Widget -->



            <div class="tabs flex flex-col gap-2">
              <button @click="toggleInstruction('handling')" 
                :class="{
                  'bg-indigo-600 text-white': expandedInstruction === 'handling',
                  'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'handling'
                }" 
                class="tab-button transition-transform transform hover:scale-105 p-2 rounded-lg flex items-center justify-center">
                <i class="fas fa-hand-holding mr-2"></i> Handling
              </button>
              <button @click="toggleInstruction('storage')" 
                :class="{
                  'bg-indigo-600 text-white': expandedInstruction === 'storage',
                  'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'storage'
                }"
                class="tab-button transition-transform transform hover:scale-105 p-2 rounded-lg flex items-center justify-center">
                <i class="fas fa-warehouse mr-2"></i> Storage
              </button>
              <button @click="toggleInstruction('ppe')" 
                :class="{
                  'bg-indigo-600 text-white': expandedInstruction === 'ppe',
                  'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'ppe'
                }"
                class="tab-button transition-transform transform hover:scale-105 p-2 rounded-lg flex items-center justify-center">
                <i class="fas fa-shield-alt mr-2"></i> PPE
              </button>
              <button @click="toggleInstruction('flammability')" 
                :class="{
                  'bg-indigo-600 text-white': expandedInstruction === 'flammability',
                  'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'flammability'
                }"
                class="tab-button transition-transform transform hover:scale-105 p-2 rounded-lg flex items-center justify-center">
                <i class="fas fa-fire mr-2"></i> Flammability
              </button>
              <button @click="toggleInstruction('toxicity')" 
                :class="{
                  'bg-indigo-600 text-white': expandedInstruction === 'toxicity',
                  'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'toxicity'
                }"
                class="tab-button transition-transform transform hover:scale-105 p-2 rounded-lg flex items-center justify-center">
                <i class="fas fa-skull-crossbones mr-2"></i> Toxicity
              </button>
              <button @click="toggleInstruction('fireExtinguisher')" 
                :class="{
                  'bg-indigo-600 text-white': expandedInstruction === 'fireExtinguisher',
                  'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'fireExtinguisher'
                }"
                class="tab-button transition-transform transform hover:scale-105 p-2 rounded-lg flex items-center justify-center">
                <i class="fas fa-fire-extinguisher mr-2"></i> Fire Extinguisher
              </button>
              <button @click="toggleInstruction('reactivityAndStability')" 
                :class="{
                  'bg-indigo-600 text-white': expandedInstruction === 'reactivityAndStability',
                  'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'reactivityAndStability'
                }"
                class="tab-button transition-transform transform hover:scale-105 p-2 rounded-lg flex items-center justify-center">
                <i class="fas fa-exclamation-triangle mr-2"></i> Reactivity and Stability
              </button>
              <button @click="toggleInstruction('firstAidMeasures')" 
                :class="{
                  'bg-indigo-600 text-white': expandedInstruction === 'firstAidMeasures',
                  'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'firstAidMeasures'
                }"
                class="tab-button transition-transform transform hover:scale-105 p-2 rounded-lg flex items-center justify-center">
                <i class="fas fa-plus-circle mr-2"></i> First Aid Measures
              </button>
              <button @click="toggleInstruction('transportation')" 
                :class="{
                  'bg-indigo-600 text-white': expandedInstruction === 'transportation',
                  'bg-gray-100 text-indigo-600 hover:bg-indigo-100': expandedInstruction !== 'transportation'
                }"
                class="tab-button transition-transform transform hover:scale-105 p-2 rounded-lg flex items-center justify-center">
                <i class="fas fa-truck mr-2"></i> Transportation
              </button>
            </div>



        </div>

        <!-- Right Column: Chemical Profile and Instructions -->
        <div class="lg:w-[75%] lg:overflow-y-auto lg:max-h-screen lg:sticky lg:top-0 lg:pb-8">
          <!-- Chemical Profile Card -->
          <div v-if="chemicalDetails" class="chemical-card mb-4 shadow-lg relative bg-white rounded-lg w-full">
            <div class="p-6 w-full">
              <h2 class="chemical-name text-2xl font-semibold text-indigo-700 mb-4">{{ chemicalDetails["Chemical Name"] }}</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p class="cas-number text-indigo-600 mb-3">
                    <i class="fas fa-vial mr-2"></i>
                    <strong>CAS No:</strong> {{ chemicalDetails["CAS Number"] }}
                  </p>
                  <p class="common-names text-gray-600 mb-3">
                    <i class="fas fa-tags mr-2"></i>
                    <strong>Common Names:</strong> {{ chemicalDetails["Synonyms"].join(', ') }}
                  </p>
                </div>
                <div>
                  <!-- Icons Section -->
                  <div class="flex items-center space-x-4 mb-3">
                    <div class="flex items-center text-red-600">
                      <i class="fas fa-fire text-xl mr-2"></i>
                      <span class="font-semibold">Flammable</span>
                    </div>
                    <div class="flex items-center text-yellow-600">
                      <i class="fas fa-exclamation-triangle text-xl mr-2"></i>
                      <span class="font-semibold">Warning</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Instructions Section -->
          <div class="mt-4 bg-white rounded-lg shadow-lg p-4">
            <h3 class="text-lg font-bold text-center text-indigo-600 border-b-2 border-indigo-600 pb-2">Instructions</h3>

            <!-- Expandable Instruction Details -->
            <div v-if="expandedInstruction" class="mt-4 p-4 bg-gray-100 rounded-lg border border-gray-300">
              <h4 class="font-bold text-xl mb-4 text-gray-800 flex items-center justify-center border-b pb-2">
                <i :class="getInstructionIcon" class="mr-2"></i>
                {{ formatInstructionTitle(expandedInstruction) }} Guidelines
              </h4>
              <div v-if="expandedInstruction === 'handling'" class="handling-instruction">
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-hands-wash mr-2"></i>Safe Handling:
                  </strong>
                  <span>{{ chemicalDetails["Handling"]["Safe Handling"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-user-shield mr-2"></i>Hygiene Measures:
                  </strong>
                  <span>{{ chemicalDetails["Handling"]["Hygiene Measures"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-exclamation-circle mr-2"></i>Precautions:
                  </strong>
                  <ul class="list-disc list-inside text-gray-700">
                    <li v-for="precaution in chemicalDetails['Handling']['Precautions']" :key="precaution">
                      {{ precaution }}
                    </li>
                  </ul>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-shield-alt mr-2"></i>Spill Protection:
                  </strong>
                  <span>{{ chemicalDetails["Handling"]["Spill Protection"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-fire-extinguisher mr-2"></i>Protection Against Fire and Explosion:
                  </strong>
                  <span>{{ chemicalDetails["Handling"]["Protection Against Fire and Explosion"] }}</span>
                </div>
              </div>


              <div v-if="expandedInstruction === 'storage'" class="storage-instruction">
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-thermometer-half mr-2"></i>Flash Point:
                  </strong>
                  <span>{{ chemicalDetails["Storage"]["Flash Point"] }}</span>
                  <div v-if="isTemperatureAboveFlashpoint" class="mt-2 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                    <i class="fas fa-exclamation-triangle mr-2"></i>
                    <strong>Warning:</strong> Be careful! The current room temperature ({{ currentTemperature }}°C) is higher than the flash point.
                  </div>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-warehouse mr-2"></i>Storage Conditions:
                  </strong>
                  <span>{{ chemicalDetails["Storage"]["Storage Conditions"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-ban mr-2"></i>Source of Ignition Precautions:
                  </strong>
                  <span>{{ chemicalDetails["Storage"]["Source of Ignition Precautions"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-vial mr-2"></i>Precautions:
                  </strong>
                  <span>{{ chemicalDetails["Storage"]["Precautions"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-check-circle mr-2"></i>Stability:
                  </strong>
                  <span>{{ chemicalDetails["Storage"]["Stability"] }}</span>
                </div>
              </div>
              <div v-if="expandedInstruction === 'ppe'" class="ppe-instruction">
                <div class="tabs">
                  <!-- Tab Buttons -->
                  <div class="tab-buttons flex">
                    <button
                      v-for="(tab, index) in ppeTabs"
                      :key="index"
                      :class="['tab-button', { active: activeTab === tab.key }]"
                      @click="activeTab = tab.key"
                    >
                      <i :class="tab.icon" class="mr-2"></i>{{ tab.label }}
                    </button>
                  </div>
                  <!-- Tab Content -->
                  <div class="tab-content mt-4">
                    <div v-if="activeTab === 'eyeFace'" class="mb-4">
                      <strong class="block text-lg text-red-600">
                        <i class="fas fa-glasses mr-2"></i>Eye/Face Protection:
                      </strong>
                      <span>{{ chemicalDetails["Personal Protective Equipment"]["Eye/Face Protection"] }}</span>
                    </div>
                    <div v-if="activeTab === 'skin'" class="mb-4">
                      <strong class="block text-lg text-red-600">
                        <i class="fas fa-hand-paper mr-2"></i>Skin Protection:
                      </strong>
                      <ul class="list-disc list-inside text-gray-700">
                        <li><strong>Material:</strong> {{ chemicalDetails["Personal Protective Equipment"]["Skin Protection"]["Material"] }}</li>
                        <li><strong>Minimum Layer Thickness:</strong> {{ chemicalDetails["Personal Protective Equipment"]["Skin Protection"]["Minimum Layer Thickness"] }}</li>
                      </ul>
                    </div>
                    <div v-if="activeTab === 'body'" class="mb-4">
                      <strong class="block text-lg text-red-600">
                        <i class="fas fa-tshirt mr-2"></i>Body Protection:
                      </strong>
                      <span>{{ chemicalDetails["Personal Protective Equipment"]["Body Protection"] }}</span>
                    </div>
                    <div v-if="activeTab === 'respiratory'" class="mb-4">
                      <strong class="block text-lg text-red-600">
                        <i class="fas fa-head-side-mask mr-2"></i>Respiratory Protection:
                      </strong>
                      <span>{{ chemicalDetails["Personal Protective Equipment"]["Respiratory Protection"] }}</span>
                    </div>
                  </div>
                </div>
              </div>



              <div v-if="expandedInstruction === 'flammability'" class="flammability-instruction">
                <div class="mb-4">
                  <strong class="block text-lg text-orange-600">
                    <i class="fas fa-fire mr-2"></i>Flammable/Explosive Concentration:
                  </strong>
                  <span>{{ chemicalDetails["Flammability"]["Flammable/Explosive Concentration"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-orange-600">
                    <i class="fas fa-thermometer-three-quarters mr-2"></i>Flash Point:
                  </strong>
                  <span>{{ chemicalDetails["Flammability"]["Flash Point and Flammability"]["Flash Point"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-orange-600">
                    <i class="fas fa-temperature-high mr-2"></i>Flammability at Storage Temperature:
                  </strong>
                  <span>{{ chemicalDetails["Flammability"]["Flash Point and Flammability"]["Flammability at Storage Temperature"] }}</span>
                </div>
              </div>

              <div v-if="expandedInstruction === 'reactivityAndStability'" class="reactivity-stability-instruction">
                <div class="mb-4">
                  <strong class="block text-lg text-yellow-600">
                    <i class="fas fa-check-circle mr-2"></i>Stability:
                  </strong>
                  <span>{{ chemicalDetails["Reactivity and Stability"]["Stability"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-yellow-600">
                    <i class="fas fa-exclamation-triangle mr-2"></i>Reactivity:
                  </strong>
                  <span>{{ chemicalDetails["Reactivity and Stability"]["Reactivity"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-yellow-600">
                    <i class="fas fa-ban mr-2"></i>Conditions to Avoid:
                  </strong>
                  <ul class="list-disc list-inside text-gray-700">
                    <li v-for="condition in chemicalDetails['Reactivity and Stability']['Conditions to Avoid']" :key="condition">
                      {{ condition }}
                    </li>
                  </ul>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-yellow-600">
                    <i class="fas fa-times-circle mr-2"></i>Incompatible Materials:
                  </strong>
                  <ul class="list-disc list-inside text-gray-700">
                    <li v-for="material in chemicalDetails['Reactivity and Stability']['Incompatible Materials']" :key="material">
                      {{ material }}
                    </li>
                  </ul>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-yellow-600">
                    <i class="fas fa-burn mr-2"></i>Decomposition Products:
                  </strong>
                  <span>{{ chemicalDetails["Reactivity and Stability"]["Decomposition Products"] }}</span>
                </div>
              </div>

              <div v-if="expandedInstruction === 'toxicity'" class="toxicity-instruction">
                <!-- Acute Toxicity Section -->
                <div class="mb-4" v-if="chemicalDetails?.['Toxic Release Measures']?.['Acute Toxicity']">
                  <strong class="block text-lg text-red-600">
                    <i class="fas fa-skull-crossbones mr-2"></i>Acute Toxicity:
                  </strong>
                  <div class="ml-4">
                    <p v-if="chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']">
                      <strong>LC50:</strong> {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']['Value'] }}
                      ({{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']['Method'] }}, 
                      {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']['Species'] }}, 
                      {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50']['Duration'] }})
                    </p>
                    <p v-if="chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50 Matrix Assessment']">
                      <strong>LC50 Assessment:</strong> {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LC50 Matrix Assessment'] }}
                    </p>
                    <p v-if="chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50']">
                      <strong>LD50:</strong> {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50']['Value'] }}
                      ({{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50']['Method'] }}, 
                      {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50']['Species'] }})
                    </p>
                    <p v-if="chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50 Matrix Assessment']">
                      <strong>LD50 Assessment:</strong> {{ chemicalDetails['Toxic Release Measures']['Acute Toxicity']['LD50 Matrix Assessment'] }}
                    </p>
                  </div>
                </div>

                <!-- Chronic Toxicity Section -->
                <div class="mb-4" v-if="chemicalDetails?.['Toxic Release Measures']?.['Chronic Toxicity']">
                  <strong class="block text-lg text-red-600">
                    <i class="fas fa-dna mr-2"></i>Chronic Toxicity:
                  </strong>
                  <div class="ml-4">
                    <p v-if="chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Germ Cell Mutagenicity']">
                      <strong>Germ Cell Mutagenicity:</strong> {{ chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Germ Cell Mutagenicity'] }}
                    </p>
                    <p v-if="chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Carcinogenicity']">
                      <strong>Carcinogenicity:</strong> {{ chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Carcinogenicity'] }}
                    </p>
                    <p v-if="chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Reproductive Toxicity']">
                      <strong>Reproductive Toxicity:</strong> {{ chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Reproductive Toxicity'] }}
                    </p>
                    <p v-if="chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Specific Target Organ Toxicity (Repeated Exposure)']">
                      <strong>Specific Target Organ Toxicity (Repeated Exposure):</strong> 
                      {{ chemicalDetails['Toxic Release Measures']['Chronic Toxicity']['Specific Target Organ Toxicity (Repeated Exposure)'] }}
                    </p>
                  </div>
                </div>

                <!-- Possible Medical Effects Section -->
                <div class="mb-4" v-if="chemicalDetails?.['Toxic Release Measures']?.['Possible Medical Effects']">
                  <strong class="block text-lg text-red-600">
                    <i class="fas fa-user-injured mr-2"></i>Possible Medical Effects:
                  </strong>
                  <div class="ml-4">
                    <p v-if="chemicalDetails['Toxic Release Measures']['Possible Medical Effects']['Acute Effects']">
                      <strong>Acute Effects:</strong> {{ chemicalDetails['Toxic Release Measures']['Possible Medical Effects']['Acute Effects'] }}
                    </p>
                    <p v-if="chemicalDetails['Toxic Release Measures']['Possible Medical Effects']['Chronic Effects']">
                      <strong>Chronic Effects:</strong> {{ chemicalDetails['Toxic Release Measures']['Possible Medical Effects']['Chronic Effects'] }}
                    </p>
                  </div>
                </div>
              </div>

              <div v-if="expandedInstruction === 'fireExtinguisher'" class="fire-extinguisher-instruction">
                <div class="mb-4">
                  <strong class="block text-lg text-red-600">
                    <i class="fas fa-fire-extinguisher mr-2"></i>Fire Extinguisher to be Used:
                  </strong>
                  <ul class="list-disc list-inside text-gray-700">
                    <li v-for="extinguisher in chemicalDetails['Fire Extinguisher']['Fire Extinguisher to be Used']" :key="extinguisher">
                      {{ extinguisher }}
                    </li>
                  </ul>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-red-600">
                    <i class="fas fa-user-shield mr-2"></i>Precautions for Firefighters:
                  </strong>
                  <span>{{ chemicalDetails["Fire Extinguisher"]["Precautions for Firefighters"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-red-600">
                    <i class="fas fa-exclamation-circle mr-2"></i>Specific Precautions:
                  </strong>
                  <span>{{ chemicalDetails["Fire Extinguisher"]["Specific Precautions"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-red-600">
                    <i class="fas fa-ban mr-2"></i>Fire Extinguisher Never to be Used:
                  </strong>
                  <span>{{ chemicalDetails["Fire Extinguisher"]["Fire Extinguisher Never to be Used"] }}</span>
                </div>
              </div>

              <div v-if="expandedInstruction === 'firstAidMeasures'" class="first-aid-instruction">
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-file-medical-alt mr-2"></i>General:
                  </strong>
                  <span>{{ chemicalDetails["First Aid Measures"]["General"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-wind mr-2"></i>Inhalation:
                  </strong>
                  <span>{{ chemicalDetails["First Aid Measures"]["Inhalation"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-hand-holding-water mr-2"></i>Skin Contact:
                  </strong>
                  <span>{{ chemicalDetails["First Aid Measures"]["Skin Contact"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-eye-dropper mr-2"></i>Eye Contact:
                  </strong>
                  <span>{{ chemicalDetails["First Aid Measures"]["Eye Contact"] }}</span>
                </div>
                <div class="mb-4">
                  <strong class="block text-lg text-indigo-600">
                    <i class="fas fa-prescription-bottle mr-2"></i>Ingestion:
                  </strong>
                  <span>{{ chemicalDetails["First Aid Measures"]["Ingestion"] }}</span>
                </div>
              </div>

              <p v-if="expandedInstruction === 'transportation'">
                 {{ chemicalDetails["Transportation"] }}
              </p>
              <button @click="expandedInstruction = null" class="mt-2 text-red-500 hover:underline">Close</button>
            </div>


            

          <!-- Recommendations Card -->
          <div v-if="chemicalDetails" class="recommendations-card mb-4 shadow-lg relative bg-white p-6 rounded-lg border-l-4 border-red-500">
            <h3 class="text-xl font-bold text-red-600 mb-4">
              <i class="fas fa-exclamation-circle mr-2"></i>
              Important Recommendations
            </h3>
            
            <!-- Immediate Actions -->
            <div class="mb-4">
              <h4 class="text-lg font-semibold text-red-700 mb-2">
                <i class="fas fa-bolt mr-2"></i>
                Immediate Actions Required:
              </h4>
              <ul class="list-disc list-inside text-gray-700 space-y-2">
                <li v-if="isTemperatureAboveFlashpoint" class="text-red-600 font-medium">
                  Temperature Warning: Current temperature is above flash point!
                </li>
                <li>Ensure proper ventilation in storage area</li>
                <li>Verify PPE availability before handling</li>
                <li>Check fire extinguisher accessibility</li>
              </ul>
            </div>

            <!-- Key Warnings -->
            <div class="mb-4">
              <h4 class="text-lg font-semibold text-yellow-600 mb-2">
                <i class="fas fa-exclamation-triangle mr-2"></i>
                Key Warnings:
              </h4>
              <ul class="list-disc list-inside text-gray-700 space-y-2">
                <li v-if="chemicalDetails.Flammability?.['Flammable/Explosive Concentration']">
                  Flammability: {{ chemicalDetails.Flammability['Flammable/Explosive Concentration'] }}
                </li>
                <li v-if="chemicalDetails['Reactivity and Stability']?.['Conditions to Avoid']">
                  Avoid: {{ chemicalDetails['Reactivity and Stability']['Conditions to Avoid'].join(', ') }}
                </li>
                <li v-if="chemicalDetails['Storage']?.['Source of Ignition Precautions']">
                  {{ chemicalDetails['Storage']['Source of Ignition Precautions'] }}
                </li>
              </ul>
            </div>

            <!-- Required PPE Summary -->
              <div>
                <h4 class="text-lg font-semibold text-blue-600 mb-2">
                  <i class="fas fa-shield-alt mr-2"></i>
                  Required PPE:
                </h4>
                <div class="flex flex-wrap gap-3">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    <i class="fas fa-glasses mr-2"></i>
                    Eye Protection
                  </span>
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    <i class="fas fa-hand-paper mr-2"></i>
                    Gloves
                  </span>
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    <i class="fas fa-tshirt mr-2"></i>
                    Protective Clothing
                  </span>
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    <i class="fas fa-head-side-mask mr-2"></i>
                    Respiratory Protection
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import Weather from './Weather.vue';
import 'font-awesome/css/font-awesome.css';

export default {
  name: 'ChemicalProfileDEE',
  components: {
    Weather
  },
  data() {
    return {
      isMenuOpen: false,
      expandedInstruction: null,
      chemicalDetails: null,
      searchQuery: '',
      chemicalAmount: 1, // Default amount
      activeTab: 'eyeFace', // Default active tab
      ppeTabs: [
        { key: 'eyeFace', label: 'Eye/Face Protection', icon: 'fas fa-glasses' },
        { key: 'skin', label: 'Skin Protection', icon: 'fas fa-hand-paper' },
        { key: 'body', label: 'Body Protection', icon: 'fas fa-tshirt' },
        { key: 'respiratory', label: 'Respiratory Protection', icon: 'fas fa-head-side-mask' },
      ],

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
        const response = await axios.get('http://10.17.18.109:8000/chemical', {
          params: { CAS_number: '60-29-7' }
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
    },
    formatInstructionTitle(instruction) {
      return instruction.charAt(0).toUpperCase() + instruction.slice(1);
    },
    get getInstructionIcon() {
      const icons = {
        handling: 'fas fa-hand-holding',
        storage: 'fas fa-warehouse',
        ppe: 'fas fa-shield-alt',
        flammability: 'fas fa-fire',
        toxicity: 'fas fa-skull-crossbones',
        fireExtinguisher: 'fas fa-fire-extinguisher',
        reactivityAndStability: 'fas fa-exclamation-triangle',
        firstAidMeasures: 'fas fa-plus-circle',
        transportation: 'fas fa-truck'
      };
      return icons[this.expandedInstruction] || 'fas fa-info-circle';
    }
  },
  props: {
  },
  head: {
    link: [
      { rel: 'stylesheet', href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css' }
    ]
  },
  computed: {
    currentTemperature() {
      // Get temperature from localStorage (set by Weather component)
      return parseFloat(localStorage.getItem('temperature')) || 0;
    },
    isTemperatureAboveFlashpoint() {
      if (!this.chemicalDetails?.Storage?.["Flash Point"]) return false;
      
      // Extract numeric value from flash point string (assuming format like "20°C")
      const flashPointMatch = this.chemicalDetails.Storage["Flash Point"].match(/(-?\d+)/);
      if (!flashPointMatch) return false;
      
      const flashPoint = parseFloat(flashPointMatch[0]);
      return this.currentTemperature > flashPoint;
    }
  }
};
</script>

<style>
.chemical-card {
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.chemical-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Ensure consistent padding and spacing */
.chemical-card, .instructions-section {
  padding: 1.5rem;
  margin-bottom: 1rem;
}

/* Grid layout for better organization */
.grid {
  display: grid;
  gap: 1.5rem;
}

@media (min-width: 1024px) {
  .chemical-card {
    height: fit-content;
    min-height: 200px; /* Adjust this value based on your content */
  }
}

/* Responsive adjustments */
@media (max-width: 1023px) {
  .weather-widget {
    position: static;
    margin-bottom: 1rem;
  }
}

/* Update existing styles */
@media (min-width: 1024px) {
  .lg\:w-\[75%\] {
    width: 75%;
    max-width: 75%;
  }
  
  .lg\:w-\[25%\] {
    width: 25%;
    max-width: 25%;
  }

  .chemical-card {
    width: 100%;
    max-width: 100%;
  }
}
</style>
