module.exports = {
  transpileDependencies: ["vuetify"],
  publicPath: "/dist",
  outputDir: "../backend/dist/",
  devServer: {
    headers: { "Access-Control-Allow-Origin": "*" },
  },
};