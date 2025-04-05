const { ModuleFederationPlugin } = require('webpack').container;

module.exports = {
  output: {
    publicPath: 'auto',
    uniqueName: 'app',
    scriptType: 'module'
  },
  experiments: {
    outputModule: true
  },
  optimization: {
    runtimeChunk: false
  },
  plugins: [
    new ModuleFederationPlugin({
      name: 'examplePlugin',
      filename: 'remoteEntry.js',
      exposes: {
        './Module': './src/app/hello.module.ts', // Expose the NgModule
        './Component': './src/app/hello.component.ts' // Keep this for potential other uses
      },
      shared: {
        '@angular/core': { singleton: true, strictVersion: false, requiredVersion: '^19.2.0' },
        '@angular/common': { singleton: true, strictVersion: false, requiredVersion: '^19.2.0' },
        '@angular/router': { singleton: true, strictVersion: false, requiredVersion: '^19.2.0' }
      },
      library: { type: 'module' }
    })
  ],
};
