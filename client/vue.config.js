module.exports={
    baseUrl:"/", //根路径
    // outputDir:"dist", //构建输出目录 生产环境出现
    assetsDir:"assets",  //静态资源目录
    lintOnSave: false, //是否开启eslint保存检测
    devServer:{
        open:true,
        host:"localhost", //0.0.0.0 真机测试
        port: 8081,
        https: false,
        hotOnly: false,
        proxy:{
            //配置跨域，请求后端接口
            '/api':{
                target: "http://localhost:5000/api/",
                ws: true,
                changOrigin: true,
                pathRewrite: {
                    '^/api':''
                }
            }

        }
    }
    
};