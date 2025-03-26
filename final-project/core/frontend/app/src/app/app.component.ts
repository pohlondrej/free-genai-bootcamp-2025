import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, Router, NavigationEnd } from '@angular/router';
import { NavigationComponent } from './components/navigation/navigation.component';
import { ThemeService } from './services/theme.service';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, NavigationComponent],
  template: `
    <app-navigation *ngIf="!isOnboardingRoute"></app-navigation>
    <main [class.content]="!isOnboardingRoute">
      <router-outlet></router-outlet>
    </main>
  `,
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  isOnboardingRoute = false;

  constructor(
    themeService: ThemeService,
    private router: Router
  ) {
    // Just inject the service to initialize it
    
    // Track route changes to hide navigation on onboarding
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.isOnboardingRoute = event.url.startsWith('/onboarding');
    });
  }
}
