import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <h1>DuoKani WaniLingo</h1>
    <div class="status-container">
      <h2>API Status:</h2>
      <p [class]="status === 'healthy' ? 'status-healthy' : 'status-error'">
        {{ status || 'Checking...' }}
      </p>
    </div>
    <router-outlet></router-outlet>
  `,
  styles: [`
    :host {
      display: block;
      padding: 2rem;
      font-family: system-ui, -apple-system, sans-serif;
    }
    h1 {
      color: #2c3e50;
      margin-bottom: 2rem;
    }
    .status-container {
      background: #f8f9fa;
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 2rem;
    }
    .status-healthy {
      color: #2ecc71;
      font-weight: bold;
    }
    .status-error {
      color: #e74c3c;
      font-weight: bold;
    }
  `]
})
export class AppComponent implements OnInit {
  status: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.checkHealth();
  }

  private checkHealth() {
    this.apiService.getHealth().subscribe({
      next: (response) => {
        this.status = response.status;
      },
      error: (error) => {
        this.status = 'Error connecting to API';
        console.error('API Health Check Error:', error);
      }
    });
  }
}
