import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { KanjiDetailComponent } from './components/kanji/kanji-detail.component';
import { initializationGuard } from './guards/initialization.guard';
import { LoadingComponent } from './components/loading/loading.component';
import { AppLayoutComponent } from './components/layout/app-layout.component';

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
      { path: 'dashboard', loadComponent: () => import('./components/dashboard/dashboard.component').then(m => m.DashboardComponent) },
      { path: 'vocabulary', loadComponent: () => import('./components/vocabulary/vocabulary.component').then(m => m.VocabularyComponent) },
      { path: 'vocabulary/:id', loadComponent: () => import('./components/vocabulary/vocabulary-detail.component').then(m => m.VocabularyDetailComponent) },
      { path: 'kanji', loadComponent: () => import('./components/kanji/kanji.component').then(m => m.KanjiComponent) },
      { path: 'kanji/:id', loadComponent: () => import('./components/kanji/kanji-detail.component').then(m => m.KanjiDetailComponent) },
      { path: 'groups', loadComponent: () => import('./components/groups/groups.component').then(m => m.GroupsComponent) },
      { path: 'sessions', loadComponent: () => import('./components/sessions/sessions.component').then(m => m.SessionsComponent) },
      { path: 'settings', loadComponent: () => import('./components/settings/settings.component').then(m => m.SettingsComponent) }
    ]
  }
];
