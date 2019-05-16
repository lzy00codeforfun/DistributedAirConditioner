<template>
  <v-app>
    
    <v-toolbar app>
      <v-btn flat @click="mainList=!mainList">
        <v-icon large>list</v-icon>
      </v-btn>
      
      <v-toolbar-title class="headline text-uppercase">
        <span>空调管理系统</span>
        <span class="font-weight-light"> {{url}} </span>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      

      <v-btn flat icon>
        <!-- <span class="mr-2">Latest Release</span>
        <v-icon>list</v-icon> -->
        <v-avatar :tile="false" size="28" color="grey lighten-4" >
          <img src="./assets/avatar.jpg" alt="avatar">
        </v-avatar>
      </v-btn>
    </v-toolbar>
    
    <v-navigation-drawer stateless value="false" v-model="mainList" app>
      <v-list>
        <v-list-tile to="/">
          <v-list-tile-action>
            <v-icon>home</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>首页</v-list-tile-title>
        </v-list-tile>

        <v-list-group
          prepend-icon="account_circle"
          value="true"
        >
          <template v-slot:activator>
            <v-list-tile>
              <v-list-tile-title>分类</v-list-tile-title>
            </v-list-tile>
          </template>
          <v-list-group
            no-action
            sub-group
            value="true"
          >
            <template v-slot:activator>
              <v-list-tile>
                <v-list-tile-title>使用平台</v-list-tile-title>
              </v-list-tile>
            </template>

            
            <v-list-tile v-for="(u, i) in use" :key="i" :to="u.path">
              <v-list-tile-title v-text="u.name"></v-list-tile-title>
              <v-list-tile-action>
                <v-icon v-text="u.icon"></v-icon>
              </v-list-tile-action>
            </v-list-tile>
            
            

          </v-list-group>

          <v-list-group
            sub-group
            no-action
          >
            <template v-slot:activator>
              <v-list-tile>
                <v-list-tile-title>管理平台</v-list-tile-title>
              </v-list-tile>
            </template>

            
            <v-list-tile v-for="(m, i) in manage" :key="i" :to="m.path">
              <v-list-tile-title v-text="m.name"></v-list-tile-title>
              <v-list-tile-action>
                <v-icon v-text="m.icon"></v-icon>
              </v-list-tile-action>
            </v-list-tile>
            
            

          </v-list-group>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>
    
    <v-content>
      <router-view/>
    </v-content>

    
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data () {
    return {
      mainList:false,
      use: [
        {name:'用户', icon:'people_outline', path:'/user'},
        {name:'前台', icon:'settings', path:'/frontdesk'}
      ],
      manage: [
        {name:'空调管理员', icon:'add', path:'/acer'},
        {name:'经理', icon:'insert_drive_file', path:'/manager'},
      ]
    }
  }
}
</script>
