var webpack = require("webpack")
var BundleTracker = require('webpack-bundle-tracker')

var config = require('./webpack.base.config.js')

config.entry = [
    'webpack-dev-server/client?http://localhost:3000',
    'webpack/hot/only-dev-server',
    '../client/js/index'
]

// override django's STATIC_URL for webpack bundles
config.output.publicPath = 'http://localhost:3000/client/bundles/'

config.plugins = config.plugins.concat([
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),  // don't reload if there is an error
    new BundleTracker({filename: './webpack-stats.json'}),
])

config.module.loaders.push(
    {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loaders: ['react-hot', 'babel'],
    }
)

module.exports = config
