<template>
  <div>
    <div class="google-map" ref="googleMap"></div>
    <template v-if="this.map">
      <slot
          :google="google"
          :map="map"
      />
    </template>
  </div>
</template>

<script>
import { Loader } from '@googlemaps/js-api-loader';

export default {
  props: {
    mapConfig: Object,
    apiKey: String,
  },

  data() {
    return {
      google: null,
      map: null,
      promise: null
    }
  },

  async mounted() {
    console.log('api key', this.$store.state.googleMap.token)

    const loader = new Loader({
      apiKey: this.apiKey,
    });

    await loader.load()
    this.initializeMap()
  },

  methods: {
    initializeMap() {
      const mapContainer = this.$refs.googleMap
      // this.google = window.google
      window.googleMp = new window.google.maps.Map(
          mapContainer, this.mapConfig
      )
    }
  }
}
</script>

<style scoped>

</style>