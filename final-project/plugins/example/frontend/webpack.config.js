const { ModuleFederationPlugin } = require('webpack').container;
const path = require('path');

module.exports = {
  output: {
    uniqueName: 'examplePlugin',
    publicPath: 'auto',
    scriptType: 'module'
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
        './Component': './src/app/hello.component.ts'
      },
      shared: {
        '@angular/core': { singleton: true, strictVersion: false, requiredVersion: '^19.2.0' },
        '@angular/common': { singleton: true, strictVersion: false, requiredVersion: '^19.2.0' },
        '@angular/router': { singleton: true, strictVersion: false, requiredVersion: '^19.2.0' }
      },
      library: { type: 'module' }
    })
  ]
};
