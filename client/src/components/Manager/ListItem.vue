<template>
    <v-card class="mt-2" style="border:1px solid rgba(30,144,255,0.5);border-radius:30px;" >
        <v-card-title primary-title>      
            <div>
                <i class="material-icons" style="font-size:24px;color:#1E90FF;position:relative;top:5px;">signal_cellular_alt</i>
                <font size="4"><strong>{{info.nameStr}}</strong></font>
                <v-btn icon flatc style="position:absolute;right:5%;top:20px;">
                <i class="material-icons" style="font-size:24px;color:#1E90FF;">get_app</i>     
                </v-btn>
            </div>
        </v-card-title>
        <v-divider></v-divider>

        <v-card-text>
        <v-layout row wrap>
            <v-flex xs12>
                <v-layout row wrap align-center justify-center>
                    <v-flex xs6>
                        <font color="black"  style="font-size:25px;display:block;text-align:center;">总费用</font>
                        <font color="black"  style="font-size:40px;font-weight:700;text-align:center;display:block;">{{info.sumFee}}</font>
                    </v-flex>
                    <v-flex xs6>
                        <font color="black"  style="font-size:25px;display:block;text-align:center;">使用时长</font>
                        <font color="black"  style="font-size:40px;font-weight:700;display:block;text-align:center;">{{info.sumTime}}
                            <font color="black"  style="font-size:25px;position:relative;top:-5px;font-weight:500;">时</font>
                        </font>
                        
                    </v-flex>
                </v-layout>
            </v-flex>
            <v-flex xs12>
                <v-layout row wrap align-center justify-center>
                    <v-flex xs2>
                        <font color="black"  style="font-size:15px;display:block;text-align:center;">开关数</font>
                        <font color="black"  style="font-size:20px;font-weight:700;display:block;text-align:center;">{{info.numOnOff}}</font>
                    </v-flex>
                    <v-flex xs2>
                        <font color="black"  style="font-size:15px;display:block;text-align:center;">调温数</font>
                        <font color="black"  style="font-size:20px;font-weight:700;display:block;text-align:center;">{{info.numTemper}}</font>
                    </v-flex>
                    <v-flex xs2>
                        <font color="black"  style="font-size:15px;display:block;text-align:center;">调风数</font>
                        <font color="black"  style="font-size:20px;font-weight:700;display:block;text-align:center;">{{info.numAir}}</font>
                    </v-flex>
                    <v-flex xs2>
                        <font color="black"  style="font-size:15px;display:block;text-align:center;">调度数</font>
                        <font color="black"  style="font-size:20px;font-weight:700;display:block;text-align:center;">{{info.numDispatch}}</font>
                    </v-flex>
                    <v-flex xs2>
                        <font color="black"  style="font-size:15px;display:block;text-align:center;">详单数</font>
                        <font color="black"  style="font-size:20px;font-weight:700;display:block;text-align:center;">{{info.numSummary}}</font>
                    </v-flex>      
                </v-layout>
            </v-flex>
        </v-layout>
        </v-card-text>
    </v-card>
</template>

<script>

  export default {
    data: () => ({
      
    }),

    components: {
      
    },
    props:{
        info:Map,
    },
  }

</script>

<style scoped>
  @import url("https://fonts.googleapis.com/icon?family=Material+Icons");

</style>