<template>
  <div>
    <v-container fluid>

      <v-layout row wrap>
        <v-flex xs10 offset-xs1>
          <v-layout row wrap>
            <v-flex xs12 sm12 md12>
              <font color="black" style="font-size:20px">快速开始/便携导航</font>
            </v-flex>
            <v-flex xs12 sm12 md12>
              <v-layout row wrap>
                <v-flex xs12 sm12 md4>
                  <v-card color="white darken-2" class="white--text" min-height="150px" @click="click1">
                    <v-layout>
                      <v-flex xs3>
                        <v-layout align-center justify-end row fill-height>
                          <v-btn flat icon @click="pageIndex=1">
                          <i class="material-icons" style="color:orange">https</i>
                          </v-btn>
                        </v-layout>
                      </v-flex>
                      <v-flex xs9>
                        <v-card-title primary-title>
                          <div>
                            <div>
                              <font color="black" style="font-size:18px">房间动态控制</font>
                            </div>
                            <div>
                              <font color="grey" style=";position:relative;top:10px;">控制空调使用权限</font>
                            </div>
                          </div>
                        </v-card-title>
                      </v-flex>
                    </v-layout>
                  </v-card>
                </v-flex>
                <v-flex xs12 sm12 md4>
                  <v-card color="white darken-2" class="white--text" min-height="150px" @click="click2">
                    <v-layout>
                      <v-flex xs3>
                        <v-layout align-center justify-end row fill-height>
                          <v-btn flat icon @click="pageIndex=2">
                          <i class="material-icons" style="color:blue">event_note</i>
                          </v-btn>
                        </v-layout>
                      </v-flex>
                      <v-flex xs9>
                        <v-card-title primary-title>
                          <div>
                            <div>
                              <font color="black" style="font-size:18px">详单生成</font>
                            </div>
                            <div>
                              <font color="grey" style=";position:relative;top:10px;">生成空调使用详单</font>
                            </div>
                          </div>
                        </v-card-title>
                      </v-flex>
                    </v-layout>
                  </v-card>
                </v-flex>
                <v-flex xs12 sm12 md4>
                  <v-card color="white darken-2" class="white--text" min-height="150px" @click="click3">
                    <v-layout>
                      <v-flex xs3>
                        <v-layout align-center justify-end row fill-height>
                          <v-btn flat icon @click="pageIndex=3">
                          <i class="material-icons" style="color:red">account_balance_wallet</i>
                          </v-btn>
                        </v-layout>
                      </v-flex>
                      <v-flex xs9>
                        <v-card-title primary-title>
                          <div>
                            <div>
                              <font color="black" style="font-size:18px">退房结账</font>
                            </div>
                            <div>
                              <font color="grey" style=";position:relative;top:10px;">生成账单，关闭空调权限</font>
                            </div>
                          </div>
                        </v-card-title>
                      </v-flex>
                    </v-layout>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-layout>

      <v-layout justify-center class="mt-4" v-if="pageIndex==1">
        <v-flex xs10>
          <v-card>
            <v-card-title class="light-white pl-5">
              <span>
                <font color="blue"  style="font-size:20px">房间动态控制</font>
              </span>
              <span style="position:relative;left:10%;display:inline-block;width:50%;">
                <v-text-field
                  label="请输入输入房间ID以搜索"
                  clearable
                  append-outer-icon="search"
                  @click:append-outer="search"
                  v-model="searchText"
                >
                </v-text-field>
              </span>
              <v-spacer></v-spacer>

            </v-card-title>

            <v-divider></v-divider>

            <div>
              <v-data-table
                :headers="headers"
                :items="items"
                :search="search"
                hide-actions
                :pagination.sync="pagination"
                class="elevation-1"
              >
                <template v-slot:items="props">
                  <td>
                    <font color=""  style="font-size:20px">{{ props.item.roomId }}</font>
                    </td>
                  <td>
                    <v-btn @click="props.item.isLock=!props.item.isLock" flat >
                      <i class="material-icons" style="font-size: 18px;color:red;position:relative;top:10%;" v-if="props.item.isLock">fiber_manual_record</i>
                      <i class="material-icons" style="font-size: 18px;color:green;position:relative;top:10%;" v-else>fiber_manual_record</i>
                      {{ props.item.isLock?"已上锁":"已解锁" }}
                    </v-btn>
                    
                  </td>
                </template>
              </v-data-table>
              <div class="text-xs-center pt-2">
                <v-pagination v-model="pagination.page" :length="pages"></v-pagination>
              </div>
            </div>
          </v-card>
        </v-flex>
      </v-layout>

      <v-layout justify-center class="mt-4" v-if="pageIndex==2">
        <v-flex xs10>
          <v-card>
            <v-card-title class="light-white pl-5">
              <span>
                <font color="blue"  style="font-size:20px">空调详情</font>
              </span>
              <span style="position:relative;left:10%;display:inline-block;width:50%;">
                <v-text-field
                  label="请输入输入房间ID以搜索"
                  clearable
                  append-outer-icon="search"
                  @click:append-outer="search"
                  v-model="searchText2"
                >
                </v-text-field>
              </span>
              <v-spacer></v-spacer>

            </v-card-title>

            <v-divider></v-divider>

            <div>
              <v-data-table
                :headers="headers2"
                :items="items2"
                :search="search2"
                hide-actions
                :pagination.sync="pagination"
                class="elevation-1"
              >
                <template v-slot:items="props">
                  <td><font color=""  style="font-size:20px">{{ props.item.time }}</font></td>
                  <td><font color=""  style="font-size:20px">{{ props.item.speed }}</font></td>
                  <td>
                    <i class="material-icons" style="font-size: 18px;color:red;position:relative;top:10%;" v-if="props.item.status=='制热'">fiber_manual_record</i>
                    <i class="material-icons" style="font-size: 18px;color:green;position:relative;top:10%;" v-else-if="props.item.status=='制冷'">fiber_manual_record</i>
                    <i class="material-icons" style="font-size: 18px;color:blue;position:relative;top:10%;" v-else>fiber_manual_record</i>
                    {{ props.item.status }}      
                  </td>
                  <td><font color=""  style="font-size:20px">{{ props.item.feeRate }}</font></td>
                  <td><font color=""  style="font-size:20px">{{ props.item.sumFee }}</font></td>
                  <td><font color=""  style="font-size:20px">{{ props.item.spendTime }}</font></td>
                </template>
              </v-data-table>
              <div class="text-xs-center pt-2">
                <v-pagination v-model="pagination.page" :length="pages"></v-pagination>
              </div>
            </div>
          </v-card>
        </v-flex>
      </v-layout>

    </v-container>
  </div>
