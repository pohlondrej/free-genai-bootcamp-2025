import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { PluginsService, PluginInfo } from '../../services/plugins.service';

@Component({
  selector: 'app-plugins',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="plugins-page">
      <header class="page-header">
        <h1>Plugins</h1>
      </header>

      <div class="plugins-grid" *ngIf="!loading && !error">
        <div class="plugin-card"
          *ngFor="let plugin of plugins"
          (click)="launchPlugin(plugin.name)">
          <div class="name">{{ plugin.name }}</div>
          <div class="endpoints">
            <div class="backend">{{ plugin.backend_endpoint }}</div>
            <div class="frontend">{{ plugin.frontend_endpoint }}</div>
          </div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading plugins...
      </div>

      <div class="error" *ngIf="error">
        {{ error }}
      </div>
    </div>
  `,
  styleUrls: ['./plugins.component.scss']
})
export class PluginsComponent implements OnInit {
  plugins: PluginInfo[] = [];
  loading = true;
  error: string | null = null;

  constructor(private pluginsService: PluginsService, private router: Router) {}

  ngOnInit() {
    this.loadPlugins();
  }

  launchPlugin(pluginName: string) {
    console.log(`PluginsComponent: launchPlugin - Navigating to ${pluginName}`);
    this.router.config.forEach(r => console.log(JSON.stringify(r)));
    this.router.navigate(['/plugins', 'plugin-hello', 'launch'])
      .then(() => { this.router.config.forEach(r => console.log(JSON.stringify(r))) })
      .then(() => console.log(`PluginsComponent: Navigation to ${pluginName} complete`))
      .catch(err => console.error(`PluginsComponent: Navigation error`, err));
  }

  private loadPlugins() {
    this.pluginsService.getPlugins().subscribe({
      next: (plugins) => {
        this.plugins = plugins;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load plugins. Please try again later.';
        this.loading = false;
        console.error('Error loading plugins:', err);
      }
    });
  }
}
