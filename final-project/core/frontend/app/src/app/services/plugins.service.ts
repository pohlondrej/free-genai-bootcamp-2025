import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { loadRemoteModule } from '@angular-architects/module-federation';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface PluginInfo {
  name: string;
  backend_endpoint: string;
  frontend_endpoint: string;
  module_name: string;
  image: string;
}

@Injectable({
  providedIn: 'root'
})
export class PluginsService {
  private pluginsSubject = new BehaviorSubject<PluginInfo[]>([]);
  plugins$ = this.pluginsSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadPlugins();
  }

  private loadPlugins() {
    this.http.get<PluginInfo[]>('/api/plugins').subscribe(
      plugins => this.pluginsSubject.next(plugins)
    );
  }

  getPlugins(): Observable<PluginInfo[]> {
    return this.plugins$;
  }

  async loadPluginComponent(plugin: PluginInfo): Promise<any> {
    try {
      const module = await loadRemoteModule({
        remoteEntry: `${plugin.frontend_endpoint}/remoteEntry.js`,
        remoteName: plugin.module_name,
        exposedModule: './Component'
      });
      
      return module.HelloComponent;
    } catch (err) {
      console.error(`Failed to load plugin ${plugin.name}:`, err);
      throw err;
    }
  }
}
