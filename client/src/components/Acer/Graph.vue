<template>
  <v-card
    color="white"
  >
    <v-card-title>
      <v-icon
        :color="checking ? 'red lighten-2' : 'indigo'"
        class="mr-5"
        size="64"
        @click="takePulse"
      >
        insert_chart
      </v-icon>
      <v-layout
        column
        align-start
      >
        <div class="caption grey--text">
          平均温度
        </div>
        <div>
          <span
            class="display-2 font-weight-black"
            v-text="avg || '—'"
          ></span>
          <strong v-if="avg">摄氏度</strong>
        </div>
      </v-layout>

      <v-spacer></v-spacer>

      <v-btn flat small><div class="caption grey--text">房间 : 210</div></v-btn>
    </v-card-title>

    <v-sheet color="transparent">
      <v-sparkline
        :key="String(avg)"
        :smooth="16"
        :gradient="['#f72047', '#ffd200', '#1feaea']"
        :line-width="3"
        :value="heartbeats"
        auto-draw
        stroke-linecap="round"
      ></v-sparkline>
    </v-sheet>
  </v-card>
</template>

<script>
  const exhale = ms =>
    new Promise(resolve => setTimeout(resolve, ms))

  export default {
    props:{
        roomId:String,
    },

    data: () => ({
      checking: false,
      heartbeats: []
    }),

    computed: {
      avg () {
        const sum = this.heartbeats.reduce((acc, cur) => acc + cur, 0)
        const length = this.heartbeats.length

        if (!sum && !length) return 0

        return Math.ceil(sum / length)
      }
    },

    created () {
      this.takePulse(false)
    },

    methods: {
      heartbeat () {
        return Math.ceil(Math.random() * (120 - 80) + 80)
      },
      async takePulse (inhale = true) {
        this.checking = true

        inhale && await exhale(1000)

        this.heartbeats = Array.from({ length: 20 }, this.heartbeat)

        this.checking = false
      }
    }
  }
</script>

