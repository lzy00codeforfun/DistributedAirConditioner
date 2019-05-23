<template>
  <div>
    <v-container fluid>
      <v-layout row wrap>
        <v-flex xs8 offset-xs2>

        <v-layout row wrap>
          <v-flex xs12 sm12 md12>
            <v-layout v-if=isOn>
              <v-flex xs12 sm12 md5>
                <v-layout column wrap>
                  <v-flex>
                    <div style="background-color:#3e50b4;height:84px;">
                      <v-btn flat icon color="green" class="mr-0 ml-5 my-4">
                        <v-icon>fiber_manual_record</v-icon>
                      </v-btn>
                      <v-btn flat icon color="red" class="mx-0 my-4">
                        <v-icon>fiber_manual_record</v-icon>
                      </v-btn>
                      <v-btn flat icon color="grey" class="mx-0 my-4">
                        <v-icon>fiber_manual_record</v-icon>
                      </v-btn>
                      <v-btn flat icon color="blue" class="mx-0 my-4">
                        <v-icon>fiber_manual_record</v-icon>
                      </v-btn>
                      <v-btn flat icon color="yellow" class="mx-0 my-4">
                        <v-icon>fiber_manual_record</v-icon>
                      </v-btn>
                    </div>
                  </v-flex>
                  <v-flex>
                    <div style="background-color:#3e50b4;height:336px">
                      
                      <div style="position:relative;top:20%;text-align:right;">
                        <font color="white"  style="font-size:100px">{{currentTmp}}</font>
                        <font color="white"  style="font-size:20px;position:relative;top: 10px;">℃</font>
                        <font color="white"  style="font-size:80px;position:relative;top: 20px;font-weight:100;">/</font>
                        <font color="white"  style="font-size:40px;position:relative;top: 20px;">{{targetTmp}}</font>
                        <font color="white"  style="font-size:20px;position:relative;top: 30px;">℃</font>
                      </div>
                      
                      <div style="position:relative;top:20%;text-align:right;">
                        <font color="white"  style="font-size:20px"><i>节电同心，低碳同行</i></font>
                      </div>

                    </div>
                  </v-flex>
                </v-layout>
              </v-flex>

              <v-flex xs12 sm12 md3>
                <v-layout column wrap>
                  <v-flex>
                    <div style="background-color:#3e50b4;height:210px">
                      <div style="position:relative;top:20%;">
                        <div style="display:inline-block;position:relative;left:20%;">
                          <font color="white"  style="font-size:25px">风速</font>
                        </div>
                        <div style="display:inline-block;position:relative;top:20px;left:30%;">
                          <i><img src="../assets/User/air.png" height="50px" ></i>
                        </div>
                      </div>
                      <div style="position:relative;top:25%;left:120px">
                        <i><img src="../assets/User/black.png" height="5px" width="10px" v-if="airSpeed>=1"></i>
                        <i><img src="../assets/User/black.png" height="10px" width="10px" style="position:relative;left:5px;"  v-if="airSpeed>=2"></i>
                        <i><img src="../assets/User/black.png" height="18px" width="10px" style="position:relative;left:10px;"  v-if="airSpeed>=3"></i>
                        <i><img src="../assets/User/black.png" height="29px" width="10px" style="position:relative;left:15px;"  v-if="airSpeed>=4"></i>
                      </div>
                    </div>
                  </v-flex>
                  <v-flex>
                    <div style="background-color:#3e50b4;height:210px">

                        <div style="position:relative;left:20%;">
                          <font color="white"  style="font-size:25px">模式</font>
                        </div>
                        <div style="position:relative;top:30px;left:50%;">
                          <i><img src="../assets/User/cold.png" height="50px" v-if="mode==1"></i>
                          <i><img src="../assets/User/hot.png" height="50px" v-if="mode==2"></i>
                        </div>


                    </div>
                  </v-flex>
                </v-layout>
              </v-flex>

              <v-flex xs12 sm12 md4>
                <v-layout column wrap>
                  <v-flex>
                    <div style="background-color:#3e50b4;height:210px">
                      <div style="display:inline-block;float:right;position:relative;top:5%;">
                        <v-btn color="red" round>
                          <font color="white" style="font-weight:580;">一层101</font>
                        </v-btn>
                      </div>
                    </div>
                  </v-flex>
                  <v-flex>
                    <div style="background-color:#3e50b4;height:210px">
                      <div style="position:relative;top:0%;">
                        <div style="position:relative;top:8.8px;">
                          <font color="white"  style="font-size:25px">总费用</font>
                        </div>
                        <div style="text-align:center">
                          <font color="white"  style="font-size:50px;display:block;">￥{{sumFee}}</font>
                          <v-btn color="green" large>
                            <font color="white" style="font-weight:800;">第一阶段</font>
                          </v-btn>
                        </div>
                      </div>
                    </div>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>

            <v-layout v-if=!isOn>
              <v-flex xs12>
              <v-card
                class="mx-auto"
                color="#26c6da"
                dark
              >
                <v-card-title>
                  <span class="title font-weight-light">已关机</span>
                </v-card-title>

                <v-card-text class="headline font-weight-bold">
                  "感谢您的使用！“节电同心，低碳同行”，我们在路上！期待您的下次使用！"
                </v-card-text>

                <v-card-actions class="pa-3">
                  Rate this service
                  <v-icon class="mx-2">tag_faces</v-icon>
                  <v-spacer></v-spacer>
                  <v-icon>star_border</v-icon>
                  <v-icon>star_border</v-icon>
                  <v-icon>star_border</v-icon>
                  <v-icon>star_border</v-icon>
                  <v-icon>star_border</v-icon>
                </v-card-actions>
              </v-card>
              </v-flex>
            </v-layout>
          </v-flex>

          

          <v-flex xs12 sm6 md2>
            <v-btn color="#3e50b4" block large v-if=isOn @click="isOn=!isOn">
                <i><img src="../assets/User/on_off.png" height="40px" ></i>
            </v-btn>
            <v-btn color="#26c6da" block large v-else @click="isOn=!isOn">
                <i><img src="../assets/User/on_off.png" height="40px" ></i>
            </v-btn>
          </v-flex>
          <v-flex xs12 sm6 md3>
            <v-btn color="#3e50b4" block large v-if=isOn @click="mode=(mode%2+1)">
                <font color="white" style="font-weight:800;">模式</font>
            </v-btn>
            <v-btn color="#26c6da" block large v-else>
                <font color="white" style="font-weight:800;">模式</font>
            </v-btn>
          </v-flex>
          <v-flex xs12 sm6 md3>
            <v-btn color="#3e50b4" block large v-if=isOn @click="airSpeed=airSpeed%4+1">
                <font color="white" style="font-weight:800;">风速</font>
            </v-btn>
            <v-btn color="#26c6da" block large v-else>
                <font color="white" style="font-weight:800;">风速</font>
            </v-btn>
          </v-flex>
          <v-flex xs12 sm3 md2>
            <v-btn color="#3e50b4" block large v-if=isOn @click="targetTmp++">
                <font color="white" style="font-weight:800;font-size:30px">+</font>
            </v-btn>
            <v-btn color="#26c6da" block large v-else>
                <font color="white" style="font-weight:800;font-size:30px">+</font>
            </v-btn>
          </v-flex>
          <v-flex xs12 sm3 md2>
            <v-btn color="#3e50b4" block large v-if=isOn @click="targetTmp--">
                <font color="white" style="font-weight:800;font-size:30px">-</font>
            </v-btn>
            <v-btn color="#26c6da" block large v-else>
                <font color="white" style="font-weight:800;font-size:30px">-</font>
            </v-btn>
          </v-flex>
        </v-layout>
          
        

        </v-flex>
      </v-layout>


    </v-container>
  </div>
</template>

<script>

  export default {
    data: () => ({
      isOn:false,
      currentTmp:24,
      targetTmp:18,
      airSpeed:4,
      mode:1, //1:cold 2:hot
      sumFee:50.21
    }),

    components: {
      
    }
  }

</script>

<style scoped>
  @import url("https://fonts.googleapis.com/icon?family=Material+Icons");
  div{
    border-radius: 0;
    border-style: none;
  }
</style>