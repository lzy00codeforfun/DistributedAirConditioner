<template>
  <div id="app">
    <v-app id="inspire">
      <v-container fluid grid-list-md>
        <v-layout row wrap>
          <v-flex xs10 offset-xs1>

            <v-toolbar>
              <v-toolbar-title class="headline">
                <span>空调管理</span>
              </v-toolbar-title>
              <v-btn color="success" class="ml-4">夏季模式-正在执行</v-btn>
            </v-toolbar>

          </v-flex>
          <v-flex xs10 offset-xs1>

            <v-layout row wrap>
              
              <v-flex  xs12 sm12 md6>
                <v-layout row wrap>
                  <v-flex  xs12>
                    <!-- Graph page -->
                    <Graph></Graph>
                  </v-flex>
                  <v-flex  xs12>
                    <!-- Opt page -->
                    <Opt></Opt>
                  </v-flex>
                  <v-flex  xs12>
                    <!-- Info page -->
                    <Info></Info>
                  </v-flex>
                </v-layout>
              </v-flex>

              <v-flex  xs12 sm12 md6>
                <List></List>
              </v-flex>

            </v-layout>
          
          </v-flex>
        </v-layout>
       
      
      </v-container>
    </v-app>
  </div>
</template>

<script>
  import Graph from "../components/Acer/Graph.vue";
  import Opt from "../components/Acer/Opt.vue";
  import Info from "../components/Acer/Info.vue";
  import List from "../components/Acer/List.vue";
  export default {
    data: () => ({
      
    }),

    components: {
      Graph,Opt,Info,List
    }
  }

</script>