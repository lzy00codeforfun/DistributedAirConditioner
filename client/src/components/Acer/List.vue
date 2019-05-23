<template>
  <v-layout justify-center>
    <v-flex xs12>
      <v-card>
        <v-card-title class="light-white pl-5">
          <span class="headline black--text"><strong>空调状态</strong></span>
          
          <v-spacer></v-spacer>
          <v-menu offset-y>
            <template v-slot:activator="{ on }">
              <v-btn
                color="primary"
                dark
                v-on="on"
              >
                {{currentLevel}}
                <v-icon>expand_more</v-icon>
              </v-btn>
            </template>

            <v-list>
              <v-list-tile
                v-for="(item, i) in levels"
                :key="i"
                @click="currentLevel=item.title"
              >
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-card-title>

        <v-divider></v-divider>

       <!-- <ListItem v-for="(item,i) in items" :key="i" :info=item></ListItem> -->

      <div>
        <v-data-table
        hide-headers
        :items="items"
        :search="search"
        hide-actions
        :pagination.sync="pagination"
        class="elevation-1"
        >
        <template v-slot:items="props">
            <ListItem :info=props.item></ListItem>
        </template>
        </v-data-table>
        <div class="text-xs-center pt-2">
        <v-pagination v-model="pagination.page" :length="pages"></v-pagination>
        </div>
      </div>

        
       
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  import ListItem from "./ListItem.vue"
  export default {
    computed: {
      pages () {
        if (this.pagination.rowsPerPage == null ||
          this.pagination.totalItems == null
        ) return 0

        return Math.ceil(this.pagination.totalItems / this.pagination.rowsPerPage)
      }
    },
    data: () => ({
      currentLevel:"全部",
      levels: [
        { title: '全部' },
        { title: '一层' },
        { title: '二层' },
        { title: '三层' },
        { title: '四层' },
        { title: '五层' }
      ],

      search: '',
      pagination: {},
      items:[
          {
            nameStr:"一层101",
            maxTmp:23,
            minTmp:18,
            serviceState:"正在服务",
            isCold:true,
            percent:100,
            fee:100,
            info:"24小时3分 第一状态"
          },
          {
            nameStr:"二层222",
            maxTmp:30,
            minTmp:20,
            serviceState:"停止服务",
            isCold:false,
            percent:50,
            fee:200,
            info:"22小时3分 第二状态"
          },
          {
            nameStr:"三层301",
            maxTmp:50,
            minTmp:0,
            serviceState:"正在服务",
            isCold:true,
            percent:30,
            fee:2000,
            info:"255小时8分 第一状态"
          },
          {
            nameStr:"五层501",
            maxTmp:23,
            minTmp:18,
            serviceState:"正在服务",
            isCold:false,
            percent:100,
            fee:20,
            info:"242小时3分 第一状态"
          },
          {
            nameStr:"五层501",
            maxTmp:23,
            minTmp:18,
            serviceState:"正在服务",
            isCold:false,
            percent:100,
            fee:20,
            info:"242小时3分 第一状态"
          },
          {
            nameStr:"五层501",
            maxTmp:23,
            minTmp:18,
            serviceState:"正在服务",
            isCold:false,
            percent:100,
            fee:20,
            info:"242小时3分 第一状态"
          },
          {
            nameStr:"五层501",
            maxTmp:23,
            minTmp:18,
            serviceState:"正在服务",
            isCold:false,
            percent:100,
            fee:20,
            info:"242小时3分 第一状态"
          },
          {
            nameStr:"五层501",
            maxTmp:23,
            minTmp:18,
            serviceState:"正在服务",
            isCold:false,
            percent:100,
            fee:20,
            info:"242小时3分 第一状态"
          },
          {
            nameStr:"五层501",
            maxTmp:23,
            minTmp:18,
            serviceState:"正在服务",
            isCold:false,
            percent:100,
            fee:20,
            info:"242小时3分 第一状态"
          },
      ],
     
    }),

    components: {
      ListItem
    }
  }

</script>