</template>

<script>
export default {
  data: () => ({
    pageIndex:2,
    
    searchText:"",
    search: '',
    pagination: {},
    headers: [
          {
            text: '房间',
            align: 'left',
            sortable: true,
            value: 'roomId'
          },
          { text: '状态', value: 'isLock',align: 'left',},

        ],
    items:[
          {
            roomId:"101",
            isLock:false
          },
          {
            roomId:"303",
            isLock:true
          },
          {
            roomId:"202",
            isLock:false
          },
          {
            roomId:"102",
            isLock:true
          },
          {
            roomId:"666",
            isLock:true
          },
          {
            roomId:"666",
            isLock:true
          },
          {
            roomId:"666",
            isLock:true
          },
          {
            roomId:"666",
            isLock:true
          },
      ],

    searchText2:"",
    search2: '',
    pagination2: {},
    headers2: [
          {
            text: '时间',
            align: 'left',
            sortable: true,
            value: 'time'
          },
          { text: '风速', value: 'speed',align: 'left',},
          { text: '状态', value: 'status',align: 'left',},
          { text: '费率', value: 'feeRate',align: 'left',},
          { text: '总费用', value: 'sumFee',align: 'left',},
          { text: '耗时', value: 'spendTime',align: 'left',},
        ],
    items2:[
          {
            time:"2019-10-01 10:53",
            speed:100,
            status:"制冷",
            feeRate:"第一阶段",
            sumFee:5,
            spendTime:"5min"
          },
          {
            time:"2019-10-01 10:53",
            speed:200,
            status:"制热",
            feeRate:"第二阶段",
            sumFee:5,
            spendTime:"1h"
          },
          {
            time:"2019-10-01 10:53",
            speed:90,
            status:"送风",
            feeRate:"第一阶段",
            sumFee:5,
            spendTime:"5min"
          },
          {
            time:"2019-10-01 10:53",
            speed:50,
            status:"送风",
            feeRate:"第二阶段",
            sumFee:5,
            spendTime:"5min"
          },
          {
            time:"2019-10-02 10:53",
            speed:100,
            status:"制冷",
            feeRate:"第一阶段",
            sumFee:5,
            spendTime:"50min"
          },
          {
            time:"2019-10-08 10:53",
            speed:200,
            status:"制热",
            feeRate:"第一阶段",
            sumFee:5,
            spendTime:"35min"
          },
          
      ],
  }),
  methods:{
    search(){

    },
    click1(){
      
    },
    click2(){
      
    },
    click3(){
      
    },
  },
  computed: {
      pages () {
        if (this.pagination.rowsPerPage == null ||
          this.pagination.totalItems == null
        ) return 0

        return Math.ceil(this.pagination.totalItems / this.pagination.rowsPerPage)
      }
    }
};
</script>