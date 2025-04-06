import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="dashboard">
      <h1>Welcome to DuoKani!</h1>
      <p>Your Japanese learning journey starts here.</p>
      <a routerLink="/games" class="games-link">Play Games</a>
    </div>
  `,
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {}
