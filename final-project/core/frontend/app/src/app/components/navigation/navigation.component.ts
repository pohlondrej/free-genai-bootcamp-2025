import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navigation',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <nav>
      <div class="logo">
        <a routerLink="/">DuoKani</a>
      </div>
      <ul class="nav-links">
        <li><a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Dashboard</a></li>
        <li><a routerLink="/vocabulary" routerLinkActive="active">Vocabulary</a></li>
        <li><a routerLink="/kanji" routerLinkActive="active">Kanji</a></li>
        <li><a routerLink="/groups" routerLinkActive="active">Groups</a></li>
        <li><a routerLink="/sessions" routerLinkActive="active">Sessions</a></li>
      </ul>
    </nav>
  `,
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent {}
