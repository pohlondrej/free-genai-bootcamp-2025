import { Component, OnInit, ViewContainerRef, Injector } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, ActivatedRoute, Router } from '@angular/router';
import { PluginsService, PluginInfo } from '../../services/plugins.service';

@Component({
  selector: 'app-plugin-host',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="plugin-host">
      <header class="page-header">
        <button class="back-button" routerLink="/plugins">← Back to Plugins</button>
      </header>

      <div class="plugin-container" *ngIf="!loading && !error && plugin">
        <h2>{{ plugin.name }}</h2>
        <div class="plugin-mount" #pluginMount></div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading plugin...
      </div>

      <div class="error" *ngIf="error">
        {{ error }}
      </div>
    </div>
  `,
  styleUrls: ['./plugin-host.component.scss']
})
export class PluginHostComponent implements OnInit {
  plugin: PluginInfo | null = null;
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private pluginsService: PluginsService,
    private injector: Injector,
    private viewContainer: ViewContainerRef
  ) {}

  ngOnInit() {
    const pluginName = this.route.snapshot.paramMap.get('name');
    if (!pluginName) {
      this.router.navigate(['/plugins']);
      return;
    }

    this.pluginsService.getPlugins().subscribe({
      next: (plugins) => {
        const plugin = plugins.find(p => p.name === pluginName);
        if (!plugin) {
          this.error = `Plugin ${pluginName} not found`;
          this.loading = false;
          return;
        }
        this.plugin = plugin;
        this.loadPlugin(plugin);
      },
      error: (err) => {
        this.error = 'Failed to load plugin info. Please try again later.';
        this.loading = false;
        console.error('Error loading plugin info:', err);
      }
    });
  }

  private async loadPlugin(plugin: PluginInfo) {
    try {
      const componentType = await this.pluginsService.loadPluginComponent(plugin);
      const componentRef = this.viewContainer.createComponent(componentType, {
        injector: this.injector
      });
      componentRef.changeDetectorRef.detectChanges();
      this.loading = false;
    } catch (err) {
      this.error = `Failed to load plugin ${plugin.name}`;
      this.loading = false;
      console.error('Error loading plugin:', err);
    }
  }
}
