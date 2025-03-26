import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { map, catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { OnboardingService, OnboardingStatus } from '../onboarding/onboarding.service';

export const initializationGuard = () => {
  const router = inject(Router);
  const onboardingService = inject(OnboardingService);

  return onboardingService.getStatus().pipe(
    map((status: OnboardingStatus) => {
      if (!status.is_initialized) {
        router.navigate(['/onboarding']);
        return false;
      }
      return true;
    }),
    catchError(() => {
      router.navigate(['/onboarding']);
      return of(false);
    })
  );
};
