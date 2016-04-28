var path = require("path")
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: './assets/js/index.jsx',

  output: {
      path: path.resolve('./assets/bundles/'),
      filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    loaders: [
        {
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
                presets: ['es2015','react']
            }
        },
    ],
  }
}
