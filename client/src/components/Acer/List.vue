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
      selected: [],

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
      desserts: [
          {
            name: 'Frozen Yogurt',
            calories: 159,
            fat: 6.0,
            carbs: 24,
            protein: 4.0,
            iron: '1%'
          },
          {
            name: 'Ice cream sandwich',
            calories: 237,
            fat: 9.0,
            carbs: 37,
            protein: 4.3,
            iron: '1%'
          },
          {
            name: 'Eclair',
            calories: 262,
            fat: 16.0,
            carbs: 23,
            protein: 6.0,
            iron: '7%'
          },
          {
            name: 'Cupcake',
            calories: 305,
            fat: 3.7,
            carbs: 67,
            protein: 4.3,
            iron: '8%'
          },
          {
            name: 'Gingerbread',
            calories: 356,
            fat: 16.0,
            carbs: 49,
            protein: 3.9,
            iron: '16%'
          },
          {
            name: 'Jelly bean',
            calories: 375,
            fat: 0.0,
            carbs: 94,
            protein: 0.0,
            iron: '0%'
          },
          {
            name: 'Lollipop',
            calories: 392,
            fat: 0.2,
            carbs: 98,
            protein: 0,
            iron: '2%'
          },
          {
            name: 'Honeycomb',
            calories: 408,
            fat: 3.2,
            carbs: 87,
            protein: 6.5,
            iron: '45%'
          },
          {
            name: 'Donut',
            calories: 452,
            fat: 25.0,
            carbs: 51,
            protein: 4.9,
            iron: '22%'
          },
          {
            name: 'KitKat',
            calories: 518,
            fat: 26.0,
            carbs: 65,
            protein: 7,
            iron: '6%'
          }
        ]
    }),

    components: {
      ListItem
    }
  }

</script>