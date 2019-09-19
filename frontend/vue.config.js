const path = require('path');

module.exports = {
    outputDir: path.resolve(__dirname, "../src/static/dist"),
    configureWebpack: {
        output: {
            filename: '[name].js',
            chunkFilename: '[name].js'
        },
    }
};
