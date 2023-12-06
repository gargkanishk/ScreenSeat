
module.exports = {
  configureWebpack: {
    devtool: 'source-map'
  },
  chainWebpack: (config) => {
    config.module
      .rule('csv')
      .test(/\.csv$/)
      .use('csv-loader')
      .loader('csv-loader')
      .options({
        header: true, // Treat the first row as header
      })
    }
}
