var path = require("path")
var webpack = require('webpack')

module.exports = {
    context: __dirname,

    entry: '../client/js/index',

    output: {
        path: path.resolve('./bundles/'),
        filename: "[name]-[hash].js"
    },

    plugins: [
    ], // add all common plugins here

    module: {
      loaders: [] // add all common loaders here
    },

    resolve: {
        modulesDirectories: ['node_modules', 'bower_components'],
        extensions: ['', '.js', '.jsx']
    },

    watchOptions: {
        poll: true
    }
}
