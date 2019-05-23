<template>
    <v-card class="mt-2" style="border:1px solid rgba(30,144,255,0.5);border-radius:30px;" >
    <v-card-title primary-title>
        <div>      
        <div class="blue--text">
            <i class="material-icons" style="font-size: 24px;position:relative;top:5px;">signal_cellular_alt</i>
            <font size="4"><strong>{{info.nameStr}}</strong></font>
        </div>
        <span class="grey--text">状况良好</span>
        </div>
    </v-card-title>

    <v-card-text>
        <v-layout row wrap>
            <v-flex xs12>
                <v-toolbar color="rgba(0,0,0,0)" flat style="border:1px solid #DCDCDC;border-radius:10px;">
                    <v-toolbar-title class="blue--text" >
                        <font size="5">{{info.maxTmp}}℃/{{info.minTmp}}℃</font>
                    </v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn color="rgba(144,238,144,0.5)">
                        <font color="#32CD32" style="font-weight:580;">{{info.serviceState}}</font>
                    </v-btn>
                </v-toolbar>
            </v-flex>
            <v-flex xs12 class="mt-3">
                <v-layout row wrap align-center justify-center>
                    <v-flex xs3>
                        <v-btn color="info" v-if="info.isCold">制冷</v-btn>
                        <v-btn color="error" v-else>制热</v-btn>
                    </v-flex>

                    <!-- 竖线自适应 -->
                    <v-divider vertical v-if="$vuetify.breakpoint.md || $vuetify.breakpoint.lg"></v-divider>
                    <v-flex xs1></v-flex>
                    <!-- <v-spacer></v-spacer> -->

                    <v-flex xs3>
                        <div class="headline"><strong><font color="#1E90FF" size="5">{{info.percent}}%</font></strong></div>
                    </v-flex>
                    <v-flex xs3>
                        <div class="headline"><strong><font color="red" size="5">{{info.fee}}元</font></strong></div>
                    </v-flex>
                </v-layout>
            </v-flex>
        </v-layout>
    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions>
        <v-btn color="rgba(135,206,250,0.5)" class="ml-5">
            <font color="#1E90FF" style="font-weight:580;">{{info.info}}</font>
        </v-btn>
        <v-spacer></v-spacer>

        <v-menu offset-y>
            <template v-slot:activator="{ on }">
              <v-btn
                outline 
                color="primary"
                dark
                v-on="on"
              >
                {{currentOpt}}
                <v-icon>expand_more</v-icon>
              </v-btn>
            </template>

            <v-list>
              <v-list-tile
                v-for="(item, i) in opts"
                :key="i"
              >
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile>
            </v-list>
        </v-menu>


        <v-btn icon @click="show = !show">
        <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
        </v-btn>
    </v-card-actions>

    <v-slide-y-transition>
        <v-card-text v-show="show">
        可能的额外信息
        </v-card-text>
    </v-slide-y-transition>
    </v-card>

</template>


<script>

  export default {
    data: () => ({
      show:false,
      currentOpt:"操作",
      opts: [
        { title: '操作1' },
        { title: '操作2' },
        { title: '操作3' },
      ]
    }),
    props:{
        info:Map,
    },


    components: {
      
    }
  }

</script>

<style scoped>
    @import url("https://fonts.googleapis.com/icon?family=Material+Icons");
    .border{
        background-color: azure
    }
</style>
