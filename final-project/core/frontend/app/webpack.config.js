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
      name: 'app',
      library: { type: 'module' },
      shared: {
        '@angular/core': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0', eager: true },
        '@angular/common': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0', eager: true },
        '@angular/router': { singleton: true, strictVersion: true, requiredVersion: '^19.2.0', eager: true },
      }
    })
  ]
};
