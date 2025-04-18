const { ModuleFederationPlugin } = require('webpack').container;
const path = require('path');

module.exports = {
  output: {
    uniqueName: 'examplePlugin',
    publicPath: 'auto',
    scriptType: 'text/javascript',
  },
  optimization: {
    runtimeChunk: false
  },
  experiments: {
    outputModule: true
  },
  plugins: [
    new ModuleFederationPlugin({
      name: 'examplePlugin',
      filename: 'remoteEntry.js',
      exposes: {
        './Module': './src/app/hello.module.ts',
      },
      shared: {
        '@angular/core': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0' },
        '@angular/common': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0' },
        '@angular/router': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0' },
        '@angular/common/http': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0' },
      }
    })
  ]
};
