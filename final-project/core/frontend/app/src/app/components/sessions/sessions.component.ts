import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sessions',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="sessions">
      <h1>Study Sessions</h1>
      <p>Your study sessions will appear here.</p>
    </div>
  `,
  styleUrls: ['./sessions.component.scss']
})
export class SessionsComponent {}
