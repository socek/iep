<template>
    <table>
        <thead>
            <tr>
                <td>#</td>
                <td>UUID</td>
                <td>Name</td>
                <td>Description</td>
            </tr>
        </thead>
        <tbody>
            <tr v-for="panel in panels">
                <td>#</td>
                <td>{{ panel.uid }}</td>
                <td>{{ panel.name }}</td>
                <td>{{ panel.description }}</td>
            </tr>
        </tbody>
    </table>
</template>
<script>
import panelResource from '@/panels/resource'

export default {
  data () {
    return {
      panels: [],
      resource: panelResource(this)
    }
  },
  mounted () {
    this.resource.list().then((response) => {
      this.panels = response.body
    })
  }
}
</script>
