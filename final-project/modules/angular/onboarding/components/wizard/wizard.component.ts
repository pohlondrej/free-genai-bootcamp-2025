import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { OnboardingService } from '../../onboarding.service';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-wizard',
  templateUrl: './wizard.component.html',
  styleUrls: ['./wizard.component.scss'],
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule]
})
export class WizardComponent {
  apiKey = '';
  isSubmitting = false;
  error = '';

  constructor(
    private onboardingService: OnboardingService,
    private router: Router
  ) { }

  async onSubmit(): Promise<void> {
    if (!this.apiKey) {
      this.error = 'Please enter your WaniKani API key';
      return;
    }

    this.isSubmitting = true;
    this.error = '';

    try {
      const initResult = await firstValueFrom(
        this.onboardingService.initialize({ api_key: this.apiKey })
      );
      
      if (initResult.is_initialized) {
        await this.router.navigate(['/dashboard']);
      } else {
        this.error = initResult.message || 'Failed to initialize with the provided API key';
      }
    } catch (err: any) {
      console.error('Initialization error:', err);
      this.error = err.error?.detail || err.message || 'Failed to initialize with the provided API key';
    } finally {
      this.isSubmitting = false;
    }
  }
}
