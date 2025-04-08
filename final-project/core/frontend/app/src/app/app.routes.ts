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
        path: 'games',
        loadComponent: () => import('./components/games/games.component')
          .then(m => m.GamesComponent)
      },

      // Games, hardcoded for now.
      // TODO: Make the module federation lazy-loading work (out of scope for final project)
      {
        path: 'games/example',
        loadChildren: () => import('./components/games/example/hello.module')
          .then(m => m.HelloModule)
      },
      {
        path: 'games/wkcrawler',
        loadChildren: () => import('./components/games/wkcrawler/wkcrawler.module')
          .then(m => m.WkCrawlerModule)
      },
      {
        path: 'games/flashcards',
        loadChildren: () => import('./components/games/flashcards/flashcards.module')
          .then(m => m.FlashcardsModule)
      }
    ]
  }
];
