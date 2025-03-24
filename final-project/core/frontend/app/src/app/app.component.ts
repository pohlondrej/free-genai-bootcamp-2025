import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';
import { NavigationComponent } from './components/navigation/navigation.component';

interface HealthResponse {
  status: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, NavigationComponent],
  template: `
    <app-navigation></app-navigation>
    <main class="content">
      <div class="status-container">
        <h2>API Status:</h2>
        <p [class]="status === 'healthy' ? 'status-healthy' : 'status-error'">
          {{ status || 'Checking...' }}
        </p>
      </div>
      <router-outlet></router-outlet>
    </main>
  `,
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  status: string = '';

  constructor(private api: ApiService) {
    this.checkApiStatus();
  }

  async checkApiStatus() {
    try {
      const health = await this.api.get<HealthResponse>('/health');
      this.status = health.status;
    } catch (error) {
      this.status = 'error';
    }
  }
}
