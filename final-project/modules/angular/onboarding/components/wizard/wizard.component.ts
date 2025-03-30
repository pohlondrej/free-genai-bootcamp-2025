import { Component, OnDestroy } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { OnboardingService } from '../../onboarding.service';
import { WebSocketService } from '../../services/websocket.service';
import { firstValueFrom, Subscription } from 'rxjs';

@Component({
  selector: 'app-wizard',
  templateUrl: './wizard.component.html',
  styleUrls: ['./wizard.component.scss'],
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule]
})
export class WizardComponent implements OnDestroy {
  apiKey = '';
  geminiApiKey = '';
  isSubmitting = false;
  error = '';
  progress = 0;
  progressMessage = '';
  isImportComplete = false;
  private progressSubscription?: Subscription;

  constructor(
    private onboardingService: OnboardingService,
    private webSocketService: WebSocketService,
    private router: Router
  ) { }

  ngOnDestroy() {
    this.progressSubscription?.unsubscribe();
    this.webSocketService.disconnect();
  }

  async initializeWithJLPT(): Promise<void> {
    this.isSubmitting = true;
    this.error = '';
    this.progress = 0;
    this.progressMessage = 'Starting JLPT N5 import...';

    // Connect to WebSocket for progress updates
    this.progressSubscription = this.webSocketService.connect().subscribe({
      next: (progress) => {
        this.progress = progress.percentage;
        this.progressMessage = progress.message;
        if (progress.percentage === 100) {
          setTimeout(() => {
            this.isImportComplete = true;
            this.isSubmitting = false;
          }, 1000);
        }
      },
      error: (err) => {
        console.error('WebSocket error:', err);
      }
    });

    try {
      const result = await firstValueFrom(
        this.onboardingService.initialize({
          api_key: '',
          gemini_api_key: this.geminiApiKey || undefined,
          use_wanikani: false
        })
      );

      if (!result.is_initialized) {
        this.error = result.message || 'Failed to initialize application';
        this.isSubmitting = false;
      }
    } catch (err: any) {
      this.error = err.error?.detail || 'Failed to initialize application';
      this.isSubmitting = false;
    }
  }

  async onSubmit(): Promise<void> {
    if (!this.apiKey) {
      this.error = 'Please enter your WaniKani API key';
      return;
    }

    this.isSubmitting = true;
    this.error = '';
    this.progress = 0;
    this.progressMessage = 'Starting WaniKani import...';

    // Connect to WebSocket for progress updates
    this.progressSubscription = this.webSocketService.connect().subscribe({
      next: (progress) => {
        this.progress = progress.percentage;
        this.progressMessage = progress.message;
        if (progress.percentage === 100) {
          setTimeout(() => {
            this.isImportComplete = true;
            this.isSubmitting = false;
          }, 1000);
        }
      },
      error: (err) => {
        console.error('WebSocket error:', err);
      }
    });

    try {
      const result = await firstValueFrom(
        this.onboardingService.initialize({
          api_key: this.apiKey,
          gemini_api_key: this.geminiApiKey || undefined,
          use_wanikani: true
        })
      );

      if (!result.is_initialized) {
        this.error = result.message || 'Failed to initialize application';
        this.isSubmitting = false;
      }
    } catch (err: any) {
      this.error = err.error?.detail || 'Failed to initialize application';
      this.isSubmitting = false;
    }
  }

  goToApp(): void {
    this.router.navigate(['/']);
  }
}
