<template>
  <v-layout justify-center>
    <v-flex xs12>
      <v-card>
        <v-card-title class="cyan lighten-1">
          <span class="headline white--text">模式信息</span>
          <v-spacer></v-spacer>
          <v-btn dark icon>
            <v-icon>edit</v-icon>
          </v-btn>
        </v-card-title>

        <v-list>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>text_fields</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title>温度范围</v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action>

              <v-icon>chat</v-icon>
            </v-list-tile-action>
          </v-list-tile>

          <!-- <v-divider inset></v-divider> -->

          <v-list-tile>
            <v-list-tile-action>
              <v-icon>code</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title>模式范围</v-list-tile-title>
            </v-list-tile-content>

            <v-list-tile-action>
              <v-icon>chat</v-icon>
            </v-list-tile-action>
          </v-list-tile>

          <!-- <v-divider inset></v-divider> -->

          <v-list-tile>
            <v-list-tile-action>
              <v-icon>title</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title>温度</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- <v-divider inset></v-divider> -->

          
        </v-list>
        <v-tooltip top>
            <template v-slot:activator="{ on }">
                
                    <v-img v-on="on"
                    src="https://bqzp.xyz/wp-content/uploads/2019/05/timg.jpg"
                    height="300px"
                    ></v-img>
                
            </template>
            <span>tooltip试用</span>
        </v-tooltip>
        
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

  export default {
    data: () => ({
      
    }),

    components: {
      
    }
  }

</script>