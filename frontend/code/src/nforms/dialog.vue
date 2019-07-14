<template>
  <div class="button-wrapper">
    <b-btn v-if="showButton" size="sm" :variant="variant" @click="showModal" v-b-tooltip.hover :title="title">
      <slot></slot>
    </b-btn>

    <b-modal ref="modal" :size="size" :title="title" hide-footer>
      <vue-form-generator :schema="schema" :model="value" ref="nform" :options="options"></vue-form-generator>

      <input type="submit" value="Zapisz" @click="submitHandler" class="btn btn-primary">
      <b-btn variant="danger" @click="hide">Anuluj</b-btn>

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
      schema: {
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
        withLoading: this.fetchContent && true,
        options: {
          validateAfterChanged: true
        }
      }
    },
    methods: {
      showModal (modal) {
        this.isBusy = this.withLoading
        this.$refs.modal.show()
        if (this.fetchContent) {
          this.fetchContent().then((response) => {
            this.$emit("input", response.body)
            this.isBusy = false
          })
        } else {
          this.$emit("input", {})
        }
      },
      hide () { this.$refs.modal.hide() },
      submitHandler () {
        if (this.$refs.nform.validate()) {
          this.$emit("submit", this, this.value)
        }
      }
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
