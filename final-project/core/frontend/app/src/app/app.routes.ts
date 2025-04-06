import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { KanjiDetailComponent } from './components/kanji/kanji-detail.component';
import { initializationGuard } from './guards/initialization.guard';
import { LoadingComponent } from './components/loading/loading.component';
import { AppLayoutComponent } from './components/layout/app-layout.component';
import { loadRemoteModule } from '@angular-architects/module-federation';

export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    component: LoadingComponent
  },
  {
    path: 'onboarding',
    loadChildren: () => import('./onboarding/onboarding.module')
      .then(m => m.OnboardingModule)
  },
  {
    path: '',
    component: AppLayoutComponent,
    canActivate: [initializationGuard],
    children: [
      {
        path: 'dashboard',
        component: DashboardComponent
      },
      {
        path: 'kanji',
        loadComponent: () => import('./components/kanji/kanji.component')
          .then(m => m.KanjiComponent)
      },
      {
        path: 'kanji/:id',
        component: KanjiDetailComponent
      },
      {
        path: 'vocabulary',
        loadComponent: () => import('./components/vocabulary/vocabulary.component')
          .then(m => m.VocabularyComponent)
      },
      {
        path: 'vocabulary/:id',
        loadComponent: () => import('./components/vocabulary/vocabulary-detail.component')
          .then(m => m.VocabularyDetailComponent)
      },
      {
        path: 'groups',
        loadComponent: () => import('./components/groups/groups.component')
          .then(m => m.GroupsComponent)
      },
      {
        path: 'groups/:id',
        loadComponent: () => import('./components/groups/group-details.component')
          .then(m => m.GroupDetailsComponent)
      },
      {
        path: 'settings',
        loadComponent: () => import('./components/settings/settings.component')
          .then(m => m.SettingsComponent)
      },
      {
        path: 'plugins',
        loadComponent: () => import('./components/plugins/plugins.component')
          .then(m => m.PluginsComponent)
      },
      {
        path: 'plugins/:name/launch',
        loadChildren: () => {
            console.log('[Host Router] Starting loadRemoteModule for HelloModule...'); // Add Log
            return loadRemoteModule({
                type: 'module',
                remoteEntry: 'http://localhost:4201/remoteEntry.js',
                exposedModule: './Module'
            })
            .then(m => {
                console.log('[Host Router] Remote module loaded. Raw module object:', m); // Add Log
                if (m && m.HelloModule) {
                    console.log('[Host Router] Found HelloModule class:', m.HelloModule); // Add Log
                    // Check if it has Angular metadata (might be stripped?)
                    console.log('[Host Router] HelloModule ngModuleDef:', (m.HelloModule as any)?.ɵmod); 
                } else {
                    console.error('[Host Router] HelloModule class NOT found in loaded remote module!');
                }
                return m.HelloModule; // Return the module class
            })
            .catch(err => {
                 console.error('[Host Router] Error loading remote module:', err); // Add Log
                 throw err; // Re-throw error
            });
        }
    }
    ]
  }
];
