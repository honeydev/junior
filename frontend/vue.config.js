const path = require('path');

module.exports = {
    configureWebpack: {
        // Make output JS file names static
        output: {
          filename: '[name].js',
          chunkFilename: '[name].js'
        }
    }
}
