import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { KanjiDetailComponent } from './components/kanji/kanji-detail.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { 
    path: 'vocabulary',
    loadComponent: () => import('./components/vocabulary/vocabulary.component').then(m => m.VocabularyComponent)
  },
  { 
    path: 'kanji',
    loadComponent: () => import('./components/kanji/kanji.component').then(m => m.KanjiComponent)
  },
  { 
    path: 'kanji/:id',
    loadComponent: () => import('./components/kanji/kanji-detail.component').then(m => m.KanjiDetailComponent)
  },
  { 
    path: 'groups',
    loadComponent: () => import('./components/groups/groups.component').then(m => m.GroupsComponent)
  },
  { 
    path: 'sessions',
    loadComponent: () => import('./components/sessions/sessions.component').then(m => m.SessionsComponent)
  },
  {
    path: 'settings',
    loadComponent: () => import('./components/settings/settings.component').then(m => m.SettingsComponent)
  }
];
