<template>
    <v-card color="white">             
        <v-layout row wrap>
        <v-flex d-flex xs12>
            <v-layout row wrap justify-center class="pt-3">  
            
            <v-flex d-flex xs12 sm12 md5>
  
                <v-layout row wrap>                            
                <v-flex d-flex xs6 sm6 md6>
                    <p class="text-xs-right">
                        <v-icon color='red darken-2' size="75">
                            date_range
                        </v-icon>
                    </p>
                </v-flex>                               
                <v-flex d-flex xs6 sm6 md6>
                    <v-layout align-start justify-center column fill-height>
                        <div class="headline"><strong><font color="red" size="5" class="pl-3">50</font></strong></div>
                        <div class="headline"><strong><font color="grey" size="3">挂起对象</font></strong></div>
                    </v-layout>
                </v-flex>
                </v-layout>
 
            </v-flex>
            
            <!-- 竖线自适应 -->
            <v-divider vertical v-if="$vuetify.breakpoint.md || $vuetify.breakpoint.lg"></v-divider>

            <v-flex d-flex xs12 sm12 md5>
                <v-layout row wrap>                               
                <v-flex d-flex xs6 sm6 md6>
                    <p class="text-xs-right">
                        <v-icon color='blue darken-2' size="75">
                            playlist_add_check
                        </v-icon>
                    </p>
                </v-flex>                               
                <v-flex d-flex xs6 sm6 md6>
                    <v-layout align-start justify-center column fill-height>
                        <div class="headline"><strong><font color="blue" size="5" class="pl-3">20</font></strong></div>
                        <div class="headline"><strong><font color="grey" size="3">服务对象</font></strong></div>
                    </v-layout>
                </v-flex>
                </v-layout>
            </v-flex>


            </v-layout>
        </v-flex>
        <v-flex d-flex xs12 class="px-3">
            <v-layout row wrap>
                <v-flex d-flex xs12 sm12 md6>
                <v-btn block depressed large color="success">
                    <v-icon>loop</v-icon>
                    <strong>&nbsp;重置当前模式/关机</strong>
                </v-btn>
                </v-flex>
                <v-flex d-flex xs12 sm12 md6>
                <v-btn block depressed large color="info">
                    <v-icon>arrow_upward</v-icon>
                    <strong>更新/开启当前模式</strong>
                </v-btn>
                </v-flex>
            </v-layout>
        </v-flex>
        </v-layout>

    </v-card>
</template>

<script>

  export default {
    data: () => ({
      
    }),

    components: {
      
    }
  }

</script>
