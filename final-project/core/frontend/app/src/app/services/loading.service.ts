import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { OnboardingService } from '../onboarding/onboarding.service';
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoadingService {
  constructor(
    private router: Router,
    private onboardingService: OnboardingService
  ) {}

  async checkInitialization(): Promise<void> {
    try {
      const status = await firstValueFrom(this.onboardingService.getStatus());
      if (status.is_initialized) {
        await this.router.navigate(['/dashboard']);
      } else {
        await this.router.navigate(['/onboarding']);
      }
    } catch (error) {
      console.error('Error checking initialization:', error);
      await this.router.navigate(['/onboarding']);
    }
  }
}
