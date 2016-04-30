var path = require("path")
var webpack = require("webpack")
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: [
      'webpack-dev-server/client?http://localhost:3000',
      'webpack/hot/only-dev-server',
      './client/js/index'
  ],

  output: {
      path: path.resolve('./client/bundles/'),
      filename: "[name]-[hash].js",
      publicPath: 'http://localhost:3000/client/bundles/',
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),  // don't reload if there is an error
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    loaders: [
        {
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            loaders: ['react-hot', 'babel'],
        },
    ],
  },

  resolve: {
    modulesDirectories: ['node_modules', 'bower_components'],
    extensions: ['', '.js', '.jsx']
  },

  watchOptions: {
    poll: true
  }
}
