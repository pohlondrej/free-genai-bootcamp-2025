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
        <a routerLink="/">
          <span>DUO</span>
          <span class="logo-icon"></span>
          <span>KANI</span>
        </a>
      </div>
      <button class="menu-toggle" (click)="toggleMenu()" [attr.aria-expanded]="menuOpen">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </button>
      <ul class="nav-links" [class.open]="menuOpen">
        <li><a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}" (click)="closeMenu()">Dashboard</a></li>
        <li><a routerLink="/vocabulary" routerLinkActive="active" (click)="closeMenu()">Vocabulary</a></li>
        <li><a routerLink="/kanji" routerLinkActive="active" (click)="closeMenu()">Kanji</a></li>
        <li><a routerLink="/groups" routerLinkActive="active" (click)="closeMenu()">Groups</a></li>
        <li><a routerLink="/sessions" routerLinkActive="active" (click)="closeMenu()">Sessions</a></li>
        <li><a routerLink="/settings" routerLinkActive="active" (click)="closeMenu()">Settings</a></li>
      </ul>
    </nav>
  `,
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent {
  menuOpen = false;

  toggleMenu() {
    this.menuOpen = !this.menuOpen;
  }

  closeMenu() {
    this.menuOpen = false;
  }
}
