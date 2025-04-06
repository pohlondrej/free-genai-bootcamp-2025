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
        './Component': './src/app/hello.component.ts',
        './Module': './src/app/hello.module.ts'
      },
      shared: {
        '@angular/core': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0', eager: true },
        '@angular/common': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0', eager: true },
        '@angular/router': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0', eager: true }
      },
      library: { type: 'module' }
    })
  ]
};
