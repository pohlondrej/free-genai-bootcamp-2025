import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard">
      <h1>Welcome to DuoKani</h1>
      <p>Your Japanese learning journey starts here.</p>
    </div>
  `,
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {}
