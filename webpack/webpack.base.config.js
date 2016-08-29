var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

var app_root = '../manoseimas'
var precss        = require('precss'),
    autoprefixer  = require('autoprefixer'),
    lost          = require('lost'),
    postcssImport = require('postcss-import')

module.exports = {
    context: __dirname,

    entry: {
       compat_test: app_root + '/compatibility_test/client/index',
       react: ['react', 'react-dom', 'react-router', 'react-redux', 'redux'],
    },

    output: {
        path: path.resolve('./build/bundles/'),
        filename: "[name]-[hash].js"
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.optimize.CommonsChunkPlugin('react', "react.bundle.js"),
    ], // add all common plugins here

    module: {
        loaders: [{
            test: /\.(js|jsx)$/,
            include: path.join(__dirname, '../manoseimas/compatibility_test'),
            loaders: ['react-hot', 'babel'],
        }, {
            test:   /\.css$/,
            exclude: /node_modules/,
            loader: 'style!css-loader?modules&importLoaders=1&localIdentName=[name]__[local]___[hash:base64:5]!postcss-loader'
        }
      ] // add all common loaders here
    },

    resolve: {
        modulesDirectories: ['node_modules', 'bower_components'],
        extensions: ['', '.js', '.jsx']
    },

    postcss: function () {
        return [
            postcssImport({ addDependencyTo: webpack }), // Must be first item in list
            precss,
            autoprefixer,
            lost
        ]
    },

    watchOptions: {
        poll: true
    }
}
