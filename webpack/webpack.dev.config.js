var path = require('path');
var webpack = require("webpack")
var BundleTracker = require('webpack-bundle-tracker')

var precss        = require('precss'),
    autoprefixer  = require('autoprefixer'),
    lost          = require('lost'),
    postcssImport = require('postcss-import')

var config = require('./webpack.base.config.js')
var app_root = '../manoseimas'


config.devtool = 'eval-source-map'

config.entry = {
    compat_test: [
        'webpack-dev-server/client?http://localhost:3000',
        'webpack/hot/dev-server',
        app_root + '/compatibility_test/client/index'
    ],
    react: ['react', 'react-dom', 'react-router', 'react-redux', 'redux'],
}

// override django's STATIC_URL for webpack bundles
config.output.publicPath = 'http://localhost:3000/client/bundles/'
config.libraryTarget = 'umd'

config.plugins = config.plugins.concat([
    new webpack.HotModuleReplacementPlugin(),
    // new webpack.NoErrorsPlugin(),  // don't reload if there is an error
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.optimize.CommonsChunkPlugin('react', "react.bundle.js"),
])

config.module.loaders.push(
    {
        test: /\.(js|jsx)$/,
        include: path.join(__dirname, '../manoseimas/compatibility_test'),
        loaders: ['react-hot', 'babel'],

    }, {
        test:   /\.css$/,
        exclude: /node_modules/,
        loader: 'style!css-loader?modules&importLoaders=1&localIdentName=[name]__[local]___[hash:base64:5]!postcss-loader'
    }
)

config.postcss = function () {
    return [
        postcssImport({ addDependencyTo: webpack }), // Must be first item in list
        precss,
        autoprefixer,
        lost
    ]
}

module.exports = config
