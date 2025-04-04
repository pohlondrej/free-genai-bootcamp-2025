import { Component, OnInit, ViewChildren, ViewContainerRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PluginsService, PluginInfo } from '../../services/plugins.service';

@Component({
  selector: 'app-plugin-host',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="plugins-container">
      <h2>Plugins</h2>
      <div class="plugin-list">
        <div *ngFor="let plugin of plugins" class="plugin-item">
          <h3>{{ plugin.name }}</h3>
          <div #pluginContainer></div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .plugins-container {
      padding: 1rem;
    }
    .plugin-list {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1rem;
      margin-top: 1rem;
    }
    .plugin-item {
      border: 1px solid #ccc;
      border-radius: 4px;
      padding: 1rem;
    }
  `]
})
export class PluginHostComponent implements OnInit {
  @ViewChildren('pluginContainer', { read: ViewContainerRef }) 
  pluginContainer!: ViewContainerRef;

  plugins: PluginInfo[] = [];

  constructor(private pluginsService: PluginsService) {}

  ngOnInit() {
    this.pluginsService.getPlugins().subscribe(plugins => {
      this.plugins = plugins;
      this.loadPlugins();
    });
  }

  private async loadPlugins() {
    for (const plugin of this.plugins) {
      try {
        const component = await this.pluginsService.loadPluginComponent(plugin);
        this.pluginContainer.createComponent(component);
      } catch (err) {
        console.error(`Failed to load plugin ${plugin.name}:`, err);
      }
    }
  }
}
