import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ThemeService } from '../../services/theme.service';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="settings">
      <h1>Settings</h1>
      <div class="setting-item">
        <label class="theme-toggle">
          <span class="label-text">Dark Mode</span>
          <button 
            class="toggle-button" 
            [class.active]="isDarkMode"
            (click)="toggleTheme()"
            role="switch"
            [attr.aria-checked]="isDarkMode">
            <span class="toggle-thumb"></span>
          </button>
        </label>
      </div>
    </div>
  `,
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent {
  isDarkMode = true;

  constructor(private themeService: ThemeService) {
    this.themeService.darkMode$.subscribe(
      dark => this.isDarkMode = dark
    );
  }

  toggleTheme() {
    this.themeService.toggleDarkMode();
  }
}
