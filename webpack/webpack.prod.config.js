var webpack = require("webpack")
var BundleTracker = require('webpack-bundle-tracker')
var config = require('./webpack.base.config.js')

config.output.path = require('path').resolve('./bundles')

config.plugins = config.plugins.concat([
  new BundleTracker({filename: './webpack-stats-prod.json'}),

  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production')
  }}),

  // keeps hashes consistent between compilations
  new webpack.optimize.OccurenceOrderPlugin(),

  // minifies bundled code
  new webpack.optimize.UglifyJsPlugin({
    compressor: { warnings: false }
  })
])

module.exports = config
