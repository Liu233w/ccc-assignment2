<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <GmapMap :options="mapConfig" :center="center" style="width: 500px; height: 300px">
          <GmapInfoWindow
              :options="infoOptions"
              :position="infoWindowPos"
              :opened="infoWinOpen"
              @closeclick="infoWinOpen=false"
              ref="infoWindow"
          />
<!--&lt;!&ndash;          <GmapMarker&ndash;&gt;-->
<!--&lt;!&ndash;              :key="index"&ndash;&gt;-->
<!--&lt;!&ndash;              v-for="(m, index) in markers"&ndash;&gt;-->
<!--&lt;!&ndash;              :position="m.position"&ndash;&gt;-->
<!--&lt;!&ndash;              :clickable="true"&ndash;&gt;-->
<!--&lt;!&ndash;              :draggable="true"&ndash;&gt;-->
<!--&lt;!&ndash;              @click="center=m.position"&ndash;&gt;-->
<!--&lt;!&ndash;          />&ndash;&gt;-->

        </GmapMap>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import GoogleMapLoader from "@/components/GoogleMapLoader";
// import GoogleMapMarker from "@/components/GoogleMapMarker";

export default {
  name: "Map",
  // components: {
  //   GoogleMapLoader,
  //   // GoogleMapMarker
  // },

  data() {
    return {
      markers: [
        {
          id: "a",
          position: {lat: 3, lng: 101}
        },
        {
          id: "b",
          position: {lat: 5, lng: 99}
        },
        {
          id: "c",
          position: {lat: 6, lng: 97}
        }
      ],

      // Gmap
      center: {
        lat: -37.840935,
        lng: 144.946457
      },

      //  Info Window
      infoOptions: {
        content: 'Find You!',
        //optional: offset infowindow so it visually sits nicely on top of our marker
        pixelOffset: {
          width: 0,
          height: -35
        }
      },
      infoWindowPos: null,
      infoWinOpen: false,


    }
  },

  computed: {
    mapToken() {
      return this.$store.state.googleMap.token
    },
    mapConfig() {
      return this.$store.state.googleMap.options
    }
  },

  methods: {

    getCurrentLocation() {
      console.log('1')
      if (navigator.geolocation) {
        console.log('geo')
        navigator.geolocation.getCurrentPosition(
            (position) => {
              this.infoWindowPos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
              };
              this.infoWinOpen = true;
            },
            () => {
              alert("Error: The Geolocation service failed.")
            }
        );
      } else {
        // Browser doesn't support Geolocation
        alert("Error: Your browser doesn't support geolocation.")
      }
    },
  },

  created() {
  },

  mounted() {

    this.getCurrentLocation()

  }

}
</script>

<style scoped>

</style>