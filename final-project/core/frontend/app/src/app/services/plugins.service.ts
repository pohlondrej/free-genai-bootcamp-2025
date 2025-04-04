import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { loadRemoteModule } from '@angular-architects/module-federation';

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
      console.log('Loading remote module from:', plugin.frontend_endpoint);
      
      // Load the remote entry module
      const containerModule = await loadRemoteModule({
        remoteEntry: `${plugin.frontend_endpoint}/remoteEntry.js`,
        type: 'module',
        exposedModule: './Component',
      });
      console.log('Remote module loaded');

      return containerModule.HelloComponent;
    } catch (err) {
      console.error(`Failed to load plugin ${plugin.name}:`, err);
      throw err;
    }
  }
}
