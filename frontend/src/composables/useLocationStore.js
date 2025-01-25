import { ref } from 'vue'

const selectedLocationProfile = ref(JSON.parse(localStorage.getItem('selectedLocationProfile')) || null)
const locationProfiles = ref(JSON.parse(localStorage.getItem('locationProfiles')) || [
  {
    id: 1,
    name: 'Current Location',
    location: 'Auto Detect',
    temperature: null,
    humidity: null
  },
  {
    id: 2,
    name: 'Chennai Lab',
    location: 'Chennai, India',
    temperature: 30,
    humidity: 75
  },
  {
    id: 3,
    name: 'Mumbai Facility',
    location: 'Mumbai, India',
    temperature: 28,
    humidity: 80
  }
])

export function useLocationStore() {
  const setSelectedLocation = (profile) => {
    selectedLocationProfile.value = profile
    localStorage.setItem('selectedLocationProfile', JSON.stringify(profile))
  }

  const getSelectedLocation = () => {
    return selectedLocationProfile.value
  }

  const clearSelectedLocation = () => {
    selectedLocationProfile.value = null
    localStorage.removeItem('selectedLocationProfile')
  }

  const getAllProfiles = () => {
    return locationProfiles.value
  }

  const addProfile = (profile) => {
    locationProfiles.value.push(profile)
    saveProfilesToStorage()
  }

  const updateProfile = (updatedProfile) => {
    const index = locationProfiles.value.findIndex(p => p.id === updatedProfile.id)
    if (index !== -1) {
      locationProfiles.value[index] = { ...updatedProfile }
      saveProfilesToStorage()
    }
  }

  const deleteProfile = (profileId) => {
    const index = locationProfiles.value.findIndex(p => p.id === profileId)
    if (index !== -1) {
      locationProfiles.value.splice(index, 1)
      if (selectedLocationProfile.value?.id === profileId) {
        clearSelectedLocation()
      }
      saveProfilesToStorage()
    }
  }

  const saveProfilesToStorage = () => {
    localStorage.setItem('locationProfiles', JSON.stringify(locationProfiles.value))
  }

  const fetchCurrentLocationData = async () => {
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Dummy data for current location
      const dummyLocations = [
        { city: 'Bangalore', country: 'India', temp: 27, hum: 65 },
        { city: 'Delhi', country: 'India', temp: 32, hum: 55 },
        { city: 'Hyderabad', country: 'India', temp: 29, hum: 70 }
      ];

      // Randomly select one location for demonstration
      const randomLocation = dummyLocations[Math.floor(Math.random() * dummyLocations.length)];

      const currentLocationProfile = {
        id: 1,
        name: 'Current Location',
        location: `${randomLocation.city}, ${randomLocation.country}`,
        temperature: randomLocation.temp,
        humidity: randomLocation.hum
      };

      // Update the current location profile in the profiles list
      const index = locationProfiles.value.findIndex(p => p.id === 1);
      if (index !== -1) {
        locationProfiles.value[index] = currentLocationProfile;
        saveProfilesToStorage();
      }

      return currentLocationProfile;
    } catch (error) {
      console.error('Error fetching current location data:', error);
      throw error;
    }
  };

  return {
    selectedLocationProfile,
    locationProfiles,
    setSelectedLocation,
    getSelectedLocation,
    clearSelectedLocation,
    getAllProfiles,
    addProfile,
    updateProfile,
    deleteProfile,
    saveProfilesToStorage,
    fetchCurrentLocationData
  }
} 