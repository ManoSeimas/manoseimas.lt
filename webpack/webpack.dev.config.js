var path = require('path');
var webpack = require("webpack")

var config = require('./webpack.base.config.js')
var app_root = '../manoseimas'


config.devtool = 'eval-source-map'

config.entry.compat_test = [
    'webpack-dev-server/client?http://192.168.33.10:3000',
    'webpack/hot/dev-server',
    app_root + '/compatibility_test/client/index'
]

// override django's STATIC_URL for webpack bundles
config.output.publicPath = 'http://192.168.33.10:3000/client/bundles/'
config.libraryTarget = 'umd'

config.plugins = config.plugins.concat([
    new webpack.HotModuleReplacementPlugin(),
    // new webpack.NoErrorsPlugin(),  // don't reload if there is an error
])

// config.module.loaders.push({})


module.exports = config
