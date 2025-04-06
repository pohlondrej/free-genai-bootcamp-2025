import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { NavigationComponent } from '../navigation/navigation.component';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, NavigationComponent],
  template: `
    <app-navigation></app-navigation>
    <main class="content">
      <router-outlet></router-outlet>
    </main>
  `,
  styleUrls: ['./app-layout.component.scss']
})
export class AppLayoutComponent {}
