<template>
  <div>
    <v-container fluid>
      <v-layout row wrap>
        <v-flex xs10 offset-xs1>
          <v-layout row wrap>

            <v-flex xs12 sm12 md12>
              <v-toolbar>
                <v-toolbar-title class="headline">
                  <span>报表查看</span>
                </v-toolbar-title>
              </v-toolbar>
            </v-flex>

            <v-flex xs12 sm12 md12 class="mt-2">
              <v-tabs v-model="active" color="cyan" dark slider-color="yellow" height=50>
                <v-tab v-for="i in sumType.length" :key="i" ripple >
                  {{sumType[i-1]}}
                </v-tab>
                <v-tab-item v-for="n in 4" :key="n">
                  <v-card flat>

                    <v-flex xs12 sm12 md12>
                      <v-layout row wrap>
                        <v-flex xs12 sm12 md1 class="mt-3 ml-1">
                          <span> <font color="black"  style="font-size:15px;">所属楼层:</font></span>
                        </v-flex>
                        <v-flex xs12 sm12 md10>
                          <v-btn v-for="i in sumLevel.length" :key= i :color="currentLevel==i?'info':'white'" @click="currentLevel=i">{{sumLevel[i-1]}}</v-btn>
                        </v-flex>
                      </v-layout>              
                    </v-flex>

                    <v-flex xs12 sm12 md12>     
                      <v-btn color="success" round><i class="material-icons">get_app</i>一键导出全部</v-btn>
                    </v-flex>

                    <v-flex xs12 sm12 md12 >
                      <v-layout row wrap>
                        <v-flex xs12 sm12 md4 v-for="i in items.length" :key= i>
                          <ListItem :info=items[i-1]></ListItem>
                        </v-flex>
                      </v-layout>
                    </v-flex>

                  </v-card>
                </v-tab-item>
              </v-tabs>
            </v-flex>

            
            
          </v-layout>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
  import ListItem from "../components/Manager/ListItem.vue";
  export default {
    
    data: () => ({
      sumType:["日报","周报","月报","年报"],
      sumLevel:["全部","一层","二层","三层","四层"],
      currentLevel:1,
      active: null,
      

      items:[
        {
          nameStr:"一层101",
          sumFee:23,
          sumTime:24,
          numOnOff:2,
          numTemper:10,
          numAir:5,
          numDispatch:5,
          numSummary:3,
        },
        {
          nameStr:"二层201",
          sumFee:50,
          sumTime:24,
          numOnOff:22,
          numTemper:50,
          numAir:6,
          numDispatch:5,
          numSummary:3,
        },
        {
          nameStr:"一层101",
          sumFee:83,
          sumTime:24,
          numOnOff:22,
          numTemper:10,
          numAir:9,
          numDispatch:15,
          numSummary:33,
        },
        {
          nameStr:"三层101",
          sumFee:823,
          sumTime:24,
          numOnOff:232,
          numTemper:50,
          numAir:9,
          numDispatch:25,
          numSummary:33,
        },
        {
          nameStr:"二层201",
          sumFee:823,
          sumTime:24,
          numOnOff:82,
          numTemper:130,
          numAir:92,
          numDispatch:215,
          numSummary:34,
        },
      ]
    }),

    components: {
      ListItem
    },
    methods:{

      
    }
  }

</script>
<style scoped>
  @import url("https://fonts.googleapis.com/icon?family=Material+Icons");
</style>

