<script>
import Loading from "./views/Loading.vue";

export default {
  name: "App",
  components: {
    Loading,
  },
  data() {
    return { isLoading: true };
  },
  mounted() {
    setTimeout(() => {
      this.isLoading = false;
    }, 3000);
  },
};
</script>

<template>
  <Loading v-if="isLoading" />
  <div class="">
    <router-view v-if="!isLoading" />
  </div>
</template>

<style></style>
