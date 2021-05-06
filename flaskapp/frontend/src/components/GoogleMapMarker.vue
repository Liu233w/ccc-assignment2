<template>
  <div ref="mapMarker"></div>
</template>

<script>
import { POINT_MARKER_ICON_CONFIG } from "@/utils/mapSettings";

export default {

  name: "MapMarker",
  props: {
    map: Object,
    marker: Object,
    google: Object
  },

  mounted() {
    const { Marker } = this.google.maps;

    new Marker({
      position: this.marker.position,
      marker: this.marker,
      map: this.map,
      icon: POINT_MARKER_ICON_CONFIG
    });
  }
}
</script>

<style scoped>

</style>