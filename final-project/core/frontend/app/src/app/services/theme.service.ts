import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private darkMode = new BehaviorSubject<boolean>(true); // Default to dark mode
  darkMode$ = this.darkMode.asObservable();

  constructor() {
    // Try to get saved preference, default to true (dark mode)
    const savedTheme = localStorage.getItem('darkMode');
    const prefersDark = savedTheme !== null ? savedTheme === 'true' : true;
    this.setDarkMode(prefersDark);
  }

  setDarkMode(isDark: boolean) {
    this.darkMode.next(isDark);
    localStorage.setItem('darkMode', isDark.toString());
    document.documentElement.classList.toggle('dark-theme', isDark);
  }

  toggleDarkMode() {
    this.setDarkMode(!this.darkMode.value);
  }
}
