const ModuleFederationPlugin = require('@angular-architects/module-federation/webpack').ModuleFederationPlugin;

module.exports = {
  output: {
    publicPath: 'auto'
  },
  optimization: {
    runtimeChunk: false
  },
  experiments: {
    outputModule: true
  },
  plugins: [
    new ModuleFederationPlugin({
      library: { type: 'module' },
      remotes: {
        // Remotes will be added dynamically based on plugin registration
      },
      shared: {
        '@angular/core': { singleton: true, strictVersion: true },
        '@angular/common': { singleton: true, strictVersion: true },
        '@angular/router': { singleton: true, strictVersion: true }
      }
    })
  ]
};
