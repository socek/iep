<template>
  <div class="button-wrapper">
    <b-btn v-if="showButton" size="sm" :variant="variant" @click="showModal" v-b-tooltip.hover :title="title">
      <slot name="anhor"></slot>
    </b-btn>

    <b-modal ref="modal" :size="size" :title="title" hide-footer>
      <ccform ref="form" v-model="value" @submit="$emit('submit', value)" @cancel="$refs.modal.hide()" v-show="!isBusy">
        <slot name="content"></slot>
      </ccform>
      <div v-show="isBusy" class="modal-spiner">
        <icon name="sync" scale="2" spin></icon>
      </div>
    </b-modal>
  </div>
</template>

<script>
  export default {
    props: {
      title: String,
      variant: {
        type: String,
        default: "outline-primary"
      },
      fetchContent: {
        default: false
      },
      size: {
        default: "md"
      },
      value: {
        type: Object,
        required: true
      },
      showButton: {
        type: Boolean,
        default: true
      }
    },
    data () {
      return {
        isBusy: true,
        withLoading: this.fetchContent && true
      }
    },
    methods: {
      showModal (modal) {
        this.isBusy = this.withLoading
        this.$refs.modal.show()
        if (this.fetchContent) {
          this.fetchContent().then((response) => {
            this.value.setDefaults(response.body)
            this.isBusy = false
            this.$emit("afterFetchContent", response.body)
          })
        } else {
          this.value.reset()
        }
      },
      hide () { this.$refs.modal.hide() }
    }
  }
</script>

<style scoped>
  .modal-spiner {
    text-align: center;
  }
  .save {
    float: left;
  }
  .cancel {
    float: right;
  }
  .button-wrapper {
    float: left;
    padding-left: 5px;
  }
</style>
