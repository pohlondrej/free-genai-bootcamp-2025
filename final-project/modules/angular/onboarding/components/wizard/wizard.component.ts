import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { OnboardingService } from '../../onboarding.service';

@Component({
  selector: 'app-wizard',
  templateUrl: './wizard.component.html',
  styleUrls: ['./wizard.component.scss'],
  standalone: true,
  imports: [FormsModule]
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
      await this.onboardingService.initialize({ api_key: this.apiKey }).toPromise();
      this.router.navigate(['/']);
    } catch (err) {
      this.error = 'Failed to initialize with the provided API key';
    } finally {
      this.isSubmitting = false;
    }
  }
}
