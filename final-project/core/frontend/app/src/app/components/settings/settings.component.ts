import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="settings">
      <h1>Settings</h1>
      <p>Application settings will appear here.</p>
    </div>
  `,
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent {}
