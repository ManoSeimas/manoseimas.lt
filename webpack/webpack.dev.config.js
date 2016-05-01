var path = require('path');
var webpack = require("webpack")
var BundleTracker = require('webpack-bundle-tracker')
var WatchIgnorePlugin = require('watch-ignore-webpack-plugin')

var config = require('./webpack.base.config.js')
var app_root = '../manoseimas'

config.devtool = 'eval-source-map'

config.entry = {
    compat_test: [
       'webpack-dev-server/client?http://localhost:3000',
       'webpack/hot/only-dev-server',
        app_root + '/compatibility_test/client/index'
    ],
    react: ['react', 'react-dom'],
}

// override django's STATIC_URL for webpack bundles
config.output.publicPath = 'http://localhost:3000/client/bundles/'

config.plugins = config.plugins.concat([
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),  // don't reload if there is an error
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.optimize.CommonsChunkPlugin('react', "react.bundle.js"),
    new WatchIgnorePlugin([path.resolve(__dirname, './node_modules')])
])

config.module.loaders.push(
    {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loaders: ['react-hot', 'babel'],
    }
)

module.exports = config
